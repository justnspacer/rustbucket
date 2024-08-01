using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace RustyTech.Server.Models.Posts
{
    public abstract class Post
    {
        public int Id { get; set; }

        [StringLength(60, MinimumLength = 5, ErrorMessage = "Title must be between 5 and 60 characters.")]
        public string? Title { get; set; }

        [MaxLength(20000, ErrorMessage = "Content cannot exceed 20000 characters.")]
        public string? Content { get; set; }
        public string? PlainTextContent { get; set; }
        public bool IsPublished { get; set; }
        public ICollection<PostKeyword> Keywords { get; set; } = new List<PostKeyword>();
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }

        public Guid UserId { get; set; } // Foreign key

        [JsonIgnore]
        public User? User { get; set; } // Navigation property
    }
}
