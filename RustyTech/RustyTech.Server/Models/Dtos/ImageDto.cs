namespace RustyTech.Server.Models.Dtos
{
    public class ImageDto : PostDto
    {
        public new required IFormFile ImageUrl { get; set; }
    }
}
