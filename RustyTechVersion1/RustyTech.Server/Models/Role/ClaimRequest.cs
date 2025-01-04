namespace RustyTech.Server.Models.Role
{
    public class ClaimRequest
    {
        public required string RoleName { get; set; }
        public required string ClaimType { get; set; }
        public required string ClaimValue { get; set; }
    }
}
