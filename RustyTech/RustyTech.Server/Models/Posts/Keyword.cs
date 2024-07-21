namespace RustyTech.Server.Models.Posts
{
    public class Keyword
    {
        public int Id { get; set; }
        public required string Text { get; set; }
        public ICollection<PostKeyword> PostKeywords { get; set; } = new List<PostKeyword>();
    }
}
