namespace RustyTech.Server.Models.Dtos
{
    public class GetUserRequest
    {
        public string? Id { get; set; }
        public string? Email { get; set; }
        public string? UserName { get; set; }
        public DateTime? VerifiedAt { get; set; }
    }
}
