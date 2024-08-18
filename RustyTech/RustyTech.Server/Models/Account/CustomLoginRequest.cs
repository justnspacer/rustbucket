namespace RustyTech.Server.Models.Account
{
    public class CustomLoginRequest
    {
        public required string Email { get; set; }
        public required string Password { get; set; }
        public bool RememberMe { get; set; }
    }
}
