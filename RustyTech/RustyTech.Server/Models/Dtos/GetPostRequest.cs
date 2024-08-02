
namespace RustyTech.Server.Models.Dtos
{
    public class GetPostRequest
    {
        public int Id { get; set; }
        public string? Title { get; set; }
        public string? Content { get; set; }
        public bool IsPublished { get; set; }
        public List<string>? Keywords { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }
        public GetUserRequest? User { get; set; }
        public Guid UserId { get; set; }
        public string? PostType { get; set; }
        public string? VideoFile { get; set; } 
        public string? ImageFile { get; set; }
        public List<string>? ImageFiles { get; set; }
    }
}
