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
            if (!result.IsSuccess)
            {
                return BadRequest("Error with user registration");
            }
            return Ok(result);
        }

        [HttpPost("login")]
        public async Task<IActionResult> LoginAsync([FromBody] UserLogin request)
        {
            var result = await _authService.LoginAsync(request);
            if (!result.IsAuthenticated)
            {
                return BadRequest("Error with user login");
            }
            return Ok(result);
        }

        [HttpPost("verifyEmail")]
        public async Task<IActionResult> VerifyEmail([FromBody] ConfirmEmailRequest request)
        {
            var result = await _authService.VerifyEmail(request);
            if (!result.IsSuccess)
            {
                return BadRequest("Error with email verification");
            }
            return Ok(result);
        }

        [HttpPost("resendConfirmationEmail")]
        public IActionResult ResendEmailAsync(string email)
        {
            var result = _authService.ResendEmailAsync(email);
            if (!result.IsSuccess)
            {
                return BadRequest("Error with email resending");
            }
            return Ok(result);
        }

        [HttpPost("forgotPassword")]
        public async Task<IActionResult> ForgotPasswordAsync(string email)
        {
            var result = await _authService.ForgotPasswordAsync(email);
            if (!result.IsSuccess)
            {
                return BadRequest("Error with forgot password");
            }
            return Ok(result);
        }

        //[Authorize]
        [HttpPut("update")]
        public async Task<IActionResult> UpdateUserAsync([FromBody] UserUpdateDto user)
        {
            var result = await _authService.UpdateUserAsync(user);
            if (!result.IsSuccess)
            {
                return BadRequest("Error with user update");
            }
            return Ok(result);
        }

        [HttpPost("resetPassword")]
        public async Task<IActionResult> ResetPasswordAsync([FromBody] ResetPasswordRequest model)
        {
            var result = await _authService.ResetPasswordAsync(model);
            if (!result.IsSuccess)
            {
                return BadRequest("Error with password reset");
            }
            return Ok(result);
        }

        //[Authorize]
        [HttpPost("manage/2fa")]
        public async Task<IActionResult> Enable2faAsync(Guid userId)
        {
            var result = await _authService.EnableTwoFactorAuthenticationAsync(userId);
            if (!result.IsSuccess)
            {
                return BadRequest("Error with enabling 2fa");
            }
            return Ok(result);
        }

        //[Authorize]
        [HttpGet("manage/info")]
        public IActionResult GetInfoAsync(Guid userId)
        {
            var result = _authService.GetInfoAsync(userId);
            if (!result.IsSuccess)
            {
                return BadRequest("Error with getting user info");
            }
            return Ok(result);
        }

        //[Authorize]
        [HttpPost("logout")]
        public IActionResult LogoutAsync()
        {
            var result = _authService.LogoutAsync();
            if (!result.IsAuthenticated)
            {
                return BadRequest("Error with user logout");
            }
            return Ok(result);
        }
    }
}
