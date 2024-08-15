using Microsoft.AspNetCore.Identity.UI.Services;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Services
{
    public class EmailSender : IEmailSender
    {
        private readonly IEmailService _emailService;

        public EmailSender(IEmailService emailService)
        {
            _emailService = emailService;
        }
        public Task SendEmailAsync(string email, string subject, string htmlMessage)
        {
            var request = new EmailRequest { To = email, Subject = subject, Body = htmlMessage };
            _emailService.SendEmailAsync(request);
            return Task.CompletedTask;
        }
    }
}
