using Microsoft.AspNetCore.Identity;
using RustyTech.Server.Models.Posts;

namespace RustyTech.Server.Models
{
    public class User : IdentityUser
    {
        public new Guid Id { get; set; }
        public override string? Email { get; set; }
        public override string? UserName { get; set; }
        public string? VerificationToken { get; set; }
        public DateTime? VerifiedAt { get; set; }
        public string? PasswordResetToken { get; set; }
        public DateTime? ResetTokenExpires { get; set; }
        public int BirthYear { get; set; }
        public override bool TwoFactorEnabled { get; set; }

        public ICollection<Post> Posts { get; set; } // Navigation property

        public User() => Posts = new List<Post>();
    }
}
