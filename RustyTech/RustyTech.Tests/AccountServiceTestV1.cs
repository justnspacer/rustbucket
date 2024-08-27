using RustyTech.Server.Services.Interfaces;
using RustyTech.Server.Constants;
using RustyTech.Server.Services;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Moq;
using RustyTech.Server.Interfaces;
using RustyTech.Server.Models.Account;
using Microsoft.AspNetCore.Identity.Data;
using RustyTech.Server.Models;
using RustyTech.Server.Models.Dtos;
using Microsoft.AspNetCore.Identity;

namespace RustyTech.Tests
{
    [TestFixture]
    public class AccountServiceTestV1
    {
        private IAccountService _accountService;

        [SetUp]
        public void Setup()
        {
            var emailServiceMock = new Mock<IEmailService>();
            var roleServiceMock = new Mock<IRoleService>();
            var configurationMock = new Mock<IConfiguration>();
            var loggerMock = new Mock<ILogger<IAccountService>>();
            var userManagerMock = new Mock<UserManager<User>>();
            var signInManagerMock = new Mock<SignInManager<User>>();
            var imageServiceMock = new Mock<IImageService>();

            configurationMock.SetupGet(x => x[It.Is<string>(s => s == "Jwt:Key")]).Returns("J277A871-CDF3-D6B8-4167-D6B8-D85F255901CE");
            configurationMock.SetupGet(x => x[It.Is<string>(s => s == "Jwt:Issuer")]).Returns("https://testhost:7111");
            configurationMock.SetupGet(x => x[It.Is<string>(s => s == "Jwt:Audience")]).Returns("https://testhost:7111");
            configurationMock.SetupGet(x => x[It.Is<string>(s => s == "Jwt:ExpiresInMinutes")]).Returns("30");

            _accountService = new AccountService(userManagerMock.Object, signInManagerMock.Object, emailServiceMock.Object, roleServiceMock.Object, configurationMock.Object, loggerMock.Object, imageServiceMock.Object);
        }

        [Test]
        public async Task RegisterAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var request = new CustomRegisterRequest()
            {
                UserName = "Test",
                Email = "test@example.com",
                Password = "Test123!",
                BirthYear = 1990
            };

            // Act
            var response = await _accountService.Register(request);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo(Messages.Info.UserRegistered));
        }

        [Test]
        public async Task RegisterAsync_PasswordMismatch_ReturnsResponseBaseWithErrorMessage()
        {
            // Arrange
            var request = new CustomRegisterRequest()
            {
                UserName = "Test",
                Email = "request@example.com",
                Password = "Password123",
            };

            // Act
            var response = await _accountService.Register(request);

            // Assert
            Assert.IsFalse(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo(Messages.Error.PasswordMismatch));
        }

        [Test]
        public async Task RegisterAsync_BadEmail_ReturnsResponseBaseWithErrorMessage()
        {
            // Arrange
            var request = new CustomRegisterRequest()
            {
                UserName = "Test",
                Email = "request@example.",
                Password = "Password123",
            };

            // Act
            var response = await _accountService.Register(request);

            // Assert
            Assert.That(response.IsSuccess, Is.False);
            Assert.That(response.Message, Is.EqualTo(Messages.Error.InvalidEmail));
        }

        [Test]
        public async Task LoginAsync_SuccessfulRequest_ReturnsLoginResponseWithAuthenticatedUser()
        {
            // Arrange
            var request = new CustomLoginRequest()
            {
                Email = "test@example.com",
                Password = "Test123!"
            };

            var user = new User
            {
                Email = request.Email,
                PasswordHash = "Test123!",
                VerifiedAt = DateTime.UtcNow,
            };

            // Act
            var response = await _accountService.Login(request);

            // Assert
            Assert.IsTrue(response.IsAuthenticated);
            Assert.That(response.IsSuccess, Is.True);
            Assert.IsNotNull(response.User);
            Assert.That(response.User.Email, Is.EqualTo(request.Email));
        }

        [Test]
        public async Task VerifyEmailAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccess()
        {
            // Arrange
            var request = new VerifyEmailRequest
            {
                Token = "valid_token"
            };
            var user = new User
            {
                VerificationToken = "valid_token"
            };

            // Act
            var response = await _accountService.VerifyEmail(request);

            // Assert
            Assert.That(response.IsSuccess, Is.True);
        }

        [Test]
        public async Task ResendEmailAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var email = "test@example.com";
            var user = new User
            {
                Email = email,
                VerificationToken = "valid_token"
            };

            // Act
            var response = await _accountService.ResendEmail(email);

            // Assert
            Assert.Multiple(() =>
            {
                Assert.That(response.IsSuccess, Is.True);
                Assert.That(response.Message, Is.EqualTo(Messages.Info.ResendEmail));
            });
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

            // Act
            var response = await _accountService.ForgotPassword(email);

            // Assert
            Assert.Multiple(() =>
            {
                Assert.That(response.IsSuccess, Is.True);
                Assert.That(response.Message, Is.EqualTo(Messages.Info.UserPasswordReset));
            });
        }

        [Test]
        public async Task ResetPasswordAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var request = new CustomResetPasswordRequest
            {
                Email = "test123@example.com",
                ResetCode = "valid_token",
                NewPassword = "NewPassword123!",
            };

            var user = new User
            {
                Id = Guid.NewGuid().ToString(),
                Email = "test123@example.com",
                PasswordResetToken = "valid_token"
            };


            // Act
            var response = await _accountService.ResetPassword(request);

            // Assert
            Assert.Multiple(() =>
            {
                Assert.That(response.IsSuccess, Is.True);
                Assert.That(response.Message, Is.EqualTo(Messages.Info.UserPasswordReset));
            });
        }

        [Test]
        public async Task UpdateUserAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var userId = Guid.NewGuid().ToString();
            var userDto = new UpdateUserRequest
            {
                UserId = userId,
                UserName = "John",
                Email = "john.doe@example.com",
                BirthYear = 1990
            };
            var user = new User
            {
                Id = Guid.NewGuid().ToString(),
                UserName = "Johnner",
                Email = "johnner.doer@example.com",
                BirthYear = 1980
            };

            // Act
            var response = await _accountService.UpdateUser(userDto);

            // Assert
            Assert.Multiple(() =>
            {
                
                Assert.That(response.IsSuccess, Is.True);
                Assert.That(response.Message, Is.EqualTo("User updated, email reverifcation required"));
            });          
        }

        [Test]
        public async Task EnableTwoFactorAuthenticationAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var userId = Guid.NewGuid().ToString();
            var user = new User { Id = userId, TwoFactorEnabled = false };

            // Act
            var response = await _accountService.ToggleTwoFactorAuth(userId);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo("Two factor enabled"));
        }

        [Test]
        public async Task GetInfoAsync_SuccessfulRequest_ReturnsResponseBaseWithSuccessMessage()
        {
            // Arrange
            var userId = Guid.NewGuid().ToString();
            var user = new User { Id = userId, TwoFactorEnabled = true };

            // Act
            var response = await _accountService.GetInfo(userId);

            // Assert
            Assert.That(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo("Two factor enabled? True"));
        }

        [Test]
        public async Task LogoutAsync_SuccessfulRequest_ReturnsLoginResponseWithLoggedOutUser()
        {
            // Arrange
            var userId = Guid.NewGuid().ToString();
            var user = new User { Id = userId };

            // Act
            var response = await _accountService.Logout();

            // Assert
            Assert.That(response.IsSuccess);
        }
    }
}