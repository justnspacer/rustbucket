using RustyTech.Server.Models.Dtos;

namespace RustyTech.Server.Models.Account
{
    public class AuthResponse : ResponseBase
    {
        public bool IsAuthenticated { get; set; }
        public GetUserRequest? User { get; set; }
    }
}
