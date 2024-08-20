using System.Text.Json.Serialization;

namespace RustyTech.Server.Models.Dtos
{
    public class CreateVideoRequest
    {
        public int Id { get; set; }
        public required string Title { get; set; }
        public required string Content { get; set; }
        public required IFormFile VideoFile { get; set; }
        public List<string>? Keywords { get; set; }
        public bool IsPublished { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }
        public string? UserId { get; set; }
        [JsonIgnore]
        public GetUserRequest? User { get; set; }
    }
}
