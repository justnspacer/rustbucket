﻿namespace RustyTech.Server.Models.User
{
    public class ImagePost : Post
    {
        public string? ImageUrl { get; set; }
        public override void Display()
        {
            Console.WriteLine($"Title: {Title}");
            Console.WriteLine($"Content: {Content}");
            Console.WriteLine($"Image Url: {ImageUrl}");
            Console.WriteLine($"IsPublished: {IsPublished}");
            Console.WriteLine($"Created At: {CreatedAt}");
            Console.WriteLine($"Updated At: {UpdatedAt}");
        }
    }
}
