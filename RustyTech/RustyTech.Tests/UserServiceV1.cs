using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Moq;
using RustyTech.Server.Constants;
using RustyTech.Server.Data;
using RustyTech.Server.Models.User;
using RustyTech.Server.Services;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Tests
{
    [TestFixture]
    public class UserServiceV1
    {
        private DataContext _context;
        private IUserService _userService;

        [SetUp]
        public void Setup()
        {
            var loggerMock = new Mock<ILogger<IUserService>>();

            // Create in-memory database
            var options = new DbContextOptionsBuilder<DataContext>()
                .UseInMemoryDatabase(databaseName: "TestDatabase")
                .Options;
            _context = new DataContext(options);

            _userService = new UserService(_context, loggerMock.Object);
        }

        [TearDown]
        public void TearDown()
        {
            _context.Database.EnsureDeleted();
            _context.Dispose();
        }

        [Test]
        public async Task GetAllAsync_ShouldReturnAllUsers_WhenActiveIsTrue()
        {
            // Arrange
            var user1 = new User { Id = Guid.NewGuid(), Email = "user1@example.com", EmailConfirmed = true };
            var user2 = new User { Id = Guid.NewGuid(), Email = "user2@example.com", EmailConfirmed = true };
            var user3 = new User { Id = Guid.NewGuid(), Email = "user3@example.com", EmailConfirmed = false };
            _context.Users.AddRange(user1, user2, user3);
            await _context.SaveChangesAsync();

            // Act
            var result = await _userService.GetAllAsync(active: true);

            // Assert
            Assert.That(result.Count, Is.EqualTo(2));
            Assert.IsTrue(result.Any(u => u.Id == user1.Id && u.Email == user1.Email));
            Assert.IsTrue(result.Any(u => u.Id == user2.Id && u.Email == user2.Email));
        }

        [Test]
        public async Task GetAllAsync_ShouldReturnAllUsers_WhenActiveIsFalse()
        {
            // Arrange
            var user1 = new User { Id = Guid.NewGuid(), Email = "user1@example.com", EmailConfirmed = true };
            var user2 = new User { Id = Guid.NewGuid(), Email = "user2@example.com", EmailConfirmed = true };
            var user3 = new User { Id = Guid.NewGuid(), Email = "user3@example.com", EmailConfirmed = false };
            _context.Users.AddRange(user1, user2, user3);
            await _context.SaveChangesAsync();

            // Act
            var result = await _userService.GetAllAsync(active: false);

            // Assert
            Assert.That(result.Count, Is.EqualTo(3));
            Assert.IsTrue(result.Any(u => u.Id == user1.Id && u.Email == user1.Email));
            Assert.IsTrue(result.Any(u => u.Id == user2.Id && u.Email == user2.Email));
            Assert.IsTrue(result.Any(u => u.Id == user3.Id && u.Email == user3.Email));
        }

        [Test]
        public async Task GetByIdAsync_ShouldReturnUserDto_WhenIdIsValid()
        {
            // Arrange
            var userId = Guid.NewGuid();
            var user = new User { Id = userId, Email = "user@example.com", EmailConfirmed = true };
            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            // Act
            var result = await _userService.GetByIdAsync(userId);

            // Assert
            Assert.IsNotNull(result);
            Assert.That(result.Id, Is.EqualTo(userId));
            Assert.That(result.Email, Is.EqualTo(user.Email));
        }

        [Test]
        public async Task GetByIdAsync_ShouldReturnNull_WhenIdIsEmpty()
        {
            // Act
            var result = await _userService.GetByIdAsync(Guid.Empty);

            // Assert
            Assert.IsNull(result);
        }

        [Test]
        public async Task GetByIdAsync_ShouldReturnNull_WhenUserNotFound()
        {
            // Arrange
            var userId = Guid.NewGuid();

            // Act
            var result = await _userService.GetByIdAsync(userId);

            // Assert
            Assert.IsNull(result);
        }

        [Test]
        public async Task FindByEmailAsync_ShouldReturnUserDto_WhenEmailIsValid()
        {
            // Arrange
            var userEmail = "user@example.com";
            var user = new User { Id = Guid.NewGuid(), Email = userEmail, EmailConfirmed = true };
            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            // Act
            var result = await _userService.FindByEmailAsync(userEmail);

            // Assert
            Assert.IsNotNull(result);
            Assert.That(result.Id, Is.EqualTo(user.Id));
            Assert.That(result.Email, Is.EqualTo(userEmail));

        }

        [Test]
        public async Task FindByEmailAsync_ShouldReturnNull_WhenEmailIsEmpty()
        {
            // Act
            var result = await _userService.FindByEmailAsync(string.Empty);

            // Assert
            Assert.IsNull(result);
        }

        [Test]
        public async Task FindByEmailAsync_ShouldReturnNull_WhenUserNotFound()
        {
            // Arrange
            var userEmail = "user@example.com";

            // Act
            var result = await _userService.FindByEmailAsync(userEmail);

            // Assert
            Assert.IsNull(result);
        }

        [Test]
        public async Task DeleteAsync_ShouldReturnUserDeletedMessage_WhenIdIsValid()
        {
            // Arrange
            var userId = Guid.NewGuid();
            var user = new User { Id = userId, Email = "user@example.com", EmailConfirmed = true };
            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            // Act
            var result = await _userService.DeleteAsync(userId);

            // Assert
            Assert.That(result, Is.EqualTo(Messages.Info.UserDeleted));
            Assert.IsNull(await _context.Users.FindAsync(userId));
        }

        [Test]
        public async Task DeleteAsync_ShouldReturnIdRequiredMessage_WhenIdIsEmpty()
        {
            // Act
            var result = await _userService.DeleteAsync(Guid.Empty);

            // Assert
            Assert.That(result, Is.EqualTo(Messages.IdRequired));
        }

        [Test]
        public async Task DeleteAsync_ShouldReturnUserNotFoundMessage_WhenUserNotFound()
        {
            // Arrange
            var userId = Guid.NewGuid();

            // Act
            var result = await _userService.DeleteAsync(userId);

            // Assert
            Assert.That(result, Is.EqualTo(Messages.Info.UserNotFound));
        }
    }
}
