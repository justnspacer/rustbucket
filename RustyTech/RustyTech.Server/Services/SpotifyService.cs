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
        private readonly IUserService _userService;
        private readonly DataContext _context;
        private static readonly HttpClient _httpClient = new HttpClient();
        private readonly ILogger<SpotifyService> _logger;
        private readonly string? _apiUrl;
        private readonly string? _authUrl;
        private readonly string? _clientId;
        private readonly string? _clientSecret;
        private readonly string? _redirectUri;
        private readonly string? _scopes;
        private readonly string? _tokenUrl;

        public SpotifyService(IConfiguration configuration, ILogger<SpotifyService> logger, IUserService userService, DataContext context)
        {
            _configuration = configuration;
            _logger = logger;
            _apiUrl = _configuration["Spotify:ApiUrl"];
            _authUrl = _configuration["Spotify:AuthUrl"];
            _clientId = _configuration["Spotify:ClientId"];
            _clientSecret = _configuration["Spotify:ClientSecret"];
            _redirectUri = _configuration["Spotify:RedirectUri"];
            _scopes = _configuration["Spotify:DefaultScopes"];
            _tokenUrl = _configuration["Spotify:TokenUrl"];
            _userService = userService;
            _context = context;
        }

        public string GetAuthorizationUrl(string userId)
        {
            var state = Convert.ToBase64String(Encoding.UTF8.GetBytes($"userId:{userId}"));
            return $"{_authUrl}{_clientId}&response_type=code&redirect_uri={Uri.EscapeDataString(_redirectUri)}&show_dialog=true&scope={Uri.EscapeDataString(_scopes)}&state={state}";
        }

        public async Task<AccessTokenResponse?> Callback(string code, string userId)
        {
            var user = await _userService.GetByIdAsync(userId);
            if (user == null)
            {
                throw new Exception("User not found");
            }
            var requestMessage = new HttpRequestMessage(HttpMethod.Post, _tokenUrl);
            var data = new FormUrlEncodedContent(new Dictionary<string, string>
            {
                { "grant_type", "authorization_code" },
                { "code", code },
                { "redirect_uri", WebUtility.UrlEncode(_redirectUri) }
            });
            var authHeader = Convert.ToBase64String(Encoding.UTF8.GetBytes(_clientId + ":" + _clientSecret));
            var payload = JsonConvert.SerializeObject(data);
            var content = new StringContent(payload, Encoding.UTF8, "application/x-www-form-urlencoded");
            requestMessage.Content = content;
            requestMessage.Headers.Add("Authorization", $"Basic {authHeader}");
            HttpResponseMessage response = await _httpClient.SendAsync(requestMessage);
            _logger.LogInformation($"request content: {content}");
            if (response.IsSuccessStatusCode)
            {
                string responseContent = await response.Content.ReadAsStringAsync();
                var accessToken = JsonConvert.DeserializeObject<AccessTokenResponse>(responseContent);
                var expirationDateTime = DateTime.UtcNow.AddSeconds(accessToken.ExpiresIn);
                _context.OAuthTokens.Add(new OAuthTokens
                {
                    UserId = userId,
                    AccessToken = accessToken.AccessToken,
                    RefreshToken = accessToken.RefreshToken,
                    ExpiresAt = expirationDateTime
                });
                await _context.SaveChangesAsync();
                return accessToken;
            }
            _logger.LogError($"Failed to get access token: {response.StatusCode}");
            throw new Exception($"Failed to get access token: {response.StatusCode}");
        }


        public async Task<AccessTokenResponse?> RefreshAccessToken(string refreshToken, string userId)
        {
            var user = await _userService.GetByIdAsync(userId);
            if (user == null)
            {
                throw new Exception("User not found");
            }
            var content = new FormUrlEncodedContent(new Dictionary<string, string>
            {
                { "grant_type", "refresh_token" },
                { "refresh_token", refreshToken }
            });
            _httpClient.DefaultRequestHeaders.Add("Content-Type", "application/x-www-form-urlencoded");
            var response = await _httpClient.PostAsync(_tokenUrl, content);
            if (!response.IsSuccessStatusCode)
            {
                throw new Exception("Failed to refresh access token");
            }

            var responseString = await response.Content.ReadAsStringAsync();
            var tokenResponse = JsonConvert.DeserializeObject<AccessTokenResponse>(responseString);
            if (tokenResponse == null)
            {
                throw new Exception("Failed to refresh access token");
            }
            var expirationDateTime = DateTime.UtcNow.AddSeconds(tokenResponse.ExpiresIn);
            var tokenToRefresh = await _context.OAuthTokens.SingleOrDefaultAsync(s => s.UserId == userId);
            
            if (tokenToRefresh == null)
            {
                throw new Exception("Token not found");
            }

            tokenToRefresh.AccessToken = tokenResponse.AccessToken;
            tokenToRefresh.RefreshToken = tokenResponse.RefreshToken;
            tokenToRefresh.ExpiresAt = expirationDateTime;
            tokenToRefresh.UpdatedAt = DateTime.UtcNow;
            _context.OAuthTokens.Update(tokenToRefresh);
            await _context.SaveChangesAsync();
            return tokenResponse;
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
