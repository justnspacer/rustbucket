using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.Data;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Net;
using System.Security.Claims;
using System.Text;
using RustyTech.Server.Models.Auth;
using System.Security.Cryptography;
using System.Data.Entity;
using RustyTech.Server.Models.Role;

namespace RustyTech.Server.Services
{
    public class AuthService
    {
        private readonly IEmailService _emailService;
        private readonly IConfiguration _configuration;
        private readonly ILogger<UserService> _logger;
        private readonly DataContext _context;
        private readonly RoleService _roleService;

        public AuthService(IEmailService emailService, IConfiguration configuration,
            ILogger<UserService> logger, DataContext context , RoleService roleService)
        {
            _emailService = emailService;
            _configuration = configuration;
            _logger = logger;
            _context = context;
            _roleService = roleService;
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
                NormalizedEmail = request.Email.ToUpper(),
                NormalizedUserName = request.Email.ToUpper(),
                PasswordHash = passwordHash,
                PasswordSalt = passwordSalt,
                VerificationToken = CreateRandomToken(),
                BirthYear = request.BirthYear,
            };

            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            if (user.Email == "admin@rustbucket.io")
            {
                user.VerifiedAt = DateTime.UtcNow;
                var roleRequest = new RoleRequest() { RoleName = "Admin", UserId = user.Id };
                await _roleService.AddRoleToUserAsync(roleRequest);
            }

            SendConfirmationEmail(user.Email, user.Id, EncodeToken(user.VerificationToken));
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
            if (user == null)
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
            var decodedToken = WebUtility.UrlDecode(request.Token);
            if (decodedToken == null)
            {
                return "TokenFailure";
            }
            var user = await _context.Users.FirstOrDefaultAsync(user => user.VerificationToken == decodedToken);
            if (user == null)
            {
                return "Invalid token";
            }

            user.VerificationToken = null;
            user.VerifiedAt = DateTime.UtcNow;
            user.EmailConfirmed = true;
            await _context.SaveChangesAsync();

            return $"User verified at: {user.VerifiedAt}";
        }

        public async Task<string> ResendEmailAsync(string email)
        {
            if (string.IsNullOrEmpty(email))
            {
                return "Email is required";
            }

            var user = await _context.Users.FirstOrDefaultAsync(user => user.Email == email);
            if (user == null)
            {
                return "User not found";
            }

            if (user.Email != null)
            {
                if (user.VerificationToken != null)
                {
                    SendConfirmationEmail(user.Email, user.Id, EncodeToken(user.VerificationToken));
                    _logger.LogInformation($"resent confirmation email");
                }else
                {
                    user.VerificationToken = CreateRandomToken();
                    await _context.SaveChangesAsync();
                    SendConfirmationEmail(user.Email, user.Id, EncodeToken(user.VerificationToken));
                    _logger.LogInformation($"resent confirmation email");
                }
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
            return "You may reset your password";
        }

        public async Task<string> UpdateUserAsync(UserUpdateDto userDto)
        {
            if (userDto.UserId == Guid.Empty)
            {
                return "Id is required";
            }
            var user = await _context.Users.FirstOrDefaultAsync(user => user.Id == userDto.UserId);
            if (user == null)
            {
                return "User not found";
            }
            if(userDto.Email != null)
            {
                user.Email = userDto.Email;
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
            }
            if (userDto.BirthYear != 0)
            {
                user.BirthYear = userDto.BirthYear;
            }
            _context.Users.Update(user);
            await _context.SaveChangesAsync();            
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

            var user = await _context.Users.FirstOrDefaultAsync(user => user.Email == request.Email);
            if (user == null)
            {
                return "user not found";
            }

            var decodedCode = WebUtility.UrlDecode(request.ResetCode);
            if (user.PasswordResetToken != decodedCode)
            {
                return "Invalid token";
            }
            if (DateTime.UtcNow >= user.ResetTokenExpires)
            {
                return "Token expired";
            }
            CreatePasswordHash(request.NewPassword, out byte[] passwordHash, out byte[] passwordSalt);
            user.PasswordHash = passwordHash;
            user.PasswordSalt = passwordSalt;
            user.PasswordResetToken = null;
            user.ResetTokenExpires = null;

            _context.Users.Update(user);
            await _context.SaveChangesAsync();

            return "User password reset";
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

        public (bool IsAuthenticated, User? User, string? token, string Message) LogoutAsync()
        {
            return (false, null, null, "User should be logged out");
        }

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

        private string EncodeToken(string token)
        {
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
