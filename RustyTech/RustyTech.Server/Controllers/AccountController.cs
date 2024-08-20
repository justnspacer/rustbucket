using Microsoft.AspNetCore.Authorization;
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

        [HttpPost("verify/email")]
        public async Task<IActionResult> VerifyEmail([FromBody] VerifyEmailRequest request)
        {
            var result = await _authService.VerifyEmail(request);
            return Ok(result);
        }

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
        public async Task<IActionResult> UpdateUser([FromBody] UpdateUserRequest user)
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
                return Forbid();
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
    }
}
