using Microsoft.AspNetCore.Identity;

namespace RustyTech.Server.Models.User
{
    public class User : IdentityUser
    {
        public new Guid Id { get; set; }
        public override string? Email { get; set; }
        public override string? UserName { get; set; }
        public new byte[] PasswordHash { get; set; } = new byte[32];
        public byte[] PasswordSalt { get; set; } = new byte[32];
        public string? VerificationToken { get; set; }
        public DateTime? VerifiedAt { get; set; }
        public string? PasswordResetToken { get; set; }
        public DateTime? ResetTokenExpires { get; set; }
        public int BirthYear { get; set; }
        public override bool TwoFactorEnabled { get; set; }
    }
}
