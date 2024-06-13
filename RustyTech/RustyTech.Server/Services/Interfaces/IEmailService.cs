using RustyTech.Server.Models.Auth;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IEmailService
    {
        Task SendEmailAsync(EmailRequest request);
    }
}
