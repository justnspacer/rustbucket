using System.ComponentModel.DataAnnotations;

namespace RustyTech.Server.Models.User
{
    public class UserRegister
    {
        [Required, EmailAddress]
        public required string Email { get; set; }
        [Required, MinLength(6, ErrorMessage = "Please enter at least 6 characters")]
        public required string Password { get; set; }
        [Required, Compare("Password")]
        public required string ConfirmPassword { get; set; }
        public int BirthYear { get; set; }
    }
}
