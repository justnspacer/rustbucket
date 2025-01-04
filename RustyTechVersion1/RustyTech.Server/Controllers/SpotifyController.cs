using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Models.Account;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Spotify;
using RustyTech.Server.Services.Interfaces;
using System.Security.Claims;
using System.Text;

namespace RustyTech.Server.Controllers
{
    //[Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class SpotifyController : ControllerBase
    {
        private readonly ISpotifyService _spotifyService;

        public SpotifyController(ISpotifyService spotifyService)
        {
            _spotifyService = spotifyService;
        }

        [HttpGet("authorization")]
        public IActionResult GetAuthorizationUrl()
        {
            var response = new AuthResponse()
            {
                IsAuthenticated = false,
                IsSuccess = false,
                User = null
            };

            var url = string.Empty;

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
                url = _spotifyService.GetAuthorizationUrl(user.Id);
            }
            return Ok(new { url });
        }

        [HttpPost("callback")]
        public async Task<IActionResult> Callback([FromBody] Callback callback)
        {
            var error = HttpContext.Request.Query["error"];
            //var state = HttpContext.Request.Query["state"];
            //var code = HttpContext.Request.Query["code"];

            if (!string.IsNullOrEmpty(error))
            {
                return BadRequest(error);
            }

            if (string.IsNullOrEmpty(callback.Code))
            {
                return BadRequest("Invalid code");
            }
            if (string.IsNullOrEmpty(callback.State))
            {
                return BadRequest("state_mismatch");
            }

            var decodedUrl = Uri.UnescapeDataString(callback.State);
            var decodedBytes = Convert.FromBase64String(decodedUrl);
            var decodedState = Encoding.UTF8.GetString(decodedBytes);
            var userId = decodedState.Split(':')[1];
            var result = await _spotifyService.Callback(callback.Code, userId);
            return Ok(result);
        }

        [HttpPost("refreshToken")]
        public async Task<IActionResult> RefreshToken(string refreshToken, string userId)
        {
            var result = await _spotifyService.RefreshAccessToken(refreshToken, userId);
            return Ok(result);
        }

        [HttpGet("getUserProfile")]
        public async Task<IActionResult> GetUserProfile(string accessToken)
        {
            var result = await _spotifyService.GetUserProfile(accessToken);
            return Ok(result);
        }

        [HttpGet("getArtist")]
        public async Task<IActionResult> GetArtist(string artistId)
        {
            var result = await _spotifyService.GetArtist(artistId);
            return Ok(result);
        }
    }
}
