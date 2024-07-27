using System.ComponentModel.DataAnnotations;

namespace RustyTech.Server.Models.Posts
{
    public class Keyword
    {
        public int Id { get; set; }
        [MaxLength(100, ErrorMessage = "A maximum of 100 keywords is allowed.")]
        public required string Text { get; set; }
        public ICollection<PostKeyword> PostKeywords { get; set; } = new List<PostKeyword>();
    }
}
