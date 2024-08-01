namespace RustyTech.Server.Models.Dtos
{
    public class ImageCreateDto : PostDto
    {
        public required IFormFile ImageFile1 { get; set; }
        public required string ImageFileString { get; set; }
    }
}
