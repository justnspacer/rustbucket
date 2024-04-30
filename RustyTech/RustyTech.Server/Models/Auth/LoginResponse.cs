using System.Text.Json.Serialization;

namespace RustyTech.Server.Models.Auth
{
    public class LoginResponse : ResponseBase
    {
        public bool IsAuthenticated { get; set; }
        public UserDto? User { get; set; }
        public string? Token { get; set; }
    }
}
