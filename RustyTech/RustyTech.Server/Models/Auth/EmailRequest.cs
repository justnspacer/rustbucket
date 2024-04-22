using System.ComponentModel.DataAnnotations;

namespace RustyTech.Server.Models.Auth
{
    public class EmailRequest
    {
        [Required]
        [EmailAddress]
        public string? To { get; set; }

        [Required]
        [StringLength(100, MinimumLength = 5)]
        public string? Subject { get; set; }

        [Required]
        public string? Body { get; set; }
    }
}
