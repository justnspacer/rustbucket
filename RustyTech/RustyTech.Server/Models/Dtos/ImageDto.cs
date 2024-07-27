namespace RustyTech.Server.Models.Dtos
{
    public class ImageDto : PostDto
    {
        public new IFormFile? ImageUrl { get; set; }
    }
}
