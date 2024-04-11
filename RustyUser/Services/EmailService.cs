using MailKit.Security;
using MimeKit.Text;
using MimeKit;
using MailKit.Net.Smtp;
using RustyUser.Models.Auth;

namespace RustyUser.Services
{
    public class EmailService : IEmailService
    {
        private readonly IConfiguration _configuration;
        private readonly int _smtpPort = 587;
        private readonly SecureSocketOptions _secureSocketOptions = SecureSocketOptions.StartTls;

        public EmailService(IConfiguration configuration)
        {
            _configuration = configuration;
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

                using var smtp = new SmtpClient();
                await smtp.ConnectAsync(_configuration["Email:Host"], _smtpPort, _secureSocketOptions);
                await smtp.AuthenticateAsync(_configuration["Email:Username"], _configuration["Email:Password"]);
                await smtp.SendAsync(email);
                await smtp.DisconnectAsync(true);
                Console.WriteLine("Email sent successfully");
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error sending email: " + ex.Message);
            }
        }
    }
}
