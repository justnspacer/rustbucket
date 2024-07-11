using AutoMapper;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Services.Interfaces;
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

            }else if (DateTime.Equals(user.VerifiedAt, null))
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

            switch (post)
            {
                case BlogPost blogPost:
                    SetBlogPostProperties(blogPost);
                    await _context.BlogPosts.AddAsync(blogPost);
                    break;
                case ImagePost imagePost:
                    SetImagePostProperties(imagePost);
                    await _context.ImagePosts.AddAsync(imagePost);
                    break;
                case VideoPost videoPost:
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
                await AddPostsByType<BlogPost>(_context.BlogPosts, allPosts, p => p.IsPublished == true);
                await AddPostsByType<ImagePost>(_context.ImagePosts, allPosts, p => p.IsPublished == true);
                await AddPostsByType<VideoPost>(_context.VideoPosts, allPosts, p => p.IsPublished == true);

                _logger.LogInformation("All published posts retrieved");
            }
            else
            {
                await AddPostsByType<BlogPost>(_context.BlogPosts, allPosts, p => true);
                await AddPostsByType<ImagePost>(_context.ImagePosts, allPosts, p => true);
                await AddPostsByType<VideoPost>(_context.VideoPosts, allPosts, p => true);

                _logger.LogInformation("All posts retrieved");
            }

            allPosts = allPosts.OrderByDescending(p => p.CreatedAt).ToList();
            return allPosts;
        }

        public async Task<PostDto?> GetPostByIdAsync(int postId)
        {
            var bp = await GetPostById<BlogPost>(postId);
            if (bp != null) return _mapper.Map<BlogPost, PostDto>(bp);

            var ip = await GetPostById<ImagePost>(postId);
            if (ip != null) return _mapper.Map<ImagePost, PostDto>(ip);

            var vp = await GetPostById<VideoPost>(postId);
            if (vp != null) return _mapper.Map<VideoPost, PostDto>(vp);

            return null;
        }

        public async Task<ResponseBase> EditPostAsync<T>(int postId, T updatedPost, Guid userId) where T : Post
        {
            var post = await _context.Set<T>().FindAsync(postId);
            if (post == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.PostNotFound };
            }

            if (post.UserId != userId)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.Unauthorized };
            }

            post.Title = updatedPost.Title;
            post.Content = updatedPost.Content;
            post.UpdatedAt = DateTime.UtcNow;

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

        private void SetBlogPostProperties(BlogPost post)
        {
            post.ImageUrls = post.ImageUrls;
        }

        private void SetImagePostProperties(ImagePost post)
        {
            post.ImageUrl = post.ImageUrl;
        }

        private void SetVideoPostProperties(VideoPost post)
        {
            post.VideoUrl = post.VideoUrl;
        }
    }
}
