using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity.Data;
using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Models.Auth;
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
        private readonly ILogger<AccountController> _logger;

        public AccountController(IAccountService authService, ILogger<AccountController> logger)
        {
            _authService = authService;
            _logger = logger;
        }

        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] CustomRegisterRequest request)
        {
            var result = await _authService.Register(request);
            _logger.LogInformation($"User {request.Email} registered successfully");
            return Ok(result);
        }

        [HttpPost("login")]
        public async Task<IActionResult> LoginAsync([FromBody] Models.Auth.LoginRequest_old request)
        {
            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.Name, request.Email)
            };
            var claimsIdentity = new ClaimsIdentity(claims, CookieAuthenticationDefaults.AuthenticationScheme);
            await HttpContext.SignInAsync(CookieAuthenticationDefaults.AuthenticationScheme, new ClaimsPrincipal(claimsIdentity));
            if (User.Identity.IsAuthenticated)
            {
                return Ok(claimsIdentity);
            }
            return BadRequest();
        }

        [HttpPost("verify/email")]
        public async Task<IActionResult> VerifyEmail([FromBody] VerifyEmailRequest request)
        {
            var result = await _authService.VerifyEmail(request);
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
        public async Task<IActionResult> LogoutAsync()
        {
            //var result = _authService.LogoutAsync();
            //Response.Cookies.Delete("AuthToken");
            await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
            return Redirect("/auth/login");
        }
    }
}
