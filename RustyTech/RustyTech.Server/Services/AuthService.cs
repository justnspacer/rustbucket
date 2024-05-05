using Microsoft.AspNetCore.Identity.Data;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Net;
using System.Security.Claims;
using System.Text;
using RustyTech.Server.Models.Auth;
using System.Security.Cryptography;

namespace RustyTech.Server.Services
{
    public class AuthService
    {
        private readonly IEmailService _emailService;
        private readonly IConfiguration _configuration;
        private readonly ILogger<UserService> _logger;
        private readonly DataContext _context;

        public AuthService(IEmailService emailService, IConfiguration configuration,
            ILogger<UserService> logger, DataContext context)
        {
            _emailService = emailService;
            _configuration = configuration;
            _logger = logger;
            _context = context;
        }

        public async Task<ResponseBase> RegisterAsync(UserRegister request)
        {
            if (_context.Users.Any(user => user.Email == request.Email))
            {
                return new ResponseBase() { IsSuccess = false, Message = "User already exists" };
            }

            CreatePasswordHash(request.Password, out byte[] passwordHash, out byte[] passwordSalt);

            var user = new User
            {
                UserName = request.Email,
                Email = request.Email,
                NormalizedEmail = request.Email.ToUpper(),
                NormalizedUserName = request.Email.ToUpper(),
                PasswordHash = passwordHash,
                PasswordSalt = passwordSalt,
                VerificationToken = CreateRandomToken(),
                BirthYear = request.BirthYear,
            };

            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            //address
            if (user.Email == "someemail")
            {
                user.VerifiedAt = DateTime.UtcNow;
            }

            SendConfirmationEmail(user.Email, user.Id, EncodeToken(user.VerificationToken));
            _logger.LogInformation($"register email sent");

            return new ResponseBase() { IsSuccess = true, Message = "User registered, email confirmation sent" };
        }

        public async Task<LoginResponse> LoginAsync(UserLogin request)
        {
            var user = _context.Users.FirstOrDefault(user => user.Email == request.Email);
            if (user == null)
            {
                return new LoginResponse() { IsAuthenticated = false, Message = "User not found" };
            }

            if (user.VerifiedAt == null)
            {
                return new LoginResponse() { IsAuthenticated = false, Message = "User not verified" };
            }

            if (!VerifyPasswordHash(request.Password, user.PasswordHash, user.PasswordSalt))
            {
                return new LoginResponse() { IsAuthenticated = false, Message = "Invalid creds" };
            }
            await AddLoginRecordAsync(user.Id, "RustyTech", "Email", string.Empty);
            var token = GenerateJwtToken(request.Email);
            var userDto = new UserDto
            {
                Id = user.Id,
                Email = user.Email,
            };
            return new LoginResponse() { IsAuthenticated = true, IsSuccess = true, User = userDto, Token = token, Message = "User logged in" };
        }

        public async Task<ResponseBase> VerifyEmailAsync(ConfirmEmailRequest request)
        {
            var decodedToken = DecodeToken(request.Token);
            if (decodedToken == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = "Token not found" };
            }

