namespace RustyTech.Server.Models.User
{
    public class PostKeyword
    {
        public int PostId { get; set; }
        public Post? Post { get; set; }
        public int KeywordId { get; set; }
        public Keyword? Keyword { get; set; }
    }
}
