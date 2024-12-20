﻿using MailKit.Security;
using Microsoft.Extensions.Configuration;
using MimeKit;
using Moq;
using RustyTech.Server.Models.Account;
using RustyTech.Server.Services;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Tests
{
    [TestFixture]
    public class EmailServiceTestV1
    {
        private IEmailService _emailService;
        private Mock<ISmtpClientService> _smtpClientMock;


        [SetUp]
        public void Setup()
        {
            var configMock = new Mock<IConfiguration>();
            configMock.SetupGet(x => x["Email:Username"]).Returns("test@example.com");
            configMock.SetupGet(x => x["Email:Host"]).Returns("smtp.example.com");
            configMock.SetupGet(x => x["Email:Password"]).Returns("password");

            _smtpClientMock = new Mock<ISmtpClientService>();
            _smtpClientMock.Setup(smtp => smtp.ConnectAsync("smtp.example.com", 587, SecureSocketOptions.StartTls)).Returns(Task.CompletedTask);
            _smtpClientMock.Setup(smtp => smtp.AuthenticateAsync("test@example.com", "password")).Returns(Task.CompletedTask);
            _smtpClientMock.Setup(smtp => smtp.SendAsync(It.IsAny<MimeMessage>())).Returns(Task.CompletedTask);
            _smtpClientMock.Setup(smtp => smtp.DisconnectAsync(true)).Returns(Task.CompletedTask);

            _emailService = new EmailService(configMock.Object, _smtpClientMock.Object);
        }

        [Test]
        public async Task SendEmailAsync_ShouldSendEmail()
        {
            // Arrange
            var emailRequest = new EmailRequest
            {
                To = "recipient@example.com",
                Subject = "Test Email",
                Body = "<h1>This is a test email</h1>"
            };

            // Act
            await _emailService.SendEmailAsync(emailRequest);

            // Assert
            _smtpClientMock.Verify(smtp => smtp.ConnectAsync("smtp.example.com", 587, SecureSocketOptions.StartTls), Times.Once);
            _smtpClientMock.Verify(smtp => smtp.AuthenticateAsync("test@example.com", "password"), Times.Once);
            _smtpClientMock.Verify(smtp => smtp.SendAsync(It.Is<MimeMessage>(m => m.Subject == "Test Email" && m.To.ToString() == "recipient@example.com")), Times.Once);
            _smtpClientMock.Verify(smtp => smtp.DisconnectAsync(true), Times.Once);
        }
    }
}
