namespace RustyTech.Server.Models.Dtos
{
    public class UpdateUserRequest
    {
        public Guid UserId { get; set; }
        public string? Email { get; set; }
        public string? UserName { get; set; }
        public int BirthYear { get; set; }
    }
}
