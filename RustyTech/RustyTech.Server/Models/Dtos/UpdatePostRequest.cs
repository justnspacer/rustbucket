namespace RustyTech.Server.Models.Dtos
{
    public class UpdatePostRequest
    {
        public int? Id { get; set; }
        public string? Title { get; set; }
        public string? Content { get; set; }
        public bool IsPublished { get; set; }
        public List<string>? Keywords { get; set; }
        public Guid UserId { get; set; }
        public string? VideoFile { get; set; }
        public string? ImageFile { get; set; }
        public List<string>? ImageFiles { get; set; }
    }
}
