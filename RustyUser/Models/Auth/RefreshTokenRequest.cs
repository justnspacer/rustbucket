namespace RustyUser.Models.Auth
{
    public class RefreshTokenRequest
    {
        public required string Email { get; set; }
        public required string Password { get; set; }
    }
}
