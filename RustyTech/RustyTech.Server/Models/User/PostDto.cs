using System.Text.Json.Serialization;

namespace RustyTech.Server.Models.User
{
    public class PostDto
    {
        public int Id { get; set; }
        public string? Title { get; set; }
        public string? Content { get; set; }
        public bool IsPublished { get; set; }
        public List<string>? Keywords { get; set; }

        public DateTime? CreatedAt { get; set; }
        public DateTime? UpdatedAt { get; set; }
        public Guid UserId { get; set; }
        [JsonIgnore]
        public UserDto? User { get; set; }
    }
}
