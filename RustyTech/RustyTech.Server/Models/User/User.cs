using Microsoft.AspNetCore.Identity;

namespace RustyTech.Server.Models.User
{
    public class User
    {
        public Guid Id { get; set; }
        public string? Email { get; set; }
        public string? UserName { get; set; }
        public byte[] PasswordHash { get; set; } = new byte[32];
        public byte[] PasswordSalt { get; set; } = new byte[32];
        public string? VerificationToken { get; set; }
        public DateTime? VerifiedAt { get; set; }
        public string? PasswordResetToken { get; set; }
        public DateTime? ResetTokenExpires { get; set; }
        public DateTime? BirthYear { get; set; }
        public bool TwoFactorEnabled { get; set; }
    }
}
