using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Moq;
using RustyTech.Server.Data;
using RustyTech.Server.Models.User;
using RustyTech.Server.Services;
using System.Collections.Generic;
using System.Linq;
using Microsoft.EntityFrameworkCore;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Tests
{
    [TestFixture]
    public class Tests
    {
        private AuthService _authService;
        private Mock<DataContext> _contextMock;

        [SetUp]
        public void Setup()
        {
            _contextMock = new Mock<DataContext>();
            _authService = new AuthService(Mock.Of<IEmailService>(), Mock.Of<IConfiguration>(),
                Mock.Of<ILogger<AuthService>>(), _contextMock.Object, Mock.Of<RoleService>());
        }

        [Test]
        public async Task RegisterAsync_UserDoesNotExist_ReturnsSuccessResponse()
        {
            // Arrange
            var request = new UserRegister
            {
                Email = "test@example.com",
                Password = "Test123",
                ConfirmPassword = "Test123",
                BirthYear = 0
            };

            // Act
            var response = await _authService.RegisterAsync(request);

            // Assert
            Assert.IsTrue(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo("User registered, email confirmation sent"));
        }

        [Test]
        public async Task RegisterAsync_UserAlreadyExists_ReturnsErrorResponse()
        {
            // Arrange
            var request = new UserRegister
            {
                Email = "existing@example.com",
                Password = "Test123",
                ConfirmPassword = "Test123",
                BirthYear = 1990
            };            

            // Act
            var response = await _authService.RegisterAsync(request);

            // Assert
            Assert.IsFalse(response.IsSuccess);
            Assert.That(response.Message, Is.EqualTo("User already exists"));
        }
    }
}