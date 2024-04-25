using System.ComponentModel.DataAnnotations;

namespace RustyTech.Server.Models.Auth
{
    public class ChangePasswordRequest
    {
        [Required]
        public required string Token { get; set; }

        [Required, MinLength(6, ErrorMessage = "Please enter at least 6 characters")]
        public required string Password { get; set; }

        [Required, Compare("Password")]
        public required string ConfirmPassword { get; set; }
    }
}
