using MailKit.Security;
using MailKit.Net.Smtp;
using MimeKit.Text;
using MimeKit;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Services
{
    public class EmailService : IEmailService
    {
        private readonly IConfiguration _configuration;
        private readonly ISmtpClientService _smtpClientService;
        private readonly int _smtpPort = 587;
        private readonly SecureSocketOptions _secureSocketOptions = SecureSocketOptions.StartTls;

        public EmailService(IConfiguration configuration, ISmtpClientService smtpClientService)
        {
            _configuration = configuration;
            _smtpClientService = smtpClientService;
        }

        public async Task SendEmailAsync(EmailRequest request)
        {
            try
            {
                var email = new MimeMessage();
                email.From.Add(MailboxAddress.Parse(_configuration["Email:Username"]));
                email.To.Add(MailboxAddress.Parse(request.To));
                email.Subject = request.Subject;
                email.Body = new TextPart(TextFormat.Html) { Text = request.Body };

                await _smtpClientService.ConnectAsync(_configuration["Email:Host"], _smtpPort, _secureSocketOptions);
                await _smtpClientService.AuthenticateAsync(_configuration["Email:Username"], _configuration["Email:Password"]);
                await _smtpClientService.SendAsync(email);
                await _smtpClientService.DisconnectAsync(true);
                _smtpClientService.Dispose();
                Console.WriteLine("Email sent successfully");
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error sending email: " + ex.Message);
            }
        }
    }
}
