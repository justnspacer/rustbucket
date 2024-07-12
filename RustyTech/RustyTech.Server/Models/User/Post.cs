using System.Text.Json.Serialization;

namespace RustyTech.Server.Models.User
{
    public abstract class Post
    {
        public int Id { get; set; }
        public string? Title { get; set; }
        public string? Content { get; set; }
        public bool IsPublished { get; set; }
        public ICollection<Keyword>? Keywords { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }

        public Guid UserId { get; set; } // Foreign key

        [JsonIgnore]
        public User? User { get; set; } // Navigation property

        public abstract void Display();
    }
}
