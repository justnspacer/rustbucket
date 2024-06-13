using RustyTech.Server.Models.User;
using RustyTech.Server.Services.Interfaces;
using RustyTech.Server.Constants;
using Microsoft.EntityFrameworkCore;
using RustyTech.Server.Data;
using RustyTech.Server.Services;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using System.Data.Entity;
using Moq;
using RustyTech.Server.Interfaces;

namespace RustyTech.Tests
{
    [TestFixture]
    public class Tests
    {
        private DbContextOptions<DataContext> _dataContextOptions;
        private DataContext _dataContext;
        private AuthService _authService;
        private Mock<IEmailService> _emailServiceMock;
        private Mock<IRoleService> _roleServiceMock;
        private Mock<IConfiguration> _configurationMock;
        private Mock<ILogger<IAuthService>> _loggerMock;

        [SetUp]
        public void Setup()
        {
            _dataContextOptions = new DbContextOptionsBuilder<DataContext>()
                .UseInMemoryDatabase(databaseName: "RustyTests")
                .Options;
            _dataContext = new DataContext(_dataContextOptions);

            _emailServiceMock = new Mock<IEmailService>();
            _roleServiceMock = new Mock<IRoleService>();
            _configurationMock = new Mock<IConfiguration>();
            _loggerMock = new Mock<ILogger<IAuthService>>();

            _authService = new AuthService(_emailServiceMock.Object, _roleServiceMock.Object, _configurationMock.Object, _loggerMock.Object, _dataContext);
        }

        [TearDown]
        public void TearDown()
        {
            _dataContext.Database.EnsureDeleted();
            _dataContext.Dispose();
        }

        [Test]
        public async Task RegisterAsync_ValidRequest_ReturnsSuccessResponse()
        {
            // Arrange
            UserRegister request = new UserRegister
            {
                Email = "something@hotmail.com",
                Password = "Password123!",
                ConfirmPassword = "Password123!",
                BirthYear = 1990,
            };

            // Act
            var response = await _authService.RegisterAsync(request);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo(Message.UserRegistered));

            var user = await _dataContext.Users.FirstOrDefaultAsync(u => u.Email == request.Email);
            Assert.IsNotNull(user);
            Assert.That(user.Email, Is.EqualTo(request.Email));
        }
    }
}