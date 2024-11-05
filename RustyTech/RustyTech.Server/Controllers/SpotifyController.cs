using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Controllers
{
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
        public IActionResult Authorization()
        {
            var url = _spotifyService.AuthorizationUrl();
            return Ok(url);
        }

        [HttpPost("fetchToken")]
        public async Task<IActionResult> FetchToken(string code)
        {
            var result = await _spotifyService.Callback(code);
            return Ok(result);
        }

        [HttpGet("refreshToken")]
        public async Task<IActionResult> RefreshToken(string refreshToken)
        {
            var result = await _spotifyService.RefreshAccessToken(refreshToken);
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
