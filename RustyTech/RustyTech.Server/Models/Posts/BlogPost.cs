namespace RustyTech.Server.Models.Posts
{
    public class BlogPost : Post
    {
        public List<string> ImageUrls { get; set; }

        public BlogPost()
        {
            ImageUrls = new List<string>();
        }

        public override void Display()
        {
            Console.WriteLine($"Title: {Title}");
            Console.WriteLine($"Content: {Content}");
            Console.WriteLine("Images:");
            foreach (var imageUrl in ImageUrls)
            {
                Console.WriteLine(imageUrl);
            }
            Console.WriteLine($"IsPublished: {IsPublished}");
            Console.WriteLine($"Created At: {CreatedAt}");
            Console.WriteLine($"Updated At: {UpdatedAt}");
        }
    }
}
