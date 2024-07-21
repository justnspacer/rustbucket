namespace RustyTech.Server.Models.Dtos
{
    public class UserDto
    {
        public Guid Id { get; set; }
        public string? Email { get; set; }
        public string? UserName { get; set; }
        public DateTime? VerifiedAt { get; set; }
    }
}
