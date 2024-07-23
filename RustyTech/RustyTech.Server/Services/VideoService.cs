using RustyTech.Server.Services.Interfaces;
using Xabe.FFmpeg;

namespace RustyTech.Server.Services
{
    public class VideoService : IVideoService
    {
        private readonly string _videoPath;

        public VideoService()
        {
            _videoPath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "videos");
            if (!Directory.Exists(_videoPath))
            {
                Directory.CreateDirectory(_videoPath);
            }
            FFmpeg.SetExecutablesPath("path_to_ffmpeg");
        }

        public async Task<string> UploadVideoAsync(IFormFile file)
        {
            if (file == null || file.Length == 0)
                throw new ArgumentException("Invalid file");

            var fileName = Path.GetFileNameWithoutExtension(file.FileName) + "_" + Guid.NewGuid() + Path.GetExtension(file.FileName);
            var filePath = Path.Combine(_videoPath, fileName);

            // Optionally convert the video to reduce size
            //await ConvertToMp4(filePath);
            var convertedFilePath = Path.Combine(_videoPath, Path.GetFileNameWithoutExtension(fileName) + "_converted.mp4");
            //await ConvertVideoAsync(filePath, convertedFilePath, 1280, 720, 1000);

            using (var stream = new FileStream(convertedFilePath, FileMode.Create))
            {
                await file.CopyToAsync(stream);
            }

            return convertedFilePath;
        }

        public async Task<VideoMetadata> GetVideoMetadataAsync(string filePath)
        {
            var mediaInfo = await FFmpeg.GetMediaInfo(filePath);
            return new VideoMetadata
            {
                Duration = mediaInfo.Duration,
                Format = mediaInfo.ToString(), //double check this
                Size = new FileInfo(filePath).Length
            };
        }

        private async Task ConvertToMp4(string filePath)
        {
            var outputFilePath = Path.ChangeExtension(filePath, ".mp4");
            var conversion = await FFmpeg.Conversions.FromSnippet.Convert(filePath, outputFilePath);
            await conversion.Start();
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
    }

    public class VideoMetadata
    {
        public TimeSpan Duration { get; set; }
        public string? Format { get; set; }
        public long Size { get; set; }
    }
}
