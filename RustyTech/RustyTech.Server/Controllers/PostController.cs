﻿using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Interfaces;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Posts;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    [RequestSizeLimit(50 * 1024 * 1024)] //50MB limit for all requests
    public class PostController : ControllerBase
    {
        private readonly IPostService _postService;
        private readonly IRoleService _roleService;
        private readonly IKeywordService _keywordService;

        public PostController(IPostService postService, IRoleService roleService, IKeywordService keywordService)
        {
            _postService = postService;
            _roleService = roleService;
            _keywordService = keywordService;
        }

        [HttpGet("all")]
        public async Task<IActionResult> GetAllAsync(bool published = true)
        {
            var posts = await _postService.GetAllAsync(published);
            return Ok(posts);
        }

        [HttpGet("user")]
        public async Task<IActionResult> GetUserPostAsync([FromQuery] string userId)
        {
            var posts = await _postService.GetUserPostsAsync(userId);
            return Ok(posts);
        }

        [HttpGet("{postId}")]
        public async Task<IActionResult> GetPostByIdAsync(int postId)
        {
            var post = await _postService.GetPostByIdAsync(postId);
            return Ok(post);
        }

        [HttpPost("create/blog")]
        [Consumes("multipart/form-data")]
        public async Task<IActionResult> CreateBlogPostAsync([FromForm] CreateBlogRequest request)
        {
            var post = await _postService.CreateBlogPostAsync(request);
            return Ok(post);
        }

        [HttpPost("create/image")]
        [Consumes("multipart/form-data")]
        public async Task<IActionResult> CreateImagePostAsync([FromForm] CreateImageRequest request)
        {
            var post = await _postService.CreateImagePostAsync(request);
            return Ok(post);
        }

        [HttpPost("create/video")]
        [Consumes("multipart/form-data")]
        public async Task<IActionResult> CreateVideoPostAsync([FromForm] CreateVideoRequest request)
        {
            var post = await _postService.CreateVideoPostAsync(request);
            return Ok(post);
        }

        [Authorize(Roles = "Admin,Manager")]
        [HttpPost("publish/{postId}")]
        public async Task<IActionResult> TogglePostPublishedStatusAsync(int postId)
        {
            var result = await _postService.TogglePostPublishedStatusAsync<Post>(postId);
            return Ok(result);
        }

        [HttpPut("edit")]
        public async Task<IActionResult> EditPostAsync([FromBody] UpdatePostRequest request)
        {
            var result = await _postService.EditPostAsync<Post>(request);
            return Ok(result);
        }

        [HttpGet("keywords")]
        public async Task<IActionResult> GetKeywordsAsync()
        {
            var result = await _keywordService.GetAllKeywordsAsync();
            return Ok(result);
        }

        [HttpGet("keywords/{id}")]
        public async Task<IActionResult> GetPostKeywordsAsync(int id)
        {
            var result = await _keywordService.GetPostKeywordsAsync(id);
            return Ok(result);
        }
    }
}
