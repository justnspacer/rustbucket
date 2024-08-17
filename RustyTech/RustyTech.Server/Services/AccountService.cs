using Microsoft.AspNetCore.Identity.Data;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Net;
using System.Security.Claims;
using System.Text;
using RustyTech.Server.Models.Auth;
using System.Security.Cryptography;
using System.Text.RegularExpressions;
using RustyTech.Server.Services.Interfaces;
using RustyTech.Server.Interfaces;
using RustyTech.Server.Utilities;
using RustyTech.Server.Models.Dtos;
using Microsoft.AspNetCore.Identity;

namespace RustyTech.Server.Services
{
    public class AccountService : IAccountService
    {
        private readonly UserManager<User> _userManager;
        private readonly DataContext _context;
        private readonly IEmailService _emailService;
        private readonly IRoleService _roleService;
        private readonly IConfiguration _configuration;
        private readonly ILogger<IAccountService> _logger;

        public AccountService(UserManager<User> userManager,  DataContext context, IEmailService emailService, IRoleService roleService, IConfiguration configuration,
            ILogger<IAccountService> logger)
        {
            _userManager = userManager;
            _context = context;
            _emailService = emailService;
            _configuration = configuration;
            _logger = logger;
            _roleService = roleService;
        }

        public async Task<ResponseBase> Register(CustomRegisterRequest request)
        {
            var existingUserName = await _userManager.FindByNameAsync(request.UserName);
            if (existingUserName != null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.BadRequest };
            }

