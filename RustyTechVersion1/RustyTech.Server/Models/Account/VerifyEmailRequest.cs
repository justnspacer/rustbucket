namespace RustyTech.Server.Models.Account
{
    public class VerifyEmailRequest
    {
        public string? Id { get; set; }
        public string? Token { get; set; }
    }
}
