﻿using AutoMapper;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Moq;
using RustyTech.Server.Constants;
using RustyTech.Server.Data;
using RustyTech.Server.AutoMapper;
using RustyTech.Server.Services;
using RustyTech.Server.Services.Interfaces;
using RustyTech.Server.Models.Posts;
using RustyTech.Server.Models;
using RustyTech.Server.Models.Dtos;
using Ganss.Xss;
using Microsoft.AspNetCore.Identity;

namespace RustyTech.Tests
{
    public class PostServiceTestV1
    {
        private DataContext _context;
        private IMapper _mapper;
        private IUserService _userService;
        private IPostService _postService;
        private IImageService _imageService;
        private IVideoService _videoService;
        private IKeywordService _keywordService;

        [SetUp]
        public void Setup()
        {
            var loggerMock = new Mock<ILogger<PostService>>();
            var sanitizerMock = new Mock<HtmlSanitizer>();
            var userManagerMock = new Mock<UserManager<User>>();
            var signInManagerMock = new Mock<SignInManager<User>>();

            var options = new DbContextOptionsBuilder<DataContext>()
                .UseInMemoryDatabase(databaseName: "TestDatabase")
                .Options;

            _context = new DataContext(options);
            _mapper = new MapperConfiguration(cfg => cfg.AddProfile(new MappingProfile())).CreateMapper();
            _userService = new UserService(userManagerMock.Object, _mapper, new Logger<UserService>(new LoggerFactory()));
            _postService = new PostService(_context, _mapper, _userService, loggerMock.Object, _imageService, _videoService, _keywordService);
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
            var post = new CreateBlogRequest()
            {
                Id = 1,
                UserId = Guid.NewGuid().ToString(),
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
            var response = await _postService.CreateBlogPostAsync(post);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo(Messages.Info.PostCreated));
        }

        [Test]
        public async Task GetAllAsync_ReturnsAllPosts()
        {
            // Arrange
            var user = new User
            {
                Id = Guid.NewGuid().ToString(),
                UserName = "testuser",
                VerifiedAt = new DateTime(7775, 3, 09)
            };
            var blogPosts = new List<BlogPost>
            {
                new BlogPost
                {
                    Id = 1,
                    UserId = user.Id.ToString(),
                    User = user,
                    Title = "Test Blog Post 1",
                    Content = "This is a test blog post 1",
                    CreatedAt = new DateTime(2022, 1, 1),
                    UpdatedAt = new DateTime(2022, 1, 1),
                    IsPublished = true
                },
                new BlogPost
                {
                    Id = 2,
                    UserId = user.Id.ToString(),
                    User = user,
                    Title = "Test Blog Post 2",
                    Content = "This is a test blog post 2",
                    CreatedAt = new DateTime(2022, 1, 2),
                    UpdatedAt = new DateTime(2022, 1, 2),
                    IsPublished = true
                }
            };

            var imagePosts = new List<ImagePost>
            {
                new ImagePost
                {
                    Id = 3,
                    UserId = user.Id.ToString(),
                    User = user,
                    Title = "Test Image Post 1",
                    Content = "This is a test image post 1",
                    CreatedAt = new DateTime(2022, 1, 3),
                    UpdatedAt = new DateTime(2022, 1, 3),
                    IsPublished = true,
                    ImageFile = "test.jpg"
                },
                new ImagePost
                {
                    Id = 4,
                    UserId = user.Id.ToString(),
                    User = user,
                    Title = "Test Image Post 2",
                    Content = "This is a test image post 2",
                    CreatedAt = new DateTime(2022, 1, 4),
                    UpdatedAt = new DateTime(2022, 1, 4),
                    IsPublished = true,
                    ImageFile = "test.jpg"

                }
            };

            var videoPosts = new List<VideoPost>
            {
                new VideoPost
                {
                    Id = 5,
                    UserId = user.Id.ToString(),
                    User = user,
                    Title = "Test Video Post 1",
                    Content = "This is a test video post 1",
                    CreatedAt = new DateTime(2022, 1, 5),
                    UpdatedAt = new DateTime(2022, 1, 5),
                    IsPublished = true,
                    VideoFile = "test.mp4",
                    ImageFile = "test.png"
                },
                new VideoPost
                {
                    Id = 6,
                    UserId = user.Id.ToString(),
                    User = user,
                    Title = "Test Video Post 2",
                    Content = "This is a test video post 2",
                    CreatedAt = new DateTime(2022, 1, 6),
                    UpdatedAt = new DateTime(2022, 1, 6),
                    IsPublished = true,
                    VideoFile = "test.mp4",
                    ImageFile = "test.png"
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
            var user = new User
            {
                Id = Guid.NewGuid().ToString(),
                UserName = "testuser",
                VerifiedAt = new DateTime(7775, 3, 09)
            };
            var postId = 1;
            var blogPost = new BlogPost
            {
                Id = postId,
                UserId = user.Id.ToString(),
                User = user,
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
            var user = new User
            {
                Id = Guid.NewGuid().ToString(),
                UserName = "testuser",
                VerifiedAt = new DateTime(7775, 3, 09)
            };
            var postId = 1;
            var blogPost = new BlogPost
            {
                Id = postId,
                UserId = user.Id.ToString(),
                User = user,
                Title = "Test Blog Post",
                Content = "This is a test blog post",
                CreatedAt = new DateTime(2022, 1, 1),
                UpdatedAt = new DateTime(2022, 1, 1),
                IsPublished = true
            };
            _context.BlogPosts.Add(blogPost);
            _context.SaveChanges();

            // Act
            var response = await _postService.TogglePostPublishedStatusAsync<BlogPost>(postId);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo($"Post {postId} publish status: {blogPost.IsPublished}"));
        }
    }
}
