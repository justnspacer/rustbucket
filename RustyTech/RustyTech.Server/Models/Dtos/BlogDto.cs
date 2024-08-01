namespace RustyTech.Server.Models.Dtos
{
    public class BlogDto : PostDto
    {
        public new required string Title { get; set; }
        public new required string Content { get; set; }
        public List<IFormFile>? ImageFiles1 { get; set; }
        public List<string>? ImageFilesString { get; set; }
    }
}
