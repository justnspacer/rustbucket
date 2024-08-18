namespace RustyTech.Server.Models.Account
{
    public class CustomResetPasswordRequest
    {
        public required string Email { get; set; }
        public required string ResetCode { get; set; }
        public required string NewPassword { get; set; }
        public required string CurrentPassword { get; set; }
    }
}
