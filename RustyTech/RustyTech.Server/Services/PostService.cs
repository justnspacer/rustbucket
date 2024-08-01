using AutoMapper;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Posts;
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
                case ImageCreateDto imageDto:
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

        public async Task<List<PostReadDto>> GetAllAsync(bool published = true)
        {
            List<PostReadDto> allPosts = new List<PostReadDto>();

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

        public async Task<PostDto?> GetPostByIdAsync(int postId)
        {
            var blog = await GetPostById<BlogPost>(postId);
            if (blog != null)
            {
                var blogDto = _mapper.Map<BlogPost, PostDto>(blog);
                blogDto.PostType = "BlogPost";
                blogDto.Keywords = await GetPostKeywordsAsync(blogDto.Id);
                return blogDto;
            }

            var image = await GetPostById<ImagePost>(postId);
            if (image != null)
            {
                var imageDto = _mapper.Map<ImagePost, PostDto>(image);
                imageDto.PostType = "ImagePost";
                imageDto.Keywords = await GetPostKeywordsAsync(imageDto.Id);
                return imageDto;
            }

            var video = await GetPostById<VideoPost>(postId);
            if (video != null)
            {
                var videoDto = _mapper.Map<VideoPost, PostDto>(video);
                videoDto.PostType = "VideoPost";
                videoDto.Keywords = await GetPostKeywordsAsync(videoDto.Id);
                return videoDto;
            }
            return null;
        }

        public async Task<ResponseBase> EditPostAsync<T>(PostDto newData) where T : Post
        {
            var currentPost = await _context.Set<T>().Include(k => k.Keywords).ThenInclude(t => t.Keyword).FirstOrDefaultAsync(p => p.Id == newData.Id);
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

            if (currentPost.Keywords.Count > 0)
            {
                _keywordService.RemoveKeywords(currentPost, newData);
            }

            _keywordService.AddKeywords(currentPost, newData.Keywords);

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

        private async Task<List<PostReadDto>> GetAllBlogPosts(bool isPublished = true)
        {
            var blogs = await _context.BlogPosts.Where(b => b.IsPublished == isPublished).ToListAsync();
            var dtos = new List<PostReadDto>();
            foreach (var blog in blogs)
            {
                var dto = _mapper.Map<BlogPost, PostReadDto>(blog);
                dto.PostType = "BlogPost";
                var keywords = await GetPostKeywordsAsync(dto.Id);
                dto.Keywords = keywords;
                dtos.Add(dto);
            }
            return dtos;
        }

        private async Task<List<PostReadDto>> GetAllVideoPosts(bool isPublished = true)
        {
            var videos = await _context.VideoPosts.Where(b => b.IsPublished == isPublished).ToListAsync();
            var dtos = new List<PostReadDto>();
            foreach (var video in videos)
            {
                var dto = _mapper.Map<VideoPost, PostReadDto>(video);
                dto.PostType = "VideoPost";
                var keywords = await GetPostKeywordsAsync(dto.Id);
                dto.Keywords = keywords;
                dtos.Add(dto);
            }
            return dtos;
        }

        private async Task<List<PostReadDto>> GetAllImagePosts(bool isPublished = true)
        {
            var images = await _context.ImagePosts.Where(b => b.IsPublished == isPublished).ToListAsync();
            var dtos = new List<PostReadDto>();
            foreach (var image in images)
            {
                var dto = _mapper.Map<ImagePost, PostReadDto>(image);
                dto.PostType = "ImagePost";
                var keywords = await GetPostKeywordsAsync(dto.Id);
                dto.Keywords = keywords;
                dtos.Add(dto);
            }
            return dtos;
        }

        private async Task CreateVideoPost(VideoDto videoDto, UserDto user)
        {
            if (videoDto.VideoFile1 != null)
            {
                var content = StringHelper.SanitizeString(videoDto.Content);
                var date = DateTime.UtcNow;
                var video = new VideoPost()
                {
                    Title = StringHelper.SanitizeString(videoDto.Title),
                    Content = content,
                    PlainTextContent = StringHelper.ConvertHtmlToPlainText(content),
                    VideoFile = await _videoService.UploadVideoAsync(videoDto.VideoFile1),
                    CreatedAt = date,
                    UpdatedAt = date,
                    UserId = user.Id,
                    IsPublished = true //maybe change this to false, need publish automation
                };

                _keywordService.AddKeywords(video, videoDto.Keywords);
                await _context.VideoPosts.AddAsync(video);
                await _context.SaveChangesAsync();
            }
        }

        private async Task CreateImagePost(ImageCreateDto imageDto, UserDto user)
        {
            if (imageDto.ImageFile1 != null)
            {
                var content = StringHelper.SanitizeString(imageDto.Content);
                var date = DateTime.UtcNow;

                var image = new ImagePost()
                {
                    Title = StringHelper.SanitizeString(imageDto.Title),
                    Content = content,
                    PlainTextContent = StringHelper.ConvertHtmlToPlainText(content),
                    ImageFile = await _imageService.UploadImageAsync(imageDto.ImageFile1),
                    CreatedAt = date,
                    UpdatedAt = date,
                    UserId = user.Id,
                    IsPublished = true
                };

                _keywordService.AddKeywords(image, imageDto.Keywords);
                await _context.ImagePosts.AddAsync(image);
                await _context.SaveChangesAsync();
            }
        }

        private async Task CreateBlogPost(BlogDto blogDto, UserDto user)
        {
            var imageUrls = new List<string>();
            if (blogDto.ImageFiles1 != null)
            {
                foreach (var file in blogDto.ImageFiles1)
                {
                    imageUrls.Add(await _imageService.UploadImageAsync(file));
                }
            }
            if (blogDto.Content != null)
            {
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
                    UserId = user.Id,
                    IsPublished = true
                };

                _keywordService.AddKeywords(blog, blogDto.Keywords);
                await _context.BlogPosts.AddAsync(blog);
                await _context.SaveChangesAsync();
            }
        }

        private async Task AddPostsByType<T>(DbSet<T> dbSet, List<PostDto> allPosts, Expression<Func<T, bool>> predicate) where T : class
        {
            var posts = await dbSet.Where(predicate).ToListAsync();
            var postDtos = _mapper.Map<List<T>, List<PostDto>>(posts);

            //add type and keywords to each post
            foreach (var postDto in postDtos)
            {
                postDto.PostType = typeof(T).Name;

                var keywords = await GetPostKeywordsAsync(postDto.Id);
                postDto.Keywords = keywords;
            }

            allPosts.AddRange(postDtos);
        }

        private async Task<T?> GetPostById<T>(int postId) where T : class
        {
            return await _context.Set<T>().FindAsync(postId);
        }

        //keyword functions
        public async Task<List<string>> GetAllKeywordsAsync() => await _context.Keywords.Select(k => k.Text).ToListAsync();

        public async Task<List<string>> GetPostKeywordsAsync(int? id) => await _context.PostKeywords.Where(pk => pk.PostId == id).Select(k => k.Keyword.Text).ToListAsync();
        //keyword functions end

        //keyword helpers

    }
}