            var user = _context.Users.FirstOrDefault(user => user.VerificationToken == decodedToken);
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = "Invalid token" };
            }

            user.VerifiedAt = DateTime.UtcNow;
            user.EmailConfirmed = true;
            await _context.SaveChangesAsync();
            return new ResponseBase() { IsSuccess = true };
        }

        public ResponseBase ResendEmailAsync(string email)
        {
            if (string.IsNullOrEmpty(email))
            {
                return new ResponseBase() { IsSuccess = false, Message = "Email required" };
            }

            var user = _context.Users.FirstOrDefault(user => user.Email == email);
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = "User not found" };
            }

            if (user.Email != null)
            {
                if (user.VerificationToken != null)
                {
                    SendConfirmationEmail(user.Email, user.Id, EncodeToken(user.VerificationToken));
                    _logger.LogInformation($"resent confirmation email");
                }
            }
            return new ResponseBase() { IsSuccess = true, Message = "Resend confirmation email sent" };
        }

        public async Task<ResponseBase> ForgotPasswordAsync(string email)
        {
            var user = _context.Users.FirstOrDefault(user => user.Email == email);
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = "User not found" };
            }

            user.PasswordResetToken = CreateRandomToken();
            user.ResetTokenExpires = DateTime.UtcNow.AddDays(1);
            await _context.SaveChangesAsync();

            var emailRequest = new EmailRequest
            {
                To = user.Email,
                Subject = "Reset Password",
                Body = CreateResetPasswordBody(user.Id, EncodeToken(user.PasswordResetToken))
            };

            await _emailService.SendEmailAsync(emailRequest);
            _logger.LogInformation($"forgot password email sent");
            return new ResponseBase() { IsSuccess = true, Message = "You may reset your password" };
        }

        public async Task<ResponseBase> ResetPasswordAsync(ResetPasswordRequest request)
        {
            if (string.IsNullOrEmpty(request.Email) || string.IsNullOrEmpty(request.NewPassword) ||
                string.IsNullOrEmpty(request.ResetCode))
            {
                return new ResponseBase() { IsSuccess = false, Message = "Please recheck input data" };
            }

            var user = _context.Users.FirstOrDefault(user => user.Email == request.Email);
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = "User not found" };
            }

            var decodedCode = DecodeToken(request.ResetCode);
            if (user.PasswordResetToken != decodedCode)
            {
                return new ResponseBase() { IsSuccess = false, Message = "Invalid token" };
            }
            if (DateTime.UtcNow >= user.ResetTokenExpires)
            {
                return new ResponseBase() { IsSuccess = false, Message = "Token expired" };
            }
            CreatePasswordHash(request.NewPassword, out byte[] passwordHash, out byte[] passwordSalt);
            user.PasswordHash = passwordHash;
            user.PasswordSalt = passwordSalt;
            user.PasswordResetToken = null;
            user.ResetTokenExpires = null;
            user.VerificationToken = CreateRandomToken();

            _context.Users.Update(user);
            await _context.SaveChangesAsync();

            //send another verification notification after password reset to notify user of the change
            if (user.Email != null)
            {
                SendConfirmationEmail(user.Email, user.Id, EncodeToken(user.VerificationToken));
                _logger.LogInformation($"Email after password reset sent");
            }
            return new ResponseBase() { IsSuccess = true, Message = "User password reset, please check email" };
        }

        public async Task<ResponseBase> UpdateUserAsync(UserUpdateDto userDto)
        {
            if (userDto.UserId == Guid.Empty)
            {
                return new ResponseBase() { IsSuccess = false, Message = "Id is required" };
            }
            var user = _context.Users.FirstOrDefault(user => user.Id == userDto.UserId);
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = "User not found" };
            }
            if (userDto.Email != null)
            {
                user.Email = userDto.Email;
                user.NormalizedEmail = userDto.Email.ToUpper();
                user.VerifiedAt = null;
                user.EmailConfirmed = false;

                if (user.Email != null)
                {
                    user.VerificationToken = CreateRandomToken();
                    await _context.SaveChangesAsync();

                    SendConfirmationEmail(user.Email, user.Id, EncodeToken(user.VerificationToken));
                    _logger.LogInformation($"reconfirm new email sent");
                }
            }
            if (userDto.UserName != null)
            {
                user.UserName = userDto.UserName;
                user.NormalizedUserName = userDto.UserName.ToUpper();
            }
            if (userDto.BirthYear != 0)
            {
                user.BirthYear = userDto.BirthYear;
            }
            _context.Users.Update(user);
            await _context.SaveChangesAsync();            
            return new ResponseBase() { IsSuccess = true, Message = $"User {user.Email} updated, if email updated, reverfication email sent" };

        }

        public async Task<ResponseBase> EnableTwoFactorAuthenticationAsync(Guid id)
        {
            var user = _context.Users.FirstOrDefault(user => user.Id == id);

            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = "User not found" };
            }

            user.TwoFactorEnabled = true;
            await _context.SaveChangesAsync();
            return new ResponseBase() { IsSuccess = true, Message = "Two factor enabled" };
        }

        public ResponseBase GetInfoAsync(Guid id)
        {
            if (id == Guid.Empty)
            {
                return new ResponseBase() { IsSuccess = false, Message = "User id is required" };
            }

            var user = _context.Users.FirstOrDefault(user => user.Id == id);
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = "User not found" };
            }
            return new ResponseBase() { IsSuccess = true, Message = $"Two factor enabled? {user.TwoFactorEnabled}" };
        }

        public LoginResponse LogoutAsync()
        {
            return new LoginResponse() { IsAuthenticated = false, IsSuccess = true, User = null, Message = "User logged out"};
        }
        
        //helper methods
        private void CreatePasswordHash(string password, out byte[] passwordHash, out byte[] passwordSalt)
        {
            using (var hmac = new HMACSHA512())
            {
                passwordSalt = hmac.Key;
                passwordHash = hmac.ComputeHash(Encoding.UTF8.GetBytes(password));
            }
        }

        private bool VerifyPasswordHash(string password, byte[] passwordHash, byte[] passwordSalt)
        {
            using (var hmac = new HMACSHA512(passwordSalt))
            {
                var computedHash = hmac.ComputeHash(Encoding.UTF8.GetBytes(password));
                return computedHash.SequenceEqual(passwordHash);
            }
        }

        private string CreateRandomToken()
        {
            return Convert.ToHexString(RandomNumberGenerator.GetBytes(64));
        }

        private string EncodeToken(string token)
        {
            var encodedToken = WebUtility.UrlEncode(token);
            return encodedToken;
        }

        private string DecodeToken(string? token)
        {
            var decodedToken = WebUtility.UrlDecode(token);
            if (decodedToken == null)
            {
                return "No token";
            }
            return decodedToken;
        }

        private string GenerateJwtToken(string email)
        {
            var key = _configuration["Jwt:Key"];
            var issuer = _configuration["Jwt:Issuer"];
            var audience = _configuration["Jwt:Audience"];
            var expires = _configuration["Jwt:ExpiresInMinutes"];

            SymmetricSecurityKey securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(key));
            SigningCredentials credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

            List<Claim> claims = new List<Claim>
                {
                    new Claim(ClaimTypes.Email, email),
                    new Claim(ClaimTypes.Role, "User"),
                };

            JwtSecurityToken token = new JwtSecurityToken(
                issuer: issuer,
                audience: audience,
                claims: claims,
                expires: DateTime.Now.AddMinutes(int.Parse(expires)),
                signingCredentials: credentials);

            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        private string CreateConfirmEmailBody(Guid id, string token)
        {
            return $"<a href='{_configuration["ConfirmEmailUrl"]}id={id}&token={token}'>Confirm your email</a>";
        }

        private string CreateResetPasswordBody(Guid id, string token)
        {
            return $"<a href='{_configuration["ResetPasswordUrl"]}id={id}&token={token}'>Reset your password</a>";
        }

        private void SendConfirmationEmail(string email, Guid id, string token)
        {
            var emailRequest = new EmailRequest
            {
                To = email,
                Subject = "Confirm Email",
                Body = CreateConfirmEmailBody(id, token)
            };
            _emailService.SendEmailAsync(emailRequest);
        }

        private async Task AddLoginRecordAsync(Guid userId, string? applicationName, string loginProvider, string providerKey)
        {
            var loginInfo = new LoginInfo
            {
                UserId = userId,
                LoginProvider = loginProvider,
                ProviderKey = providerKey,
                ApplicationName = applicationName,
                LoginTime = DateTime.UtcNow,
            };

            _context.Logins.Add(loginInfo);
            await _context.SaveChangesAsync();
        }
    }
}
