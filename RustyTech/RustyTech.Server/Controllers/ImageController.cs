using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ImageController : ControllerBase
    {
        private readonly IImageService _imageService;

        public ImageController(IImageService imageService)
        {
            _imageService = imageService;
        }

        [HttpPost("upload")]
        public async Task<IActionResult> UploadImage(IFormFile file)
        {
            try
            {
                var filePath = await _imageService.UploadImageAsync(file);
                return Ok(new { filePath });
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpGet("metadata")]
        public async Task<IActionResult> GetImageMetadata(string filePath)
        {
            try
            {
                var metadata = await _imageService.GetImageMetadataAsync(filePath);
                return Ok(metadata);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }
    }
}
