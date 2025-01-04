using RustyTech.Server.Models.Posts;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IVideoService
    {
        Task<string> UploadVideoAsync(IFormFile file);
        Task<VideoMetadata> GetVideoMetadataAsync(string filePath);
    }
}
