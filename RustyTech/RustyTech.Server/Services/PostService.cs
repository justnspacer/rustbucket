using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Services
{
    public class PostService : IPostService
    {
        private DataContext _context;
        private IUserService _userService;
        private ILogger<IPostService> _logger;

        public PostService(DataContext context, IUserService userService, ILogger<IPostService> logger)
        {
            _context = context;
            _userService = userService;
            _logger = logger;
        }

        public async Task<BlogPost?> CreateBlogPostAsync(BlogPost post)
        {

            if (post == null)
            {
                return null;
            }
            if (post.User == null)
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
            if (post.User == null)
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
            if (post.User == null)
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

        public async Task<List<Post>> GetAllAsync(bool published = true)
        {
            List<Post> allPosts = new List<Post>();
            if (published)
            {
                List<BlogPost> blogPosts = await _context.BlogPosts.Where(p => p.IsPublished == true).ToListAsync();
                allPosts.AddRange(blogPosts);

                List<ImagePost> imagePosts = await _context.ImagePosts.Where(p => p.IsPublished == true).ToListAsync();
                allPosts.AddRange(imagePosts);

                List<VideoPost> videoPosts = await _context.VideoPosts.Where(p => p.IsPublished == true).ToListAsync();
                allPosts.AddRange(videoPosts);
                _logger.LogInformation($"All published posts retrieved");

            }
            else
            {
                List<BlogPost> blogPosts = await _context.BlogPosts.ToListAsync();
                allPosts.AddRange(blogPosts);

                List<ImagePost> imagePosts = await _context.ImagePosts.ToListAsync();
                allPosts.AddRange(imagePosts);

                List<VideoPost> videoPosts = await _context.VideoPosts.ToListAsync();
                allPosts.AddRange(videoPosts);
                _logger.LogInformation($"All posts retrieved");
            }

            return allPosts;
        }



    }
}
