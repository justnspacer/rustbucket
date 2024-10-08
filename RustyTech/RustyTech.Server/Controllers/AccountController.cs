﻿using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Models.Account;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Services.Interfaces;
using System.Security.Claims;

namespace RustyTech.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AccountController : ControllerBase
    {
        private readonly IAccountService _authService;

        public AccountController(IAccountService authService)
        {
            _authService = authService;
        }

        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] CustomRegisterRequest request)
        {
            var result = await _authService.Register(request);
            return Ok(result);
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] CustomLoginRequest request)
        {
            var result = await _authService.Login(request);
            return Ok(result);
        }

        [Authorize] //adding here later in process, allow users to login and then verify email
        [HttpPost("verify/email")]
        public async Task<IActionResult> VerifyEmail(VerifyEmailRequest request)
        {
            var result = await _authService.VerifyEmail(request);
            return Ok(result);
        }

        [Authorize] //adding here later in process
        [HttpPost("resend/email")]
        public async Task<IActionResult> ResendEmail(string email)
        {
            var result = await _authService.ResendEmail(email);
            return Ok(result);
        }

        [HttpPost("forgot/password")]
        public async Task<IActionResult> ForgotPassword(string email)
        {
            var result = await _authService.ForgotPassword(email);
            return Ok(result);
        }

        [HttpPost("reset/password")]
        public async Task<IActionResult> ResetPassword([FromBody] CustomResetPasswordRequest model)
        {
            var result = await _authService.ResetPassword(model);
            return Ok(result);
        }

        [Authorize]
        [HttpPut("update")]
        [Consumes("multipart/form-data")]
        public async Task<IActionResult> UpdateUser([FromForm] UpdateUserRequest user)
        {
            var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (userId != user.UserId)
            {
                return Forbid();
            }
            var result = await _authService.UpdateUser(user);
            return Ok(result);
        }

        [Authorize]
        [HttpPost("manage/2fa")]
        public async Task<IActionResult> ToggleTwoFactorAuth(string userId)
        {
            var currentUserId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (currentUserId != userId)
            {
                var response = new ResponseBase()
                {
                    IsSuccess = false,
                    Message = "You are not authorized to perform this action."
                };
                return Ok(response);
            }
            var result = await _authService.ToggleTwoFactorAuth(userId);
            return Ok(result);
        }

        [Authorize(Roles = "SuperAdmin")]
        [HttpGet("manage/info")]
        public async Task<IActionResult> GetInfo(string userId)
        {
            var result = await _authService.GetInfo(userId);
            return Ok(result);
        }

        [Authorize]
        [HttpPost("logout")]
        public async Task<IActionResult> Logout()
        {
            var result = await _authService.Logout();
            return Ok(result);
        }

        [HttpGet("isAuthenticated")]
        public IActionResult IsUserAuthenticated()
        {
            var response = new AuthResponse()
            {
                IsAuthenticated = false,
                IsSuccess = false,
                User = null
            };

            if (User.Identity.IsAuthenticated)
            {
                var user = new GetUserRequest()
                {
                    Id = User.FindFirst(ClaimTypes.NameIdentifier)?.Value,
                    Email = User.FindFirst(ClaimTypes.Email)?.Value,
                    UserName = User.FindFirst(ClaimTypes.Name)?.Value
                };

                response.IsAuthenticated = true;
                response.User = user;
                response.IsSuccess = true;
            }
            return Ok(response);
        }
    }
}
