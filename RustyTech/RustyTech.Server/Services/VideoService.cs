using RustyTech.Server.Models.Posts;
using RustyTech.Server.Services.Interfaces;
using Xabe.FFmpeg;

namespace RustyTech.Server.Services
{
    public class VideoService : IVideoService
    {
        private readonly string _videoPath;
        private readonly IWebHostEnvironment _webHostEnvironment;

        public VideoService(IWebHostEnvironment webHostEnvironment)
        {
            _webHostEnvironment = webHostEnvironment;
            _videoPath = Path.Combine(_webHostEnvironment.WebRootPath, "videos");
            if (!Directory.Exists(GetAbsolutePath(_videoPath)))
            {
                Directory.CreateDirectory(GetAbsolutePath(_videoPath));
            }
            FFmpeg.SetExecutablesPath("C:\\ffmpeg-n5.1-latest-win64-lgpl-shared-5.1\\bin"); //address when ffmpeg is installed
        }

        private string GetAbsolutePath(string relativePath)
        {
            return Path.Combine(_webHostEnvironment.WebRootPath, relativePath);
        }

        public async Task<string> UploadVideoAsync(IFormFile file)
        {
            if (file == null || file.Length == 0)
                throw new ArgumentException("Invalid file");

            var cleanFileName = file.FileName.ToLower().Replace(" ", "_");

            var fileName = Path.GetFileNameWithoutExtension(cleanFileName) + "_" + Guid.NewGuid() + Path.GetExtension(cleanFileName);
            var originalFilePath = Path.Combine(_videoPath, fileName);

            using (var stream = new FileStream(originalFilePath, FileMode.Create))
            {
                await file.CopyToAsync(stream);
            }
            /*
            // Optionally convert the video to reduce size
            var convertedFilePath = Path.Combine(_videoPath, Path.GetFileNameWithoutExtension(fileName) + "_converted.mp4");
            var newPath = await ConvertVideoAsync(originalFilePath, convertedFilePath, 1280, 720, 1000);

             Delete the original uploaded file
            if (File.Exists(originalFilePath))
            {
               File.Delete(originalFilePath);
            }
            var relativeFilePath = Path.Combine("/videos", Path.GetFileName(newPath)).Replace("\\", "/");
            */
            var relativeFilePath = Path.Combine("/videos", Path.GetFileName(originalFilePath)).Replace("\\", "/");
            return relativeFilePath;
        }

        public async Task<VideoMetadata> GetVideoMetadataAsync(string filePath)
        {

            var mediaInfo = await FFmpeg.GetMediaInfo(filePath);
            return new VideoMetadata
            {
                Duration = mediaInfo.Duration,
                Posted = mediaInfo.CreationTime,
                Size = new FileInfo(filePath).Length
            };
        }

        private async Task<string> ConvertVideoAsync(string inputFilePath, string outputFilePath, int maxWidth, int maxHeight, int maxBitrate)
        {
            var conversion = FFmpeg.Conversions.New()
                .AddParameter($"-i {inputFilePath}")
                .AddParameter($"-vf scale='min({maxWidth},iw)':'min({maxHeight},ih)':force_original_aspect_ratio=decrease")
                .AddParameter($"-b:v {maxBitrate}k")
                .SetOutput(outputFilePath);

            await conversion.Start();
            return outputFilePath;
        }

        private async Task ConvertToMp4(string filePath)
        {
            var outputFilePath = Path.ChangeExtension(filePath, ".mp4");
            var conversion = await FFmpeg.Conversions.FromSnippet.Convert(filePath, outputFilePath);
            await conversion.Start();
        }
    }
}
