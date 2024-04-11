using RustyUser.Models.Auth;

namespace RustyUser.Services
{
    public interface IEmailService
    {
        Task SendEmailAsync(EmailRequest request);
    }
}
