using AutoMapper;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Moq;
using RustyTech.Server.Constants;
using RustyTech.Server.Data;
using RustyTech.Server.AutoMapper;
using RustyTech.Server.Models.User;
using RustyTech.Server.Services;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Tests
{
    public class PostServiceTestV1
    {
        private DataContext _context;
        private IMapper _mapper;
        private IUserService _userService;
        private IPostService _postService;

        [SetUp]
        public void Setup()
        {
            var loggerMock = new Mock<ILogger<PostService>>();

            var options = new DbContextOptionsBuilder<DataContext>()
                .UseInMemoryDatabase(databaseName: "TestDatabase")
                .Options;

            _context = new DataContext(options);
            _mapper = new MapperConfiguration(cfg => cfg.AddProfile(new MappingProfile())).CreateMapper();
            _userService = new UserService(_context, _mapper, new Logger<UserService>(new LoggerFactory()));
            _postService = new PostService(_context, _mapper, _userService, loggerMock.Object);
        }

        [TearDown]
        public void TearDown()
        {
            _context.Database.EnsureDeleted();
            _context.Dispose();
        }

        [Test]
        public async Task CreatePostAsync_WithValidPost_ReturnsSuccessResponse()
        {
            // Arrange
            var post = new BlogDto()
            {
                Id = 1,
                UserId = Guid.NewGuid(),
                Title = "Test Post",
                Content = "This is a test post",
                CreatedAt = new DateTime(7775, 3, 09),
                UpdatedAt = new DateTime(7775, 3, 09),
                IsPublished = true
            };

            // Mock the user service to return a valid user
            var user = new User
            {
                Id = post.UserId,
                UserName = "testuser",
                VerifiedAt = new DateTime(7775, 3, 09)
            };
            _context.Users.Add(user);
            _context.SaveChanges();

            // Act
            var response = await _postService.CreatePostAsync(post);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo(Messages.Info.PostCreated));
        }

        [Test]
        public async Task CreatePostAsync_WithNullPost_ReturnsBadRequestResponse()
        {
            // Arrange
            BlogDto post = new BlogDto();

            // Act
            var response = await _postService.CreatePostAsync(post);

            // Assert
            Assert.IsFalse(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo(Messages.Error.BadRequest));
        }

        [Test]
        public async Task GetAllAsync_ReturnsAllPosts()
        {
            // Arrange
            var blogPosts = new List<Blog>
            {
                new Blog
                {
                    Id = 1,
                    UserId = Guid.NewGuid(),
                    Title = "Test Blog Post 1",
                    Content = "This is a test blog post 1",
                    CreatedAt = new DateTime(2022, 1, 1),
                    UpdatedAt = new DateTime(2022, 1, 1),
                    IsPublished = true
                },
                new Blog
                {
                    Id = 2,
                    UserId = Guid.NewGuid(),
                    Title = "Test Blog Post 2",
                    Content = "This is a test blog post 2",
                    CreatedAt = new DateTime(2022, 1, 2),
                    UpdatedAt = new DateTime(2022, 1, 2),
                    IsPublished = true
                }
            };

            var imagePosts = new List<Image>
            {
                new Image
                {
                    Id = 3,
                    UserId = Guid.NewGuid(),
                    Title = "Test Image Post 1",
                    Content = "This is a test image post 1",
                    CreatedAt = new DateTime(2022, 1, 3),
                    UpdatedAt = new DateTime(2022, 1, 3),
                    IsPublished = true
                },
                new Image
                {
                    Id = 4,
                    UserId = Guid.NewGuid(),
                    Title = "Test Image Post 2",
                    Content = "This is a test image post 2",
                    CreatedAt = new DateTime(2022, 1, 4),
                    UpdatedAt = new DateTime(2022, 1, 4),
                    IsPublished = true
                }
            };

            var videoPosts = new List<Video>
            {
                new Video
                {
                    Id = 5,
                    UserId = Guid.NewGuid(),
                    Title = "Test Video Post 1",
                    Content = "This is a test video post 1",
                    CreatedAt = new DateTime(2022, 1, 5),
                    UpdatedAt = new DateTime(2022, 1, 5),
                    IsPublished = true
                },
                new Video
                {
                    Id = 6,
                    UserId = Guid.NewGuid(),
                    Title = "Test Video Post 2",
                    Content = "This is a test video post 2",
                    CreatedAt = new DateTime(2022, 1, 6),
                    UpdatedAt = new DateTime(2022, 1, 6),
                    IsPublished = true
                }
            };

            _context.BlogPosts.AddRange(blogPosts);
            _context.ImagePosts.AddRange(imagePosts);
            _context.VideoPosts.AddRange(videoPosts);
            _context.SaveChanges();

            // Act
            var result = await _postService.GetAllAsync(true);

            // Assert
            Assert.That(result.Count, Is.EqualTo(6));
            Assert.That(result[0].Title, Is.EqualTo("Test Video Post 2"));
            Assert.That(result[1].Title, Is.EqualTo("Test Video Post 1"));
            Assert.That(result[2].Title, Is.EqualTo("Test Image Post 2"));
            Assert.That(result[3].Title, Is.EqualTo("Test Image Post 1"));
            Assert.That(result[4].Title, Is.EqualTo("Test Blog Post 2"));
            Assert.That(result[5].Title, Is.EqualTo("Test Blog Post 1"));
        }

        [Test]
        public async Task GetPostByIdAsync_WithExistingPost_ReturnsPostDto()
        {
            // Arrange
            var postId = 1;
            var blogPost = new Blog
            {
                Id = postId,
                UserId = Guid.NewGuid(),
                Title = "Test Blog Post",
                Content = "This is a test blog post",
                CreatedAt = new DateTime(2022, 1, 1),
                UpdatedAt = new DateTime(2022, 1, 1),
                IsPublished = true
            };
            _context.BlogPosts.Add(blogPost);
            _context.SaveChanges();

            // Act
            var result = await _postService.GetPostByIdAsync(postId);

            // Assert
            Assert.IsNotNull(result);
            Assert.That(result.Title, Is.EqualTo("Test Blog Post"));
            Assert.That(result.Content, Is.EqualTo("This is a test blog post"));
            Assert.That(result.CreatedAt, Is.EqualTo(new DateTime(2022, 1, 1)));
            Assert.That(result.UpdatedAt, Is.EqualTo(new DateTime(2022, 1, 1)));
            Assert.That(result.IsPublished, Is.True);
        }

        [Test]
        public async Task TogglePostPublishedStatusAsync_WithExistingPost_ReturnsSuccessResponse()
        {
            // Arrange
            var postId = 1;
            var blogPost = new Blog
            {
                Id = postId,
                UserId = Guid.NewGuid(),
                Title = "Test Blog Post",
                Content = "This is a test blog post",
                CreatedAt = new DateTime(2022, 1, 1),
                UpdatedAt = new DateTime(2022, 1, 1),
                IsPublished = true
            };
            _context.BlogPosts.Add(blogPost);
            _context.SaveChanges();

            // Act
            var response = await _postService.TogglePostPublishedStatusAsync<Blog>(postId);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo($"Post {postId} publish status: {blogPost.IsPublished}"));
        }
    }
}
