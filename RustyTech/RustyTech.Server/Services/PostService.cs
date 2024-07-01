using AutoMapper;
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

        public async Task<BlogPost?> CreateBlogPostAsync(BlogPost post)
        {

            if (post == null)
            {
                return null;
            }
            if (post.UserId == Guid.Empty)
            {
                return null;
            }
            var user = await _userService.GetByIdAsync(post.UserId);
            if (user == null)
            {
                return null;
            }
            post.Title = post.Title;
            post.Content = post.Content;
            post.ImageUrls = post.ImageUrls;
            post.CreatedAt = DateTime.UtcNow;
            post.UpdatedAt = DateTime.UtcNow;
            post.UserId = user.Id;
            post.IsPublished = true;
            await _context.BlogPosts.AddAsync(post);
            await _context.SaveChangesAsync();
            _logger.LogInformation($"Blog post {post.Id} created");
            return post;
        }

        public async Task<ImagePost?> CreateImagePostAsync(ImagePost post)
        {
            if (post == null)
            {
                return null;
            }
            if (post.UserId == Guid.Empty)
            {
                return null;
            }
            var user = await _userService.GetByIdAsync(post.UserId);
            if (user == null)
            {
                return null;
            }
            post.Title = post.Title;
            post.Content = post.Content;
            post.ImageUrl = post.ImageUrl;
            post.CreatedAt = DateTime.UtcNow;
            post.UpdatedAt = DateTime.UtcNow;
            post.UserId = user.Id;
            post.IsPublished = true;
            await _context.ImagePosts.AddAsync(post);
            await _context.SaveChangesAsync();
            _logger.LogInformation($"Image post {post.Id} created");
            return post;
        }

        public async Task<VideoPost?> CreateVideoPostAsync(VideoPost post)
        {
            if (post == null)
            {
                return null;
            }
            if (post.UserId == Guid.Empty)
            {
                return null;
            }
            var user = await _userService.GetByIdAsync(post.UserId);
            if (user == null)
            {
                return null;
            }
            post.Title = post.Title;
            post.Content = post.Content;
            post.VideoUrl = post.VideoUrl;
            post.CreatedAt = DateTime.UtcNow;
            post.UpdatedAt = DateTime.UtcNow;
            post.UserId = user.Id;
            post.IsPublished = true;
            await _context.VideoPosts.AddAsync(post);
            await _context.SaveChangesAsync();
            _logger.LogInformation($"Video post {post.Id} created");
            return post;
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



    }
}
