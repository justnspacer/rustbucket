namespace RustyTech.Server.Models.User
{
    public class VideoPost : Post
    {
        public string? VideoUrl { get; set; }
        public override void Display()
        {
            Console.WriteLine($"Title: {Title}");
            Console.WriteLine($"Content: {Content}");
            Console.WriteLine($"Video Url: {VideoUrl}");
            Console.WriteLine($"IsPublished: {IsPublished}");
            Console.WriteLine($"Created At: {CreatedAt}");
            Console.WriteLine($"Updated At: {UpdatedAt}");
        }
    }
}
