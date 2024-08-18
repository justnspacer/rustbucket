using Microsoft.AspNetCore.Identity;
using RustyTech.Server.Models.Account;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Services
{
    public class EmailSender : IEmailSender<User>
    {
        private readonly IEmailService _emailService;

        public EmailSender(IEmailService emailService)
        {
            _emailService = emailService;
        }

        public Task SendConfirmationLinkAsync(User user, string email, string confirmationLink)
        {
            var request = new EmailRequest { To = email, Subject = "Confirm Email", Body = confirmationLink };
            _emailService.SendEmailAsync(request);
            return Task.CompletedTask;
        }

        public Task SendPasswordResetCodeAsync(User user, string email, string resetCode)
        {
            var request = new EmailRequest { To = email, Subject = "Password Reset Code", Body = resetCode };
            _emailService.SendEmailAsync(request);
            return Task.CompletedTask;
        }

        public Task SendPasswordResetLinkAsync(User user, string email, string resetLink)
        {
            var request = new EmailRequest { To = email, Subject = "Password Reset Link", Body = resetLink };
            _emailService.SendEmailAsync(request);
            return Task.CompletedTask;
        }

        public Task SendEmailAsync(string email, string subject, string htmlMessage)
        {
            var request = new EmailRequest { To = email, Subject = subject, Body = htmlMessage };
            _emailService.SendEmailAsync(request);
            return Task.CompletedTask;
        }
    }
}
