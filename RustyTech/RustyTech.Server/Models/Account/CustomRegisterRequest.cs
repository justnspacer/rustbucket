using Swashbuckle.AspNetCore.Annotations;
using System.ComponentModel.DataAnnotations;

namespace RustyTech.Server.Models.Account
{
    public class CustomRegisterRequest
    {
        [Required, MinLength(4, ErrorMessage = "Please enter at least 4 characters"), MaxLength(20, ErrorMessage = "Please enter at most 20 characters")]
        public required string UserName { get; set; }

        [Required, EmailAddress]
        public required string Email { get; set; }

        [Required, MinLength(6, ErrorMessage = "Please enter at least 6 characters")]
        [RegularExpression(Constants.PasswordRegex.Pattern,
            ErrorMessage = "Please enter at least 6 characters and one lowercase letter, uppercase letter, digit, and special character")]
        [SwaggerSchema(Description = "string")]
        public required string Password { get; set; }

        [Compare("Password", ErrorMessage = "Passwords do not match")]
        public required string ConfirmPassword { get; set; }

        public int BirthYear { get; set; }
    }
}
