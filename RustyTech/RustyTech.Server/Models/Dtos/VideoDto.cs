namespace RustyTech.Server.Models.Dtos
{
    public class VideoDto : PostDto
    {
        public required IFormFile VideoFile1 { get; set; }

        public string? VideoFileString { get; set; }
    }
}
