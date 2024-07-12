namespace RustyTech.Server.Models.User
{
    public class Keyword
    {
        public int Id { get; set; }
        public int PostId { get; set; }
        public string? Text { get; set; }
        public ICollection<Keyword>? Keywords { get; set; }
    }
}
