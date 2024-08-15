using AutoMapper;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Posts;
using RustyTech.Server.Services.Interfaces;
using RustyTech.Server.Utilities;

namespace RustyTech.Server.Services
{
    public class PostService : IPostService
    {
        private DataContext _context;
        private readonly IMapper _mapper;
        private IUserService _userService;
        private ILogger<IPostService> _logger;
        private IImageService _imageService;
        private IVideoService _videoService;
        private IKeywordService _keywordService;

        public PostService(DataContext context, IMapper mapper,
            IUserService userService, ILogger<IPostService> logger,
            IImageService imageService,
            IVideoService videoService, IKeywordService keywordService)
        {
            _context = context;
            _mapper = mapper;
            _userService = userService;
            _logger = logger;
            _imageService = imageService;
            _videoService = videoService;
            _keywordService = keywordService;
        }

        //Shared Post Tasks
        public async Task<List<GetPostRequest>> GetAllAsync(bool published = true)
        {
            List<GetPostRequest> allPosts = new List<GetPostRequest>();

            if (published)
            {
                var blogs = await GetAllBlogPosts();
                allPosts.AddRange(blogs);
                var images = await GetAllImagePosts();
                allPosts.AddRange(images);
                var videos = await GetAllVideoPosts();
                allPosts.AddRange(videos);
                _logger.LogInformation("All published posts retrieved");
            }
            else
            {
                var blogs = await GetAllBlogPosts(false);
                allPosts.AddRange(blogs);
                var images = await GetAllImagePosts(false);
                allPosts.AddRange(images);
                var videos = await GetAllVideoPosts(false);
                allPosts.AddRange(videos);
                _logger.LogInformation("All posts retrieved");
            }

            allPosts = allPosts.OrderByDescending(p => p.CreatedAt).ToList();
            return allPosts;
        }

        public async Task<GetPostRequest?> GetPostByIdAsync(int postId)
        {
            var blog = await GetPostById<BlogPost>(postId);
            if (blog != null)
            {
                var blogDto = _mapper.Map<BlogPost, GetPostRequest>(blog);
                blogDto.PostType = "BlogPost";
                blogDto.User = await _userService.GetByIdAsync(blogDto.UserId);
                blogDto.Keywords = await _keywordService.GetPostKeywordsAsync(blogDto.Id);
                return blogDto;
            }

            var image = await GetPostById<ImagePost>(postId);
            if (image != null)
            {
                var imageDto = _mapper.Map<ImagePost, GetPostRequest>(image);
                imageDto.PostType = "ImagePost";
                imageDto.User = await _userService.GetByIdAsync(imageDto.UserId);
                imageDto.Keywords = await _keywordService.GetPostKeywordsAsync(imageDto.Id);
                return imageDto;
            }

            var video = await GetPostById<VideoPost>(postId);
            if (video != null)
            {
                var videoDto = _mapper.Map<VideoPost, GetPostRequest>(video);
                videoDto.PostType = "VideoPost";
                videoDto.User = await _userService.GetByIdAsync(videoDto.UserId);
                videoDto.Keywords = await _keywordService.GetPostKeywordsAsync(videoDto.Id);
                return videoDto;
            }
            return null;
        }

        private async Task<T?> GetPostById<T>(int postId) where T : class
        {
            return await _context.Set<T>().FindAsync(postId);
        }
        
        public async Task<ResponseBase> EditPostAsync<T>(UpdatePostRequest newData) where T : Post
        {
            var currentPost = await _context.Set<T>().Include(k => k.Keywords).ThenInclude(t => t.Keyword).FirstOrDefaultAsync(p => p.Id == newData.Id);
            if (currentPost == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.PostNotFound };
            }

