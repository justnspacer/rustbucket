namespace RustyTech.Server.Models.Posts
{
    public class PostKeyword
    {
        public int Id { get; set; }
        public int PostId { get; set; }
        public Post? Post { get; set; }
        public int KeywordId { get; set; }
        public Keyword? Keyword { get; set; }
    }
}
