using System.ComponentModel.DataAnnotations;

namespace RustyTech.Server.Models.Auth
{
    public class LoginRequest
    {
        [Required, EmailAddress]
        public required string Email { get; set; }
        [Required, MinLength(6, ErrorMessage = "Please enter at least 6 characters")]
        public required string Password { get; set; }
    }
}
