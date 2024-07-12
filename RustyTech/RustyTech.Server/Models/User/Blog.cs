namespace RustyTech.Server.Models.User
{
    public class Blog : Post
    {
        public List<string> ImageUrls { get; set; }

        public Blog()
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
