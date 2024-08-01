namespace RustyTech.Server.Models.Posts
{
    public class BlogPost : Post
    {
        public List<string>? ImageFiles { get; set; }

        public BlogPost()
        {
            ImageFiles = new List<string>();
        }
    }
}
