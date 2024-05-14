using Microsoft.AspNetCore.Identity.Data;
using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Services;

namespace RustyTech.Server.Controllers
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
        public async Task<IActionResult> RegisterAsync([FromBody] UserRegister request)
        {
            var result = await _authService.RegisterAsync(request);
            return Ok(result);
        }

        [HttpPost("login")]
        public async Task<IActionResult> LoginAsync([FromBody] UserLogin request)
        {
            var result = await _authService.LoginAsync(request);
            return Ok(result);
        }

        [HttpPost("verify/email")]
        public async Task<IActionResult> VerifyEmail([FromBody] ConfirmEmailRequest request)
        {
            var result = await _authService.VerifyEmailAsync(request);
            return Ok(result);
        }

        [HttpGet("verify/token")]
        public IActionResult VerifyJwtToken(string token)
        {
            var result = _authService.VerifyJwtToken(token);
            return Ok(result);
        }

        [HttpPost("resend/email")]
        public IActionResult ResendEmailAsync(string email)
        {
            var result = _authService.ResendEmailAsync(email);
            return Ok(result);
        }

        [HttpPost("forgot/password")]
        public async Task<IActionResult> ForgotPasswordAsync(string email)
        {
            var result = await _authService.ForgotPasswordAsync(email);
            return Ok(result);
        }

        //[Authorize]
        [HttpPut("update")]
        public async Task<IActionResult> UpdateUserAsync([FromBody] UserUpdateDto user)
        {
            var result = await _authService.UpdateUserAsync(user);
            return Ok(result);
        }

        [HttpPost("reset/password")]
        public async Task<IActionResult> ResetPasswordAsync([FromBody] ResetPasswordRequest model)
        {
            var result = await _authService.ResetPasswordAsync(model);
            return Ok(result);
        }

        //[Authorize]
        [HttpPost("manage/2fa")]
        public async Task<IActionResult> Enable2faAsync(Guid userId)
        {
            var result = await _authService.EnableTwoFactorAuthenticationAsync(userId);
            return Ok(result);
        }

        //[Authorize]
        [HttpGet("manage/info")]
        public IActionResult GetInfoAsync(Guid userId)
        {
            var result = _authService.GetInfoAsync(userId);
            return Ok(result);
        }

        //[Authorize]
        [HttpPost("logout")]
        public IActionResult LogoutAsync()
        {
            var result = _authService.LogoutAsync();
            return Ok(result);
        }
    }
}
