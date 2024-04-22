using System.ComponentModel.DataAnnotations;

namespace RustyTech.Server.Models.User
{
    public class UserRegister
    {
        public required string Email { get; set; }
        public required string Password { get; set; }
    }
}
