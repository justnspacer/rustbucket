﻿using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Interfaces;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PostController : ControllerBase
    {
        private readonly IPostService _postService;
        private readonly IRoleService _roleService;

        public PostController(IPostService postService, IRoleService roleService)
        {
            _postService = postService;
            _roleService = roleService;
        }

        [HttpGet("get/all")]
        public async Task<IActionResult> GetAllAsync(bool published = true)
        {
            var posts = await _postService.GetAllAsync(published);
            return Ok(posts);
        }

        [HttpGet("get/{postId}")]
        public async Task<IActionResult> GetPostByIdAsync(int postId)
        {
            var post = await _postService.GetPostByIdAsync(postId);
            return Ok(post);
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

        [Authorize(Roles = "Admin")]
        [HttpPost("publish")]
        public async Task<IActionResult> TogglePostPublishedStatusAsync(int postId)
        {
            var result = await _postService.TogglePostPublishedStatusAsync<Post>(postId);
            return Ok(result);
        }
    }
}
