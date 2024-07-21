namespace RustyTech.Server.Models.Dtos
{
    public class BlogDto : PostDto
    {
        public List<string>? ImageUrls { get; set; }
    }
}
