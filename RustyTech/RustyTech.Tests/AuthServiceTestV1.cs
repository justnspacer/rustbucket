using RustyTech.Server.Models.User;
using RustyTech.Server.Services.Interfaces;
using RustyTech.Server.Constants;
using Microsoft.EntityFrameworkCore;
using RustyTech.Server.Data;
using RustyTech.Server.Services;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Moq;
using RustyTech.Server.Interfaces;
using RustyTech.Server.Models.Auth;
using Microsoft.AspNetCore.Identity.Data;

namespace RustyTech.Tests
{
    [TestFixture]
    public class AuthServiceTestV1
    {
        private DataContext _context;
        private IAuthService _authService;

        [SetUp]
        public void Setup()
        {
            // Mock dependencies
            var emailServiceMock = new Mock<IEmailService>();
            var roleServiceMock = new Mock<IRoleService>();
            var configurationMock = new Mock<IConfiguration>();
            var loggerMock = new Mock<ILogger<IAuthService>>();

            configurationMock.SetupGet(x => x[It.Is<string>(s => s == "Jwt:Key")]).Returns("J277A871-D6B8-4167-CDF3-D85F255901CE");
            configurationMock.SetupGet(x => x[It.Is<string>(s => s == "Jwt:Issuer")]).Returns("https://localhost:7164");
            configurationMock.SetupGet(x => x[It.Is<string>(s => s == "Jwt:Audience")]).Returns("https://localhost:7164");
            configurationMock.SetupGet(x => x[It.Is<string>(s => s == "Jwt:ExpiresInMinutes")]).Returns("30");

            // Create in-memory database
            var options = new DbContextOptionsBuilder<DataContext>()
                .UseInMemoryDatabase(databaseName: "TestDatabase")
                .Options;
            _context = new DataContext(options);

            // Initialize AuthService with mocked dependencies and in-memory database
            _authService = new AuthService(emailServiceMock.Object, roleServiceMock.Object, configurationMock.Object, loggerMock.Object, _context);
        }

        [TearDown]
        public void TearDown()
        {
            _context.Database.EnsureDeleted();
            _context.Dispose();
        }

        [Test]
        public async Task RegisterAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var request = new UserRegister
            {
                Email = "test@example.com",
                Password = "Test123!",
                ConfirmPassword = "Test123!",
                BirthYear = 1990
            };

