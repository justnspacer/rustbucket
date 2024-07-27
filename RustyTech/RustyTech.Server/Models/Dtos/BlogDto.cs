namespace RustyTech.Server.Models.Dtos
{
    public class BlogDto : PostDto
    {
        public new IEnumerable<IFormFile>? ImageUrls { get; set; }
    }
}
