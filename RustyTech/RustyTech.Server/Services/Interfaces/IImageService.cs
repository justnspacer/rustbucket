namespace RustyTech.Server.Services.Interfaces
{
    public interface IImageService
    {
        Task<string> UploadImageAsync(IFormFile file);
        Task<ImageMetadata> GetImageMetadataAsync(string filePath);

    }
}
