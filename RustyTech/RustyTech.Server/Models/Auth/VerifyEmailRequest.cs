namespace RustyTech.Server.Models.Auth
{
    public class VerifyEmailRequest
    {
        public string? Id { get; set; }
        public string? Token { get; set; }
    }
}
