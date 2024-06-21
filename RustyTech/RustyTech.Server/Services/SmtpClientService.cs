using MailKit.Net.Smtp;
using MailKit.Security;
using MimeKit;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Services
{
    public class SmtpClientService : ISmtpClientService
    {
        private readonly SmtpClient _smtpClient = new SmtpClient();

        public async Task ConnectAsync(string? host, int port, SecureSocketOptions options)
        {
            await _smtpClient.ConnectAsync(host, port, options);
        }

        public async Task AuthenticateAsync(string? username, string? password)
        {
            await _smtpClient.AuthenticateAsync(username, password);
        }

        public async Task SendAsync(MimeMessage message)
        {
            await _smtpClient.SendAsync(message);
        }

        public async Task DisconnectAsync(bool quit)
        {
            await _smtpClient.DisconnectAsync(quit);
        }

        public void Dispose()
        {
            _smtpClient.Dispose();
        }
    }
}
