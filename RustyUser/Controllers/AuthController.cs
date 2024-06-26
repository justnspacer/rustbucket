﻿using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity.Data;
using Microsoft.AspNetCore.Mvc;
using RustyUser.Models.Auth;
using RustyUser.Models.User;
using RustyUser.Services;

namespace RustyUser.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        private readonly AuthService _authService;

        public AuthController(AuthService authService)
        {
            _authService = authService;
        }

        [HttpPost("register")]
        public async Task<IActionResult> RegisterAsync([FromBody] UserRegister model)
        {
            var result = await _authService.RegisterAsync(model);
            return Ok(result);
        }

        [HttpPost("login")]
        public async Task<IActionResult> LoginAsync([FromBody] UserLogin model)
        {
            var result = await _authService.LoginAsync(model);
            return Ok(result);
        }

        [HttpPost("confirmEmail")]
        public async Task<IActionResult> ConfirmEmailAsync(ConfirmEmailRequest model)
        {
            var result = await _authService.ConfirmEmailAsync(model);
            return Ok(result);
        }

        [HttpPost("resendConfirmationEmail")]
        public async Task<IActionResult> ResendEmailAsync(string email)
        {
            var result = await _authService.ResendEmailAsync(email);
            return Ok(result);
        }

        [HttpPost("forgotPassword")]
        public async Task<IActionResult> ForgotPasswordAsync(string email)
        {
            var result = await _authService.ForgotPasswordAsync(email);
            return Ok(result);
        }

        //[Authorize]
        [HttpPut("update/{id}")]
        public async Task<IActionResult> UpdateUserAsync(string id, UserUpdate user)
        {
            var result = await _authService.UpdateUserAsync(id, user);
            return Ok(result);
        }

        [HttpPost("resetPassword")]
        public async Task<IActionResult> ResetPasswordAsync([FromBody] ResetPasswordRequest model)
        {
            var result = await _authService.ResetPasswordAsync(model);
            return Ok(result);
        }

        //[Authorize]
        [HttpPost("manage/2fa")]
        public async Task<IActionResult> Enable2faAsync(string userId)
        {
            var result = await _authService.Enable2faAsync(userId);
            return Ok(result);
        }

        //[Authorize]
        [HttpGet("manage/info")]
        public async Task<IActionResult> GetInfoAsync(string userId)
        {
            var result = await _authService.GetInfoAsync(userId);
            return Ok(result);
        }

        [Authorize]
        [HttpPost("manage/changePassword")]
        public async Task<IActionResult> ChangePasswordAsync([FromBody] ChangePasswordRequest model)
        {
            var result = await _authService.ChangePasswordAsync(model);
            return Ok(result);
        }

        [Authorize]
        [HttpPost("logout")]
        public async Task<IActionResult> LogoutAsync()
        {
            var result = await _authService.LogoutAsync();
            return Ok(result);
        }
    }
}
