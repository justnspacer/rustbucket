﻿using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Services
{
    public class ImageService : IImageService
    {
        private readonly string _imagePath;
        private readonly IWebHostEnvironment _webHostEnvironment;

        public ImageService(IWebHostEnvironment webHostEnvironment)
        {
            _webHostEnvironment = webHostEnvironment;
            _imagePath = Path.Combine(_webHostEnvironment.WebRootPath, "images");
            if (!Directory.Exists(GetAbsolutePath(_imagePath)))
            {
                Directory.CreateDirectory(GetAbsolutePath(_imagePath));
            }
        }

        private string GetAbsolutePath(string relativePath)
        {
            return Path.Combine(_webHostEnvironment.WebRootPath, relativePath);
        }

        public async Task<string> UploadImageAsync(IFormFile file)
        {
            if (file == null || file.Length == 0)
                throw new ArgumentException("Invalid file");

            /*
             * Web Thumbnails: 150x150 pixels
             * Web Full-Size Images: 800x600 pixels or 1024x768 pixels
             * Mobile Thumbnails: 100x100 pixels
             * Mobile Full-Size Images: 600x800 pixels
            */

            var resizeImage = await ResizeImageAsync(file, 1024, 768);

            var fileName = Path.GetFileNameWithoutExtension(file.FileName) + "_" + Guid.NewGuid() + "_resized" + Path.GetExtension(file.FileName);
            var filePath = Path.Combine(_imagePath, fileName);

            using (var stream = new FileStream(filePath, FileMode.Create))
            {
                await file.CopyToAsync(stream);
            }

            var relativeFilePath = Path.Combine("/images", Path.GetFileName(filePath)).Replace("\\", "/");
            return relativeFilePath;
        }

        public async Task<ImageMetadata> GetImageMetadataAsync(string filePath)
        {
            using (var image = await Image.LoadAsync(filePath))
            {
                return new ImageMetadata
                {
                    Width = image.Width,
                    Height = image.Height,
                    Format = image.Metadata.DecodedImageFormat?.ToString()
                };
            }
        }

        public void DeleteImage(string filePath)
        {
            var file = Path.Combine(_imagePath, filePath.TrimStart('/').Replace("/", "\\"));
            if (File.Exists(file))
            {
                File.Delete(file);
            }
        }

        private async Task<byte[]> ResizeImageAsync(IFormFile file, int maxWidth, int maxHeight)
        {
            using (var stream = new MemoryStream())
            {
                await file.CopyToAsync(stream);
                stream.Seek(0, SeekOrigin.Begin);

                using (var image = await Image.LoadAsync(stream))
                {
                    var (newWidth, newHeight) = CalculateDimensions(image.Width, image.Height, maxWidth, maxHeight);
                    image.Mutate(x => x.Resize(newWidth, newHeight));

                    using (var output = new MemoryStream())
                    {
                        await image.SaveAsJpegAsync(output);
                        return output.ToArray();
                    }
                }
            }
        }

        private (int width, int height) CalculateDimensions(int originalWidth, int originalHeight, int maxWidth, int maxHeight)
        {
            var aspectRatio = (double)originalWidth / originalHeight;

            if (originalWidth > originalHeight) // Landscape
            {
                var width = Math.Min(maxWidth, originalWidth);
                var height = (int)(width / aspectRatio);
                if (height > maxHeight)
                {
                    height = maxHeight;
                    width = (int)(height * aspectRatio);
                }
                return (width, height);
            }
            else // Portrait
            {
                var height = Math.Min(maxHeight, originalHeight);
                var width = (int)(height * aspectRatio);
                if (width > maxWidth)
                {
                    width = maxWidth;
                    height = (int)(width / aspectRatio);
                }
                return (width, height);
            }
        }
    }
}

public class ImageMetadata
{
    public int Width { get; set; }
    public int Height { get; set; }
    public string? Format { get; set; }
}