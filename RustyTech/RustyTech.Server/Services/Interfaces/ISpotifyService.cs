using RustyTech.Server.Models.Spotify;
using SpotifyAPI.Web;

namespace RustyTech.Server.Services.Interfaces
{
    public interface ISpotifyService
    {
        string GetAuthorizationUrl(string userId);
        Task<AccessTokenResponse?> Callback(string code, string userId);
        Task<AccessTokenResponse?> RefreshAccessToken(string refreshToken, string userId);        
        Task<PrivateUser> GetUserProfile(string accessToken);
        Task<FullArtist?> GetArtist(string artistId);
    }
}
