using RustyTech.Server.Models.Posts;
using RustyTech.Server.Services.Interfaces;
using Xabe.FFmpeg;

namespace RustyTech.Server.Services
{
    public class VideoService : IVideoService
    {
        private string _dir;
        private readonly string _videoPath;
        private readonly string _ffmpegPath;
        private readonly IWebHostEnvironment? _webHostEnvironment;

        public VideoService(IWebHostEnvironment webHostEnvironment)
        {
            _dir = webHostEnvironment.WebRootPath;
            _videoPath = Path.Combine(_dir, "videos");
            _ffmpegPath = Path.Combine(_dir, "ffmpeg");
            if (!Directory.Exists(_videoPath))
            {
                Directory.CreateDirectory(_videoPath);
            }
            FFmpeg.SetExecutablesPath(_ffmpegPath, "ffmpeg");
        }

        public async Task<string> UploadVideoAsync(IFormFile file)
        {
            if (file == null || file.Length == 0)
                throw new ArgumentException("Invalid file");

            var cleanFileName = file.FileName.ToLower().Replace(" ", "_");

            var fileName = Path.GetFileNameWithoutExtension(cleanFileName) + "_" + Guid.NewGuid() + Path.GetExtension(cleanFileName);
            var originalFilePath = Path.Combine(_videoPath, fileName);

            using (var stream = new FileStream(originalFilePath, FileMode.Create, FileAccess.Write))
            {
                await file.CopyToAsync(stream);
            }
            /*
            // Optionally convert the video to reduce size
            var convertedFilePath = Path.Combine(_videoPath, Path.GetFileNameWithoutExtension(fileName) + "_converted.mp4");
            var newPath = await ConvertVideoAsync(originalFilePath, convertedFilePath);
            // Delete the original uploaded file
            if (File.Exists(originalFilePath))
            {
               File.Delete(originalFilePath);
            }
            if (newPath == null)
            {
                return "Video conversion error.";
            }
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

        private async Task<string> ConvertVideoAsync(string inputFilePath, string outputFilePath)
        {
            var info = await FFmpeg.GetMediaInfo(inputFilePath);
            var videoStream = info.VideoStreams.First().SetCodec(VideoCodec.h264).SetSize(VideoSize.Hd480);
            var conversion = FFmpeg.Conversions.New().AddStream(videoStream).SetOutput(outputFilePath);
            await conversion.Start();
            return outputFilePath;
        }
    }
}