            if (!EmailValidator.IsValidEmail(request.Email))
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.InvalidEmail };
            }

            var existingEmail = await _userManager.FindByEmailAsync(request.Email);
            if (existingEmail != null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.BadRequest };
            }

            CreatePasswordHash(request.Password, out byte[] passwordHash, out byte[] passwordSalt);

            var user = new User
            {
                UserName = request.UserName,
                Email = request.Email,
                NormalizedEmail = request.Email.ToUpper(),
                NormalizedUserName = request.UserName.ToUpper(),
                PasswordHash = passwordHash,
                PasswordSalt = passwordSalt,
                BirthYear = request.BirthYear,
            };

            var token = await _userManager.GenerateEmailConfirmationTokenAsync(user);
            var encodedToken = EncodeToken(token);
            user.VerificationToken = token;
            await _userManager.CreateAsync(user);

            SendConfirmationEmail(user.Email, user.Id, token);
            _logger.LogInformation($"register email sent");

            return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.UserRegistered };
        }

        public async Task<LoginResponse> LoginAsync(Models.Auth.LoginRequest_old request)
        {
            var expires = _configuration["Jwt:ExpiresInMinutes"];
            var user = await _userManager.Users.FirstOrDefaultAsync(user => user.Email == request.Email);
            if (user == null)
            {
                return new LoginResponse() { IsAuthenticated = false, Message = Constants.Messages.Info.UserNotFound };
            }

            if (user.VerifiedAt == null)
            {
                return new LoginResponse() { IsAuthenticated = false, Message = Constants.Messages.Info.UserNotVerified };
            }

            if (!VerifyPasswordHash(request.Password, user.PasswordHash, user.PasswordSalt))
            {
                return new LoginResponse() { IsAuthenticated = false, Message = Constants.Messages.Error.InvalidCredentials };
            }
            await AddLoginRecordAsync(user.Id);
            var roles = await _userManager.GetRolesAsync(user);
            List<string> userRoles = new List<string>();
            foreach (var role in roles)
            {
                if (!string.IsNullOrEmpty(role))
                {
                    var addRole = await _roleService.GetRoleByIdAsync(role);
                    if (addRole != null && addRole.RoleName != null)
                    {
                        userRoles.Add(addRole.RoleName);
                    }
                }
            }
            var token = string.Empty;
            if (user.Email != null)
            {
                token = GenerateJwtToken(user.Id, user.Email, userRoles);
            }
            var userDto = new GetUserRequest
            {
                Id = user.Id,
                Email = user.Email,
            };

            return new LoginResponse() { IsAuthenticated = true, IsSuccess = true, User = userDto, Token = token };
        }

        public async Task<ResponseBase> VerifyEmail(VerifyEmailRequest request)
        {
            /*
            var decodedToken = DecodeToken(request.Token);
            if (decodedToken == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Token.Invalid };
            }
            */

            if (string.IsNullOrEmpty(request.Token))
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Token.Invalid };
            }

            var user = _userManager.Users.FirstOrDefault(user => user.VerificationToken == request.Token);
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Token.Invalid };
            }

            user.VerifiedAt = DateTime.UtcNow;
            user.EmailConfirmed = true;
            await _userManager.UpdateAsync(user);
            return new ResponseBase() { IsSuccess = true };
        }

        public ResponseBase VerifyJwtToken(string token)
        {
            var key = _configuration["Jwt:Key"];

            try
            {
                var jwtHandler = new JwtSecurityTokenHandler();
                var jwtToken = jwtHandler.ReadJwtToken(token);

                var expirationDate = jwtToken.ValidTo;
                var tokenKey = jwtToken.SecurityKey;

                var currentDate = DateTime.UtcNow;

                if (key == null)
                {
                    return new ResponseBase() { IsSuccess = false, Message = "No jwt key" };
                }

                SymmetricSecurityKey securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(key));

                if (currentDate > expirationDate && securityKey != tokenKey)
                {
                    return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Token.Invalid };
                }
                return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Token.Valid };
            }
            catch (Exception ex)
            {
                return new ResponseBase() { IsSuccess = false, Message = ex.Message };
            }
        }
        
        public async Task<ResponseBase> ResendEmailAsync(string email)
        {
            if (string.IsNullOrEmpty(email))
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.EmailRequired };
            }

            var user = await _userManager.FindByEmailAsync(email);
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.UserNotFound };
            }

            if (user.Email != null)
            {
                if (user.VerificationToken != null)
                {
                    SendConfirmationEmail(user.Email, user.Id, user.VerificationToken);
                    _logger.LogInformation($"resent confirmation email");
                }
            }
            return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.ResendEmail };
        }

        public async Task<ResponseBase> ForgotPasswordAsync(string email)
        {
            var user = await _userManager.FindByEmailAsync(email);
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.UserNotFound };
            }

            user.PasswordResetToken = CreateRandomToken();
            user.ResetTokenExpires = DateTime.UtcNow.AddDays(1);
            await _userManager.UpdateAsync(user);

            var emailRequest = new EmailRequest
            {
                To = user.Email,
                Subject = "Reset Password",
                Body = CreateResetPasswordBody(user.Id, EncodeToken(user.PasswordResetToken))
            };

            await _emailService.SendEmailAsync(emailRequest);
            _logger.LogInformation($"forgot password email sent");
            return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.UserPasswordReset };
        }

        public async Task<ResponseBase> ResetPasswordAsync(ResetPasswordRequest request)
        {
            if (string.IsNullOrEmpty(request.Email) || string.IsNullOrEmpty(request.NewPassword) ||
                string.IsNullOrEmpty(request.ResetCode))
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.DataRecheck };
            }

            if (!IsPasswordValid(request.NewPassword))
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.PasswordError };
            }

            var user = await _userManager.FindByEmailAsync(request.Email);
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.UserNotFound };
            }

            var decodedCode = DecodeToken(request.ResetCode);
            if (user.PasswordResetToken != decodedCode)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Token.Invalid };
            }
            if (DateTime.UtcNow >= user.ResetTokenExpires)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Token.Expired };
            }
            CreatePasswordHash(request.NewPassword, out byte[] passwordHash, out byte[] passwordSalt);
            user.PasswordHash = passwordHash;
            user.PasswordSalt = passwordSalt;
            user.PasswordResetToken = null;
            user.ResetTokenExpires = null;
            user.VerificationToken = await _userManager.GenerateEmailConfirmationTokenAsync(user);

            await _userManager.UpdateAsync(user);

            //send another verification notification after password reset to notify user of the change
            if (user.Email != null)
            {
                SendConfirmationEmail(user.Email, user.Id, user.VerificationToken);
                _logger.LogInformation($"Email after password reset sent");
            }
            return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.UserPasswordReset };
        }

        public async Task<ResponseBase> UpdateUserAsync(UpdateUserRequest userDto)
        {
            if (userDto.UserId == Guid.Empty)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.IdRequired };
            }
            var user = await _userManager.FindByIdAsync(userDto.UserId.ToString());
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.UserNotFound };
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

            if (userDto.Email != null)
            {
                user.Email = userDto.Email;
                user.NormalizedEmail = userDto.Email.ToUpper();
                user.VerifiedAt = null;
                user.EmailConfirmed = false;

                if (user.Email != null)
                {
                    user.VerificationToken = await _userManager.GenerateEmailConfirmationTokenAsync(user);
                    await _userManager.UpdateAsync(user);
                    SendConfirmationEmail(user.Email, user.Id, user.VerificationToken);
                    _logger.LogInformation($"reconfirm new email sent");
                }
            }
            await _userManager.UpdateAsync(user);
            return new ResponseBase() { IsSuccess = true, Message = "User updated, email reverifcation required" };
        }

        public async Task<ResponseBase> EnableTwoFactorAuthenticationAsync(Guid id)
        {
            var user = await _userManager.FindByIdAsync(id.ToString());

            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.UserNotFound };
            }

            user.TwoFactorEnabled = true;
            await _userManager.UpdateAsync(user);
            return new ResponseBase() { IsSuccess = true, Message = "Two factor enabled" };
        }

        public async Task<ResponseBase> GetInfoAsync(Guid id)
        {
            if (id == Guid.Empty)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.IdRequired };
            }

            var user = await _userManager.FindByIdAsync(id.ToString());
            if (user == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Info.UserNotFound };
            }
            return new ResponseBase() { IsSuccess = true, Message = $"Two factor enabled? {user.TwoFactorEnabled}" };
        }

        public LoginResponse LogoutAsync()
        {
            return new LoginResponse() { IsAuthenticated = false, IsSuccess = true, User = null, Message = Constants.Messages.Info.UserLoggedOut };
        }

        //helper methods
        public string GenerateJwtToken(Guid id, string email, List<string> userRoles)
        {
            var key = _configuration["Jwt:Key"];
            var issuer = _configuration["Jwt:Issuer"];
            var audience = _configuration["Jwt:Audience"];
            var expires = _configuration["Jwt:ExpiresInMinutes"];

            //need a key and expiration time to generate token
            if (key != null && expires != null)
            {
                SymmetricSecurityKey securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(key));
                SigningCredentials credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

                List<Claim> claims = new List<Claim>
                {
                new Claim(ClaimTypes.NameIdentifier, id.ToString()),
                new Claim(ClaimTypes.Email, email),
                new Claim(ClaimTypes.Role, string.Join(",", userRoles)),
                };

                JwtSecurityToken token = new JwtSecurityToken(
                    issuer: issuer,
                    audience: audience,
                    claims: claims,
                    expires: DateTime.UtcNow.AddMinutes(int.Parse(expires)),
                    signingCredentials: credentials);

                return new JwtSecurityTokenHandler().WriteToken(token);

            }
            return "Error generating token";
        }

        public void CreatePasswordHash(string password, out byte[] passwordHash, out byte[] passwordSalt)
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
                return Constants.Messages.Token.Invalid;
            }
            return decodedToken;
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

        private async Task AddLoginRecordAsync(Guid userId)
        {
            var loginInfo = new LoginInfo
            {
                UserId = userId,
                LoginTime = DateTime.UtcNow,
            };

            _context.Logins.Add(loginInfo);
            await _context.SaveChangesAsync();
        }

        private bool IsPasswordValid(string password)
        {
            string pattern = Constants.PasswordRegex.Pattern;
            Regex regex = new Regex(pattern);
            return regex.IsMatch(password);
        }
    }
}
