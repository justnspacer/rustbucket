using AutoMapper;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Services.Interfaces;
using RustyTech.Server.Utilities;
using System.Linq.Expressions;

namespace RustyTech.Server.Services
{
    public class PostService : IPostService
    {
        private DataContext _context;
        private readonly IMapper _mapper;
        private IUserService _userService;
        private ILogger<IPostService> _logger;

        public PostService(DataContext context, IMapper mapper, IUserService userService, ILogger<IPostService> logger)
        {
            _context = context;
            _mapper = mapper;
            _userService = userService;
            _logger = logger;
        }

        public async Task<ResponseBase> CreatePostAsync<T>(T post) where T : Post
        {
            if (post == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.BadRequest };
            }

            if (post.UserId == Guid.Empty)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.IdRequired };
            }

            var user = await _userService.GetByIdAsync(post.UserId);
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.UserNotFound };

            }
            else if (DateTime.Equals(user.VerifiedAt, null))
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.UserNotVerified };
            }

            post.Title = post.Title;
            post.Content = post.Content;
            DateTime date = DateTime.UtcNow;
            post.CreatedAt = date;
            post.UpdatedAt = date;
            post.UserId = user.Id;
            post.IsPublished = true;

            if (post.Keywords != null)
            {
                foreach (var keyword in post.Keywords)
                {
                    var obj = await GetKeywordAsync(keyword);
                    if (obj == null)
                    {
                        var newKeyword = new Keyword() { Text = keyword.Text };
                        if (newKeyword.Text != null)
                        {
                            var normalizedKeyword = KeywordNormalizer.Normalize(newKeyword.Text);
                            await AddKeywordAsync(newKeyword);
                        }

                    }
                }
            }

            switch (post)
            {
                case Blog blogPost:
                    SetBlogPostProperties(blogPost);
                    await _context.BlogPosts.AddAsync(blogPost);
                    break;
                case Image imagePost:
                    SetImagePostProperties(imagePost);
                    await _context.ImagePosts.AddAsync(imagePost);
                    break;
                case Video videoPost:
                    SetVideoPostProperties(videoPost);
                    await _context.VideoPosts.AddAsync(videoPost);
                    break;
                default:
                    return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.InvalidRequest };
            }

            await _context.SaveChangesAsync();
            _logger.LogInformation($"{typeof(T).Name} post {post.Id} created");
            return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.PostCreated };
        }

        public async Task<List<PostDto>> GetAllAsync(bool published = true)
        {
            List<PostDto> allPosts = new List<PostDto>();

            if (published)
            {
                await AddPostsByType<Blog>(_context.BlogPosts, allPosts, p => p.IsPublished == true);
                await AddPostsByType<Image>(_context.ImagePosts, allPosts, p => p.IsPublished == true);
                await AddPostsByType<Video>(_context.VideoPosts, allPosts, p => p.IsPublished == true);

                _logger.LogInformation("All published posts retrieved");
            }
            else
            {
                await AddPostsByType<Blog>(_context.BlogPosts, allPosts, p => true);
                await AddPostsByType<Image>(_context.ImagePosts, allPosts, p => true);
                await AddPostsByType<Video>(_context.VideoPosts, allPosts, p => true);

                _logger.LogInformation("All posts retrieved");
            }

            allPosts = allPosts.OrderByDescending(p => p.CreatedAt).ToList();
            return allPosts;
        }

        public async Task<PostDto?> GetPostByIdAsync(int postId)
        {
            var bp = await GetPostById<Blog>(postId);
            if (bp != null) return _mapper.Map<Blog, PostDto>(bp);

            var ip = await GetPostById<Image>(postId);
            if (ip != null) return _mapper.Map<Image, PostDto>(ip);

            var vp = await GetPostById<Video>(postId);
            if (vp != null) return _mapper.Map<Video, PostDto>(vp);

            return null;
        }

        public async Task<ResponseBase> EditPostAsync<T>(PostEditRequest request) where T : Post
        {
            var post = await _context.Set<T>().FindAsync(request.PostId);
            if (post == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.PostNotFound };
            }

            if (post.UserId != request.UserId)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.Unauthorized };
            }

            post.Title = request.UpdatedPost?.Title;
            post.Content = request.UpdatedPost?.Content;
            post.UpdatedAt = DateTime.UtcNow;
            var updatedKeywords = request.UpdatedPost?.Keywords;

            if (updatedKeywords != null && updatedKeywords != post.Keywords)
            {
                foreach (var keyword in updatedKeywords)
                {
                    var obj = await GetKeywordAsync(keyword);
                    if (obj == null)
                    {
                        var newKeyword = new Keyword() { Text = keyword.Text };
                        if (newKeyword.Text != null)
                        {
                            var normalizedKeyword = KeywordNormalizer.Normalize(newKeyword.Text);
                            await AddKeywordAsync(newKeyword);
                        }

                    }
                }
            }

            await _context.SaveChangesAsync();

            _logger.LogInformation($"{typeof(T).Name} post {post.Id} updated");

            return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.PostUpdated };
        }

        public async Task<ResponseBase> TogglePostPublishedStatusAsync<T>(int postId) where T : Post
        {
            var post = await _context.Set<T>().FindAsync(postId);
            if (post == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.PostNotFound };
            }

            post.IsPublished = !post.IsPublished;
            post.UpdatedAt = DateTime.UtcNow;
            await _context.SaveChangesAsync();

            _logger.LogInformation($"Post {post.Id} is published? {post.IsPublished}");

            return new ResponseBase() { IsSuccess = true, Message = $"Post {post.Id} publish status: {post.IsPublished}" };
        }

        public async Task<List<string?>> GetAllKeywordsAsync() => await _context.Keywords.Select(k => k.Text).ToListAsync();
        private async Task<Keyword?> GetKeywordAsync(Keyword keyword) => await _context.Keywords.FirstOrDefaultAsync(key => key.Text == keyword.Text);

        private async Task AddKeywordAsync(Keyword keyword)
        {
            _context.Keywords.Add(keyword);
            await _context.SaveChangesAsync();
        }

        private async Task AddPostsByType<T>(DbSet<T> dbSet, List<PostDto> allPosts, Expression<Func<T, bool>> predicate) where T : class
        {
            var posts = await dbSet.Where(predicate).ToListAsync();
            var postDtos = _mapper.Map<List<T>, List<PostDto>>(posts);
            allPosts.AddRange(postDtos);
        }

        private async Task<T?> GetPostById<T>(int postId) where T : class
        {
            return await _context.Set<T>().FindAsync(postId);
        }

        private void SetBlogPostProperties(Blog post)
        {
            post.ImageUrls = post.ImageUrls;
        }

        private void SetImagePostProperties(Image post)
        {
            post.ImageUrl = post.ImageUrl;
        }

        private void SetVideoPostProperties(Video post)
        {
            post.VideoUrl = post.VideoUrl;
        }
    }
}
