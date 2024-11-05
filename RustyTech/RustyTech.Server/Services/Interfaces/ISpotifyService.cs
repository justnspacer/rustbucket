using RustyTech.Server.Models.Spotify;
using SpotifyAPI.Web;

namespace RustyTech.Server.Services.Interfaces
{
    public interface ISpotifyService
    {
        string AuthorizationUrl();
        Task<SpotifyTokenResponse?> Callback(string code);
        Task<string> RefreshAccessToken(string refreshToken);
        Task<PrivateUser> GetUserProfile(string accessToken);
        Task<FullArtist?> GetArtist(string artistId);
    }
}
