namespace RustyTech.Server.Models.Role
{
    public class UserRole
    {
        public string? RoleId { get; set; }
        public Guid UserId { get; set; }
        public DateTime CreatedAt { get; set; }
    }
}
