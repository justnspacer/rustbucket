using System.Text.Json.Serialization;

namespace RustyTech.Server.Models.Posts
{
    public abstract class Post
    {
        public int Id { get; set; }
        public string? Title { get; set; }
        public string? Content { get; set; }
        public bool IsPublished { get; set; }
        public ICollection<PostKeyword> Keywords { get; set; } = new List<PostKeyword>();
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }

        public Guid UserId { get; set; } // Foreign key

        [JsonIgnore]
        public User? User { get; set; } // Navigation property

        public abstract void Display();
    }
}
