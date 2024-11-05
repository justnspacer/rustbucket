using Newtonsoft.Json;
using RustyTech.Server.Models.Spotify;
using RustyTech.Server.Services.Interfaces;
using SpotifyAPI.Web;
using System.Net;
using System.Text;

namespace RustyTech.Server.Services
{
    public class SpotifyService : ISpotifyService
    {
        private readonly IConfiguration _configuration;
        private readonly ILogger<SpotifyService> _logger;
        private readonly string? _apiUrl;

        public SpotifyService(IConfiguration configuration, ILogger<SpotifyService> logger)
        {
            _configuration = configuration;
            _logger = logger;
            _apiUrl = _configuration["Spotify:ApiUrl"];
        }

        public string AuthorizationUrl()
        {
            var clientId = _configuration["Spotify:ClientId"];
            var authUrl = _configuration["Spotify:AuthUrl"];
            var redirectUri = _configuration["Spotify:RedirectUri"];
            var scopes = _configuration["Spotify:DefaultScopes"];
            var url = $"{authUrl}{clientId}&response_type=code&redirect_uri={Uri.EscapeDataString(redirectUri)}&show_dialog=true&scope={Uri.EscapeDataString(scopes)}";
            _logger.LogInformation($"Spotify authorization URL: {url}");
            return url;
        }

        public async Task<SpotifyTokenResponse?> Callback(string code)
        {
            if (string.IsNullOrEmpty(code))
            {
                return null;
            }

            var clientId = _configuration["Spotify:ClientId"];
            var clientSecret = _configuration["Spotify:ClientSecret"];
            var redirectUri = _configuration["Spotify:RedirectUri"];
            var tokenUrl = _configuration["Spotify:TokenUrl"];
            var authHeader = Convert.ToBase64String(Encoding.UTF8.GetBytes(clientId + ":" + clientSecret));

            var content = new FormUrlEncodedContent(new Dictionary<string, string>
            {
                { "grant_type", "authorization_code" },
                { "code", code },
                { "redirect_uri", WebUtility.UrlEncode(redirectUri) },
                { "client_id", clientId },
                { "client_secret", clientSecret }
            });

            using var httpClient = new HttpClient();
            httpClient.DefaultRequestHeaders.Add("Content-Type", "application/x-www-form-urlencoded");
            httpClient.DefaultRequestHeaders.Add("Authorization", "Basic " + authHeader);
            var response = await httpClient.PostAsync(tokenUrl, content);
            if (!response.IsSuccessStatusCode)
            {
                return null;
            }
            var responseString = await response.Content.ReadAsStringAsync();
            var tokenResponse = JsonConvert.DeserializeObject<SpotifyTokenResponse>(responseString);
            return tokenResponse;
        }


        public async Task<string> RefreshAccessToken(string refreshToken)
        {
            var clientId = _configuration["Spotify:ClientId"];
            var clientSecret = _configuration["Spotify:ClientSecret"];
            var url = _configuration["Spotify:TokenUrl"];


            var tokenRequest = new HttpRequestMessage(HttpMethod.Post, url)
            {
                Content = new FormUrlEncodedContent(new Dictionary<string, string>
        {
            { "grant_type", "refresh_token" },
            { "refresh_token", refreshToken },
            { "client_id", clientId },
            { "client_secret", clientSecret }
        })
            };

            using var httpClient = new HttpClient();
            var response = await httpClient.SendAsync(tokenRequest);
            if (!response.IsSuccessStatusCode)
            {
                throw new Exception("Failed to refresh access token");
            }

            var responseString = await response.Content.ReadAsStringAsync();
            var tokenData = JsonConvert.DeserializeObject<SpotifyTokenResponse>(responseString);
            if (tokenData == null)
            {
                throw new Exception("Failed to refresh access token");
            }
            return tokenData.AccessToken;
        }

        public async Task<PrivateUser> GetUserProfile(string accessToken)
        {
            var spotify = new SpotifyClient(accessToken);
            var profile = await spotify.UserProfile.Current();
            return profile;
        }

        public async Task<FullArtist?> GetArtist(string artistId)
        {
            //var spotify = new SpotifyClient(request.AccessToken);
            //var artist = await spotify.Artists.Get(artistId);
            var fullArtist = new FullArtist();
            return fullArtist;
        }
    }
}
