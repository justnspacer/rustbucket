using AutoMapper;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Services.Interfaces;

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

        public async Task<ResponseBase> CreateBlogPostAsync(BlogPost post)
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
            DateTime date = DateTime.UtcNow;
            post.Title = post.Title;
            post.Content = post.Content;
            post.ImageUrls = post.ImageUrls;
            post.CreatedAt = date;
            post.UpdatedAt = date;
            post.UserId = user.Id;
            post.IsPublished = true;
            await _context.BlogPosts.AddAsync(post);
            await _context.SaveChangesAsync();
            _logger.LogInformation($"Blog post {post.Id} created");
            return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.PostCreated };
        }

        public async Task<ResponseBase> CreateImagePostAsync(ImagePost post)
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
            DateTime date = DateTime.UtcNow;
            post.Title = post.Title;
            post.Content = post.Content;
            post.ImageUrl = post.ImageUrl;
            post.CreatedAt = date;
            post.UpdatedAt = date;
            post.UserId = user.Id;
            post.IsPublished = true;
            await _context.ImagePosts.AddAsync(post);
            await _context.SaveChangesAsync();
            _logger.LogInformation($"Image post {post.Id} created");
            return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.PostCreated };
        }

        public async Task<ResponseBase> CreateVideoPostAsync(VideoPost post)
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
            DateTime date = DateTime.UtcNow;
            post.Title = post.Title;
            post.Content = post.Content;
            post.VideoUrl = post.VideoUrl;
            post.CreatedAt = date;
            post.UpdatedAt = date;
            post.UserId = user.Id;
            post.IsPublished = true;
            await _context.VideoPosts.AddAsync(post);
            await _context.SaveChangesAsync();
            _logger.LogInformation($"Video post {post.Id} created");
            return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.PostCreated };
        }

        public async Task<List<PostDto>> GetAllAsync(bool published = true)
        {
            List<PostDto> allPosts = new List<PostDto>();
            if (published)
            {
                List<BlogPost> blogPosts = await _context.BlogPosts.Where(p => p.IsPublished == true).ToListAsync();
                var blogMap = _mapper.Map<List<BlogPost>, List<PostDto>>(blogPosts);
                allPosts.AddRange(blogMap);

                List<ImagePost> imagePosts = await _context.ImagePosts.Where(p => p.IsPublished == true).ToListAsync();
                var imageMap = _mapper.Map<List<ImagePost>, List<PostDto>>(imagePosts);
                allPosts.AddRange(imageMap);

                List<VideoPost> videoPosts = await _context.VideoPosts.Where(p => p.IsPublished == true).ToListAsync();
                var videoMap = _mapper.Map<List<VideoPost>, List<PostDto>>(videoPosts);
                allPosts.AddRange(videoMap);
                _logger.LogInformation($"All published posts retrieved");

            }
            else
            {
                List<BlogPost> blogPosts = await _context.BlogPosts.ToListAsync();
                var blogMap = _mapper.Map<List<BlogPost>, List<PostDto>>(blogPosts);
                allPosts.AddRange(blogMap);

                List<ImagePost> imagePosts = await _context.ImagePosts.ToListAsync();
                var imageMap = _mapper.Map<List<ImagePost>, List<PostDto>>(imagePosts);
                allPosts.AddRange(imageMap);

                List<VideoPost> videoPosts = await _context.VideoPosts.ToListAsync();
                var videoMap = _mapper.Map<List<VideoPost>, List<PostDto>>(videoPosts);
                allPosts.AddRange(videoMap);
                _logger.LogInformation($"All posts retrieved");
            }

            return allPosts;
        }

        public async Task<PostDto?> GetPostByIdAsync(int postId)
        {
            BlogPost blogPost = await _context.BlogPosts.FindAsync(postId);
            if (blogPost != null)
            {
                return _mapper.Map<BlogPost, PostDto>(blogPost);
            }

            ImagePost imagePost = await _context.ImagePosts.FindAsync(postId);
            if (imagePost != null)
            {
                return _mapper.Map<ImagePost, PostDto>(imagePost);
            }

            VideoPost videoPost = await _context.VideoPosts.FindAsync(postId);
            if (videoPost != null)
            {
                return _mapper.Map<VideoPost, PostDto>(videoPost);
            }

            return null;
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
    }
}
