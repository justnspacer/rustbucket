using System.ComponentModel.DataAnnotations;

namespace RustyTech.Server.Models.Account
{
    public class EmailRequest
    {
        [Required]
        [EmailAddress]
        public string? To { get; set; }

        [Required]
        [StringLength(100)]
        public string? Subject { get; set; }

        [Required]
        public string? Body { get; set; }
    }
}
