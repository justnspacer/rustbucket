using Microsoft.AspNetCore.Identity;
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
        private readonly UserManager<User> _userManager;
        private readonly IEmailService _emailService;
        private readonly IConfiguration _configuration;
        private readonly ILogger<UserService> _logger;
        private readonly DataContext _context;

        public AuthService(UserManager<User> user, IEmailService emailService, IConfiguration configuration,
            ILogger<UserService> logger, DataContext context)
        {
            _userManager = user;
            _emailService = emailService;
            _configuration = configuration;
            _logger = logger;
            _context = context;
        }

        public async Task<(bool IsSuccess, string Message, User? User)> RegisterAsync(UserRegister request)
        {
            if (_context.Users.Any(user => user.Email == request.Email))
            {
                return (false, "User already exists.", null);
            }

            CreatePasswordHash(request.Password, out byte[] passwordHash, out byte[] passwordSalt);

            var user = new User
            {
                UserName = request.Email,
                Email = request.Email,
                PasswordHash = passwordHash,
                PasswordSalt = passwordSalt,
                VerificationToken = CreateRandomToken(),
                BirthYear = request.BirthYear,
            };

            _context.Users.Add(user);
            await _context.SaveChangesAsync();


            var emailToken = await GenerateEmailToken(user);
            SendConfirmationEmail(user.Email, user.Id, emailToken);
            _logger.LogInformation($"register email sent");

            return (true, "User registered successfully.", user);
        }

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

        public async Task<(bool IsAuthenticated, User? User, string? token, string Message)> LoginAsync(UserLogin request)
        {
            var user = await _context.Users.FirstOrDefaultAsync(user => user.Email == request.Email);
            if (user == null || !await _userManager.CheckPasswordAsync(user, request.Password))
            {
                return (false, null, null, "Invalid credentials");
            }

            if (user.VerifiedAt == null)
            {
                return (false, null, null, "Not verified");
            }

            if (!VerifyPasswordHash(request.Password, user.PasswordHash, user.PasswordSalt))
            {
                return (false, null, null, "Invalid credentials");
            }
            await AddLoginRecordAsync(user.Id, "RustyTech", "Email", string.Empty);
            var token = GenerateJwtToken(request.Email);
            return (true, user, token, "Login successful");
        }

        public async Task AddLoginRecordAsync(Guid userId, string? applicationName, string loginProvider, string providerKey)
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

        public async Task<string> VerifyEmail(ConfirmEmailRequest request)
        {
            var user = await _context.Users.FirstOrDefaultAsync(user => user.VerificationToken == request.Token);
            if (user == null)
            {
                return "Invalid token";
            }
            //address
            var decodedToken = WebUtility.UrlDecode(request.Token);
            if (decodedToken == null)
            {
                return "TokenFailure";
            }

            user.VerifiedAt = DateTime.UtcNow;
            await _context.SaveChangesAsync();

            return $"User verified at: {user.VerifiedAt}";
        }

        public async Task<string> ResendEmailAsync(string email)
        {
            if (string.IsNullOrEmpty(email))
            {
                return "Email is required";
            }

            var user = await _userManager.FindByEmailAsync(email);
            if (user == null)
            {
                return "User not found";
            }

            if (user.Email != null)
            {
                var token = await GenerateEmailToken(user);
                SendConfirmationEmail(user.Email, user.Id, token);
                _logger.LogInformation($"resent confirmation email");
            }
            return "Resent confirmation email with new token";
        }

        public async Task<string> ForgotPasswordAsync(string email)
        {
            var user = await _context.Users.FirstOrDefaultAsync(user => user.Email == email);
            if (user == null)
            {
                return "User not found";
            }

            user.PasswordResetToken = await GeneratePasswordToken(user);
            user.ResetTokenExpires = DateTime.UtcNow.AddDays(1);
            await _context.SaveChangesAsync();

            var emailRequest = new EmailRequest
            {
                To = user.Email,
                Subject = "Reset Password",
                Body = CreateResetPasswordBody(user.Id, user.PasswordResetToken)
            };

            await _emailService.SendEmailAsync(emailRequest);
            _logger.LogInformation($"forgot password email sent");
            return "You may reset your password";
        }

        public async Task<string> UpdateUserAsync(string id, UserUpdate userUpdateDto)
        {
            if (string.IsNullOrEmpty(id))
            {
                return "Id is required";
            }
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
            {
                return "User not found";
            }
            if(userUpdateDto.Email != null)
            {
                user.Email = userUpdateDto.Email;
                user.VerifiedAt = null;

                if (user.Email != null)
                {
                    var token = await GenerateEmailToken(user);
                    SendConfirmationEmail(user.Email, user.Id, token);
                    _logger.LogInformation($"reconfirm new email sent");
                }
            }
            if (userUpdateDto.UserName != null)
            {
                user.UserName = userUpdateDto.UserName;
            }
            var result = await _userManager.UpdateAsync(user);
            _context.SaveChanges();            
            return $"User {user.Email} updated";
        }

        public async Task<string> ResetPasswordAsync(ResetPasswordRequest request)
        {
            // Check if email, new password, and reset code are provided
            if (string.IsNullOrEmpty(request.Email) || string.IsNullOrEmpty(request.NewPassword) ||
                string.IsNullOrEmpty(request.ResetCode))
            {
                return "Email is required";
            }

            var user = await _userManager.FindByEmailAsync(request.Email);
            if (user == null)
            {
                return "user not found";
            }

            var decodedCode = WebUtility.UrlDecode(request.ResetCode);
            var result = await _userManager.ResetPasswordAsync(user, decodedCode, request.NewPassword);
            return result.Succeeded ? "password reset" : "password reset failed";
        }

        public async Task<bool> EnableTwoFactorAuthenticationAsync(Guid id)
        {
            var user = await _context.Users.FirstOrDefaultAsync(user => user.Id == id);

            if (user == null)
            {
                return false;
            }

            user.TwoFactorEnabled = true;
            await _context.SaveChangesAsync();

            return true;
        }

        public async Task<bool> GetInfoAsync(Guid id)
        {

            if (id == Guid.Empty)
            {
                return false;
            }

            var user = await _context.Users.FirstOrDefaultAsync(user => user.Id == id);
            if (user == null)
            {
                return false;
            }
            return user.TwoFactorEnabled;
        }

        public async Task<string> ChangePasswordAsync(ChangePasswordRequest request)
        {
            var user = await _context.Users.FirstOrDefaultAsync(user => user.PasswordResetToken == request.Token);
            if (user == null || user.ResetTokenExpires < DateTime.UtcNow)
            {
                return "Invalid token";
            }

            CreatePasswordHash(request.Password, out byte[] passwordHash, out byte[] passwordSalt);
            user.PasswordHash = passwordHash;
            user.PasswordSalt = passwordSalt;
            user.PasswordResetToken = null;
            user.ResetTokenExpires = null;

            await _context.SaveChangesAsync();

            return "Password changed";
        }

        public (bool IsAuthenticated, User? User, string? token, string Message) LogoutAsync()
        {
            return (false, null, null, "User should be logged out");
        }

        //updated
        private string GenerateJwtToken(string email)
        {
            var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]));
            var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

            var claims = new List<Claim>
                {
                    new Claim(ClaimTypes.Email, email),
                    new Claim(ClaimTypes.Role, "User"),
                };

            var token = new JwtSecurityToken(
                issuer: _configuration["Jwt:Issuer"],
                audience: _configuration["Jwt:Audience"],
                claims: claims,
                expires: DateTime.Now.AddMinutes(int.Parse(_configuration["Jwt:ExpiresInMinutes"])),
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

        private async Task<string> GenerateEmailToken(User user)
        {
            var token = await _userManager.GenerateEmailConfirmationTokenAsync(user);
            var encodedToken = WebUtility.UrlEncode(token);
            return encodedToken;
        }

        private async Task<string> GeneratePasswordToken(User user)
        {
            var token = await _userManager.GeneratePasswordResetTokenAsync(user);
            var encodedToken = WebUtility.UrlEncode(token);
            return encodedToken;
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
    }
}
