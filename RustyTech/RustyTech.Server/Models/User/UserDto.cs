namespace RustyTech.Server.Models.User
{
    public class UserDto
    {
        public Guid Id { get; set; }
        public string? Email { get; set; }
        public string? UserName { get; set; }
        public ICollection<Post>? Posts { get; set; } // Navigation property
    }
}
