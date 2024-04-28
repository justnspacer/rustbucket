namespace RustyTech.Server.Models.User
{
    public class UserUpdateDto
    {
        public Guid UserId { get; set; }
        public string? Email { get; set; }
        public string? UserName { get; set; }
        public int BirthYear { get; set; }
    }
}
