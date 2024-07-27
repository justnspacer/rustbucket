namespace RustyTech.Server.Models.Dtos
{
    public class VideoDto : PostDto
    {
        public new IFormFile? VideoUrl { get; set; }
    }
}
