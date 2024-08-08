using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity.Data;
using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        private readonly IAuthService _authService;
        private readonly ILogger<AuthController> _logger;

        public AuthController(IAuthService authService, ILogger<AuthController> logger)
        {
            _authService = authService;
            _logger = logger;
        }

        [HttpPost("register")]
        public async Task<IActionResult> RegisterAsync([FromBody] Models.Auth.RegisterRequest request)
        {
            var result = await _authService.RegisterAsync(request);
            _logger.LogInformation($"User {request.Email} registered successfully");
            return Ok(result);
        }

        [HttpPost("login")]
        public async Task<IActionResult> LoginAsync([FromBody] Models.Auth.LoginRequest request)
        {
            var result = await _authService.LoginAsync(request);

            if (result.Token == null)
            {
                _logger.LogError($"Invalid login attempt for {request.Email}");
                return BadRequest("Invalid login attempt");
            }
            Response.Cookies.Append("AuthToken", result.Token);

            return Ok(result);
        }

        [HttpPost("verify/email")]
        public async Task<IActionResult> VerifyEmail([FromBody] ConfirmEmailRequest request)
        {
            var result = await _authService.VerifyEmailAsync(request);
            _logger.LogInformation($"Email verified");
            return Ok(result);
        }

        [Authorize]
        [HttpGet("verify/token")]
        public IActionResult VerifyJwtToken()
        {
            var authHeader = HttpContext.Request.Headers["Authorization"].ToString();
            if (string.IsNullOrEmpty(authHeader) || !authHeader.StartsWith("Bearer ", StringComparison.OrdinalIgnoreCase))
            {
                return BadRequest("Missing or invalid Authorization header");
            }
            var token = authHeader.Substring("Bearer ".Length).Trim();
            var result = _authService.VerifyJwtToken(token);
            return Ok(result);
        }

        [HttpPost("resend")]
        public IActionResult ResendEmailAsync(string email)
        {
            var result = _authService.ResendEmailAsync(email);
            _logger.LogInformation($"Email resent to {email}");
            return Ok(result);
        }

        [HttpPost("forgot/password")]
        public async Task<IActionResult> ForgotPasswordAsync(string email)
        {
            var result = await _authService.ForgotPasswordAsync(email);
            _logger.LogInformation($"Forgot password: {email}");
            return Ok(result);
        }

        [Authorize]
        [HttpPut("update")]
        public async Task<IActionResult> UpdateUserAsync([FromBody] UpdateUserRequest user)
        {
            var result = await _authService.UpdateUserAsync(user);
            _logger.LogInformation($"User updated");
            return Ok(result);
        }

        [Authorize]
        [HttpPost("reset/password")]
        public async Task<IActionResult> ResetPasswordAsync([FromBody] ResetPasswordRequest model)
        {
            var result = await _authService.ResetPasswordAsync(model);
            return Ok(result);
        }

        [Authorize]
        [HttpPost("manage/2fa")]
        public async Task<IActionResult> Enable2faAsync(Guid userId)
        {
            var result = await _authService.EnableTwoFactorAuthenticationAsync(userId);
            return Ok(result);
        }

        [Authorize]
        [HttpGet("manage/info")]
        public IActionResult GetInfoAsync(Guid userId)
        {
            var result = _authService.GetInfoAsync(userId);
            _logger.LogInformation($"2fa status for: {userId}");
            return Ok(result);
        }

        [Authorize]
        [HttpPost("logout")]
        public IActionResult LogoutAsync()
        {
            var result = _authService.LogoutAsync();
            Response.Cookies.Delete("AuthToken");
            return Ok(result);
        }
    }
}
