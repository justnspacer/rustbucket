using RustyTech.Server.Models.Account;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IEmailService
    {
        Task SendEmailAsync(EmailRequest request);
    }
}