            // Act
            var response = await _authService.RegisterAsync(request);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo(Messages.Info.UserRegistered));
        }

        [Test]
        public async Task LoginAsync_SuccessfulRequest_ReturnsLoginResponseWithAuthenticatedUser()
        {
            // Arrange
            var request = new UserLogin
            {
                Email = "test@example.com",
                Password = "Test123!"
            };
            _authService.CreatePasswordHash(request.Password, out byte[] hash, out byte[] salt);
            var user = new User
            {
                Email = request.Email,
                PasswordHash = hash,
                PasswordSalt = salt,
                VerifiedAt = DateTime.UtcNow,
            };

            _context.Users.Add(user);
            _context.SaveChanges();

            // Act
            var response = await _authService.LoginAsync(request);

            // Assert
            Assert.IsTrue(response.IsAuthenticated);
            Assert.IsTrue(response.IsSuccess);
            Assert.IsNotNull(response.User);
            Assert.That(response.User.Email, Is.EqualTo(request.Email));
            Assert.IsNotNull(response.Token);
        }

        [Test]
        public async Task VerifyEmailAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccess()
        {
            // Arrange
            var request = new ConfirmEmailRequest
            {
                Token = "valid_token"
            };
            var user = new User
            {
                VerificationToken = "valid_token"
            };
            _context.Users.Add(user);
            _context.SaveChanges();

            // Act
            var response = await _authService.VerifyEmailAsync(request);

            // Assert
            Assert.IsTrue(response.IsSuccess);
        }

        [Test]
        public void VerifyJwtToken_ValidToken_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var token = _authService.GenerateJwtToken(Guid.NewGuid(), "testemail@example.com", new List<string>() { "Manager" });

            // Act
            var response = _authService.VerifyJwtToken(token);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo(Messages.Token.Valid));
        }

        [Test]
        public void ResendEmailAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var email = "test@example.com";
            var user = new User
            {
                Email = email,
                VerificationToken = "valid_token"
            };
            _context.Users.Add(user);
            _context.SaveChanges();

            // Act
            var response = _authService.ResendEmailAsync(email);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo(Messages.Info.ResendEmail));
        }

        [Test]
        public async Task ForgotPasswordAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var email = "test@example.com";
            var user = new User
            {
                Email = email
            };
            _context.Users.Add(user);
            _context.SaveChanges();

            // Act
            var response = await _authService.ForgotPasswordAsync(email);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo(Messages.Info.UserPasswordReset));
        }


        [Test]
        public async Task ResetPasswordAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var request = new ResetPasswordRequest
            {
                Email = "test123@example.com",
                ResetCode = "valid_token",
                NewPassword = "NewPassword123!",
            };

            var user = new User
            {
                Id = new Guid(),
                Email = "test123@example.com",
                PasswordResetToken = "valid_token"
            };
            _context.Users.Add(user);
            _context.SaveChanges();


            // Act
            var response = await _authService.ResetPasswordAsync(request);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo(Messages.Info.UserPasswordReset));
        }

        [Test]
        public async Task UpdateUserAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var userId = Guid.NewGuid();
            var userDto = new UserUpdateDto
            {
                UserId = userId,
                UserName = "John",
                Email = "john.doe@example.com",
                BirthYear = 1990
            };
            var user = new User
            {
                Id = userId,
                UserName = "Johnner",
                Email = "johnner.doer@example.com",
                BirthYear = 1980
            };
            _context.Users.Add(user);
            _context.SaveChanges();

            // Act
            var response = await _authService.UpdateUserAsync(userDto);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo("User updated, email reverifcation required"));

            var updatedUser = _context.Users.FirstOrDefault(u => u.Id == userId);
            Assert.IsNotNull(updatedUser);
            Assert.That(updatedUser.UserName, Is.EqualTo(userDto.UserName));
            Assert.That(updatedUser.Email, Is.EqualTo(userDto.Email));
            Assert.That(updatedUser.BirthYear, Is.EqualTo(userDto.BirthYear));
        }
        [Test]
        public async Task EnableTwoFactorAuthenticationAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var userId = Guid.NewGuid();
            var user = new User { Id = userId };
            _context.Users.Add(user);
            _context.SaveChanges();

            // Act
            var response = await _authService.EnableTwoFactorAuthenticationAsync(userId);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo("Two factor enabled"));

            var updatedUser = _context.Users.FirstOrDefault(u => u.Id == userId);
            Assert.IsNotNull(updatedUser);
            Assert.IsTrue(updatedUser.TwoFactorEnabled);
        }

        [Test]
        public void GetInfoAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var userId = Guid.NewGuid();
            var user = new User { Id = userId, TwoFactorEnabled = true };
            _context.Users.Add(user);
            _context.SaveChanges();

            // Act
            var response = _authService.GetInfoAsync(userId);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo("Two factor enabled? True"));
        }

        [Test]
        public void LogoutAsync_SuccessfulRequest_ReturnsLoginResponseWithLoggedOutUser()
        {
            // Arrange
            var userId = Guid.NewGuid();
            var user = new User { Id = userId };
            _context.Users.Add(user);
            _context.SaveChanges();

            // Act
            var response = _authService.LogoutAsync();

            // Assert
            Assert.IsFalse(response.IsAuthenticated);
            Assert.IsTrue(response.IsSuccess);
            Assert.IsNull(response.User);
            Assert.IsNull(response.Token);
        }
    }
}