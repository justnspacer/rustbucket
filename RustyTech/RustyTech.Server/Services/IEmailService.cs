using RustyTech.Server.Models.Auth;

namespace RustyTech.Server.Services
{
    public interface IEmailService
    {
        Task SendEmailAsync(EmailRequest request);
    }
}
