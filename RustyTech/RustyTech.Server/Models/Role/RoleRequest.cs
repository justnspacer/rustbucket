namespace RustyTech.Server.Models.Role
{
    public class RoleRequest
    {
        public required string RoleId { get; set; }
        public required string RoleName { get; set; }
        public Guid UserId { get; set; }
    }
}