            if (currentPost.UserId != newData.UserId.ToString())
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.Unauthorized };
            }

            currentPost.Title = newData.Title;
            currentPost.Content = newData.Content;

            if (currentPost.Keywords.Count > 0)
            {
                _keywordService.RemovePostKeywords(currentPost, newData);
            }

            _keywordService.AddPostKeywords(currentPost, newData.Keywords);

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

        
        //VideoPost Tasks
        public async Task<ResponseBase> CreateVideoPostAsync(CreateVideoRequest post)
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

            var response = await CreateVideoPost(post, user);
            return response;
        }
        
        private async Task<ResponseBase> CreateVideoPost(CreateVideoRequest videoDto, GetUserRequest user)
        {
            if (videoDto.VideoFile != null)
            {
                var userfromDb = await _context.Users.FirstOrDefaultAsync(u => u.Id == user.Id);
                if (userfromDb == null)
                {
                    return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.UserNotFound };
                }
                var content = StringHelper.SanitizeString(videoDto.Content);
                var date = DateTime.UtcNow;
                var video = new VideoPost()
                {
                    Title = StringHelper.SanitizeString(videoDto.Title),
                    Content = content,
                    PlainTextContent = StringHelper.ConvertHtmlToPlainText(content),
                    VideoFile = await _videoService.UploadVideoAsync(videoDto.VideoFile),
                    CreatedAt = date,
                    UpdatedAt = date,
                    UserId = user.Id.ToString(),
                    User = userfromDb,
                    IsPublished = true //maybe change this to false, need publish automation
                };

                _keywordService.AddPostKeywords(video, videoDto.Keywords);
                await _context.VideoPosts.AddAsync(video);
                await _context.SaveChangesAsync();
                _logger.LogInformation($"Video post {video.Id} created");
                return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.PostCreated };
            }
            return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.InvalidRequest };
        }

        private async Task<List<GetPostRequest>> GetAllVideoPosts(bool isPublished = true)
        {
            var videos = await _context.VideoPosts.Where(b => b.IsPublished == isPublished).Include(user => user.User).ToListAsync();
            var dtos = new List<GetPostRequest>();
            foreach (var video in videos)
            {
                var dto = _mapper.Map<VideoPost, GetPostRequest>(video);
                dto.PostType = "VideoPost";
                var keywords = await _keywordService.GetPostKeywordsAsync(dto.Id);
                dto.Keywords = keywords;
                dtos.Add(dto);
            }
            return dtos;
        }

        
        //ImagePost Tasks
        public async Task<ResponseBase> CreateImagePostAsync(CreateImageRequest post)
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

            var response = await CreateImagePost(post, user);
            return response;
        }

        private async Task<ResponseBase> CreateImagePost(CreateImageRequest imageDto, GetUserRequest user)
        {
            if (imageDto.ImageFile != null)
            {
                var userfromDb = await _context.Users.FirstOrDefaultAsync(u => u.Id == user.Id);
                if (userfromDb == null)
                {
                    return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.UserNotFound };
                }
                var content = StringHelper.SanitizeString(imageDto.Content);
                var date = DateTime.UtcNow;
                var image = new ImagePost()
                {
                    Title = StringHelper.SanitizeString(imageDto.Title),
                    Content = content,
                    PlainTextContent = StringHelper.ConvertHtmlToPlainText(content),
                    ImageFile = await _imageService.UploadImageAsync(imageDto.ImageFile),
                    CreatedAt = date,
                    UpdatedAt = date,
                    UserId = user.Id.ToString(),
                    User = userfromDb,
                    IsPublished = true
                };

                _keywordService.AddPostKeywords(image, imageDto.Keywords);
                await _context.ImagePosts.AddAsync(image);
                await _context.SaveChangesAsync();
                _logger.LogInformation($"Image post {image.Id} created");
                return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.PostCreated };
            }
            return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.InvalidRequest };
        }

        private async Task<List<GetPostRequest>> GetAllImagePosts(bool isPublished = true)
        {
            var images = await _context.ImagePosts.Where(b => b.IsPublished == isPublished).Include(user => user.User).ToListAsync();
            var dtos = new List<GetPostRequest>();
            foreach (var image in images)
            {
                var dto = _mapper.Map<ImagePost, GetPostRequest>(image);
                dto.PostType = "ImagePost";
                var keywords = await _keywordService.GetPostKeywordsAsync(dto.Id);
                dto.Keywords = keywords;
                dtos.Add(dto);
            }
            return dtos;
        }

        
        //BlogPost Tasks
        public async Task<ResponseBase> CreateBlogPostAsync(CreateBlogRequest post)
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

            var response = await CreateBlogPost(post, user);
            return response;
        }

        private async Task<ResponseBase> CreateBlogPost(CreateBlogRequest blogDto, GetUserRequest user)
        {
            var imageUrls = new List<string>();
            if (blogDto.ImageFiles != null)
            {
                foreach (var file in blogDto.ImageFiles)
                {
                    imageUrls.Add(await _imageService.UploadImageAsync(file));
                }
            }
            if (blogDto.Content != null)
            {
                var userfromDb = await _context.Users.FirstOrDefaultAsync(u => u.Id == user.Id);
                if (userfromDb == null)
                {
                    return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.UserNotFound };
                }
                var content = StringHelper.SanitizeString(blogDto.Content);
                var date = DateTime.UtcNow;
                var blog = new BlogPost()
                {
                    Title = StringHelper.SanitizeString(blogDto.Title),
                    Content = content,
                    PlainTextContent = StringHelper.ConvertHtmlToPlainText(content),
                    ImageFiles = imageUrls,
                    CreatedAt = date,
                    UpdatedAt = date,
                    UserId = user.Id.ToString(),
                    User = userfromDb,
                    IsPublished = true
                };

                _keywordService.AddPostKeywords(blog, blogDto.Keywords);
                await _context.BlogPosts.AddAsync(blog);
                await _context.SaveChangesAsync();
                _logger.LogInformation($"Blog post {blog.Id} created");
                return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.PostCreated };
            }
            return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.InvalidRequest };
        }

        private async Task<List<GetPostRequest>> GetAllBlogPosts(bool isPublished = true)
        {
            var blogs = await _context.BlogPosts.Where(b => b.IsPublished == isPublished).Include(user => user.User).ToListAsync();
            var dtos = new List<GetPostRequest>();
            foreach (var blog in blogs)
            {
                var dto = _mapper.Map<BlogPost, GetPostRequest>(blog);
                dto.PostType = "BlogPost";
                var keywords = await _keywordService.GetPostKeywordsAsync(dto.Id);
                dto.Keywords = keywords;
                dtos.Add(dto);
            }
            return dtos;
        }
    }
}
