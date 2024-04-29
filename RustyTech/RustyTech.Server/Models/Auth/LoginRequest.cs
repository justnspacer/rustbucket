namespace RustyTech.Server.Models.Auth
{
    public class LoginRequest
    {
        public bool IsAuthenticated { get; set; }
        public UserDto? User { get; set; }
        public string? Token { get; set; }
        public string? Message { get; set; }
    }
}
