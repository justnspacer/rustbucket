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

        public async Task<ResponseBase> CreatePostAsync(PostDto post)
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

            switch (post)
            {
                case BlogDto blogDto:
                    await CreateBlogPost(blogDto, user);
                    break;
                case ImageDto imageDto:
                    await CreateImagePost(imageDto, user);
                    break;
                case VideoDto videoDto:
                    await CreateVideoPost(videoDto, user);
                    break;
                default:
                    return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.InvalidRequest };
            }
            _logger.LogInformation($"Post {post.Id} created");
            return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.PostCreated };
        }

        public async Task<List<PostDto>> GetAllAsync(bool published = true)
        {
            List<PostDto> allPosts = new List<PostDto>();
            List<BlogDto> blogs = new List<BlogDto>();
            List<ImageDto> images = new List<ImageDto>();
            List<VideoDto> videos = new List<VideoDto>();

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

        public async Task<ResponseBase> EditPostAsync<T>(PostDto newData) where T : Post
        {
            var currentPost = await _context.Set<T>().FindAsync(newData.Id);
            if (currentPost == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.PostNotFound };
            }

            if (currentPost.UserId != newData.UserId)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.Unauthorized };
            }

            currentPost.Title = newData.Title;
            currentPost.Content = newData.Content;

            var existingKeywords = currentPost.Keywords.Select(pk => pk).ToList();
            var newKeywords = newData.Keywords?.Except(existingKeywords.Select(pk => pk.Keyword.Text)).ToList();

            RemoveKeywords(currentPost, existingKeywords, newData);

            if (newKeywords != null)
            {
                await AddKeywords(currentPost, newKeywords);
            }

            currentPost.UpdatedAt = DateTime.UtcNow;
            await _context.SaveChangesAsync();

            _logger.LogInformation($"{typeof(T).Name} post {newData.Id} updated");

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

        private async Task CreateVideoPost(VideoDto videoDto, UserDto user)
        {
            var video = new Video()
            {
                Title = videoDto.Title,
                Content = videoDto.Content,
                VideoUrl = videoDto.VideoUrl,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow,
                UserId = user.Id,
                IsPublished = true
            };

            await AddKeywords(video, videoDto.Keywords);
            await _context.VideoPosts.AddAsync(video);
            await _context.SaveChangesAsync();

        }

        private async Task CreateImagePost(ImageDto imageDto, UserDto user)
        {
            var image = new Image()
            {
                Title = imageDto.Title,
                Content = imageDto.Content,
                ImageUrl = imageDto.ImageUrl,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow,
                UserId = user.Id,
                IsPublished = true
            };

            await AddKeywords(image, imageDto.Keywords);
            await _context.ImagePosts.AddAsync(image);
            await _context.SaveChangesAsync();
        }

        private async Task CreateBlogPost(BlogDto blogDto, UserDto user)
        {
            var blog = new Blog()
            {
                Title = blogDto.Title,
                Content = blogDto.Content,
                ImageUrls = blogDto.ImageUrls,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow,
                UserId = user.Id,
                IsPublished = true
            };

            await AddKeywords(blog, blogDto.Keywords);
            await _context.BlogPosts.AddAsync(blog);
            await _context.SaveChangesAsync();
        }

        private async Task AddKeywords(Post post, List<string>? keywords)
        {
            if (keywords != null)
            {
                var normailizedKeywords = KeywordNormalizer.NormalizeKeywords(keywords);
                foreach (var text in normailizedKeywords)
                {
                    var currentKeyword = _context.Keywords.FirstOrDefault(k => k.Text == text);
                    if (currentKeyword == null)
                    {
                        Keyword keyword = new Keyword { Text = text };
                        PostKeyword postKeyword = new PostKeyword { Post = post, Keyword = keyword };
                        post.Keywords.Add(postKeyword);
                        await _context.Keywords.AddAsync(keyword);
                    }
                }
            }
        }

        private void RemoveKeywords(Post currentPost, List<PostKeyword> existingKeywords, PostDto newData)
        {
            var removedKeywords = existingKeywords.Select(pk => pk.Keyword?.Text).Except(newData.Keywords).ToList();

            foreach (var keywordText in removedKeywords)
            {
                var postKeyword = currentPost.Keywords.SingleOrDefault(k => k.Keyword?.Text == keywordText);
                if (postKeyword != null)
                {
                    currentPost.Keywords.Remove(postKeyword);
                }
            }
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
    }
}
