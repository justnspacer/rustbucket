using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PostController : ControllerBase
    {
        private readonly IPostService _postService;
        public PostController(IPostService postService)
        {
            _postService = postService;
        }

        [HttpGet("get/all")]
        public async Task<IActionResult> GetAllAsync(bool published = true)
        {
            var posts = await _postService.GetAllAsync(published);
            return Ok(posts);
        }

        [HttpPost("create/blog")]
        public async Task<IActionResult> CreateBlogPostAsync([FromBody] BlogPost request)
        {
            var post = await _postService.CreateBlogPostAsync(request);
            return Ok(post);
        }

        [HttpPost("create/image")]
        public async Task<IActionResult> CreateImagePostAsync([FromBody] ImagePost request)
        {
            var post = await _postService.CreateImagePostAsync(request);
            return Ok(post);
        }

        [HttpPost("create/video")]
        public async Task<IActionResult> CreateVideoPostAsync([FromBody] VideoPost request)
        {
            var post = await _postService.CreateVideoPostAsync(request);
            return Ok(post);
        }
    }
}
