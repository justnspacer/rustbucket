using MailKit.Security;
using MimeKit;

namespace RustyTech.Server.Services.Interfaces
{
    public interface ISmtpClientService
    {
        Task ConnectAsync(string host, int port, SecureSocketOptions options);
        Task AuthenticateAsync(string userName, string password);
        Task SendAsync(MimeMessage message);
        Task DisconnectAsync(bool quit);
        void Dispose();
    }
}
