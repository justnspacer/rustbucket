using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Net;
using System.Security.Claims;
using System.Text;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Models.User;
using RustyTech.Server.Data;

namespace RustyTech.Server.Services
{
    /// <summary>
    /// Service class for handling authentication and authorization operations.
    /// </summary>
    public class AuthService
    {
        private readonly UserManager<User> _userManager;
        private readonly IEmailService _emailService;
        private readonly SignInManager<User> _signInManager;
        private readonly IConfiguration _configuration;
        private readonly ILogger<UserService> _logger;
        private readonly DataContext _context;
        private readonly IHttpContextAccessor _httpContextAccessor;

        public AuthService(UserManager<User> user, IEmailService emailService,
            SignInManager<User> signInManager, IConfiguration configuration,
            ILogger<UserService> logger, DataContext context, IHttpContextAccessor httpContextAccessor)
        {
            _userManager = user;
            _emailService = emailService;
            _signInManager = signInManager;
            _configuration = configuration;
            _logger = logger;
            _context = context;
            _httpContextAccessor = httpContextAccessor;
        }

        /// <summary>
        /// Registers a new user.
        /// </summary>
        /// <param name="model">The user registration model.</param>
        /// <returns>The result of the registration operation.</returns>
        public async Task<IdentityResult> RegisterAsync([FromBody] UserRegister model)
        {
            if (string.IsNullOrWhiteSpace(model.Email) || string.IsNullOrWhiteSpace(model.Password))
            {
                return CreateFailureResult("EmailRequired");
            }

            var user = new User
            {
                UserName = model.Email,
                Email = model.Email
            };

            var result = await _userManager.CreateAsync(user, model.Password);

            var token = await GenerateEmailToken(user);
            SendConfirmationEmail(user.Email, user.Id, token);
            _logger.LogInformation($"register email sent");

            return result.Succeeded ? 
                IdentityResult.Success : 
                IdentityResult.Failed(result.Errors.Select(x => new IdentityError { Code = x.Code, Description = x.Description }).ToArray());
        }

        /// <summary>
        /// Logs in a user.
        /// </summary>
        /// <param name="model">The user login model.</param>
        /// <returns>The result of the login operation.</returns>
        public async Task<AuthResult> LoginAsync([FromBody] UserLogin model)
        {
            if (string.IsNullOrWhiteSpace(model.Email) || string.IsNullOrWhiteSpace(model.Password) || string.IsNullOrWhiteSpace(model.ApplicationName))
            {
                _logger.LogInformation($"login failed for {model.Email}");
                return CreateFailureResult();
            }

            var result = await _signInManager.PasswordSignInAsync(model.Email, model.Password, model.RememberMe, false);
            if (result.Succeeded)
            {
                await AddLoginRecordAsync(model.Email, model.ApplicationName, model.LoginProvider, model.ProviderKey);
                var token = GenerateJwtToken(model.Email);
                return new AuthResult { Succeeded = true, Token = token, Errors = null };
            }
            return CreateFailureResult();
        }

        /// <summary>
        /// Adds a login record for a user.
        /// </summary>
        /// <param name="email">The user's email.</param>
        /// <param name="applicationName">The name of the application.</param>
        /// <param name="loginProvider">Login provider of login attempt.</param>
        /// <param name="providerKey">Provider key for user.</param>
        /// <returns>The result of the add login record operation.</returns>
        public async Task<IdentityResult> AddLoginRecordAsync(string email, string? applicationName, string loginProvider, string providerKey)
        {
            if (string.IsNullOrEmpty(email))
            {
                return CreateFailureResult("EmailRequired");
            }

            var user = await _userManager.FindByEmailAsync(email);
            if (user == null)
            {
                return CreateFailureResult("UserNotFound");
            }

            var login = new UserLoginInfo(loginProvider, providerKey, applicationName);
            /*
            var identityuserlogin = new IdentityUserLogin<string>
            {
                UserId = user.Id,
                ProviderDisplayName = login.ProviderDisplayName,
                LoginProvider = login.LoginProvider,
                ProviderKey = login.ProviderKey,
            };
            */
            //_context.UserLogins.Add(identityuserlogin);
            _context.SaveChanges();
            return IdentityResult.Success;
        }

        /// <summary>
        /// Confirms a user's email.
        /// </summary>
        /// <param name="model">The confirm email request model.</param>
        /// <returns>The result of the confirm email operation.</returns>
        public async Task<IdentityResult> ConfirmEmailAsync(ConfirmEmailRequest model)
        {
            if (string.IsNullOrWhiteSpace(model.Id) || string.IsNullOrWhiteSpace(model.Token))
            {
                return CreateFailureResult("IdOrTokenRequired");
            }

            var decodedToken = WebUtility.UrlDecode(model.Token);
            if (decodedToken == null)
            {
                return CreateFailureResult("TokenFailure");
            }

            var user = await _userManager.FindByIdAsync(model.Id);
            if (user == null)
            {
                return CreateFailureResult("UserNotFound");
            }

            var result = await _userManager.ConfirmEmailAsync(user, decodedToken);
            return result.Succeeded ? IdentityResult.Success : CreateFailureResult("ConfirmEmailFailure");
        }

        /// <summary>
        /// Resends the confirmation email for a user.
        /// </summary>
        /// <param name="email">The user's email.</param>
        /// <returns>The result of the resend email operation.</returns>
        public async Task<IdentityResult> ResendEmailAsync(string email)
        {
            if (string.IsNullOrEmpty(email))
            {
                return CreateFailureResult("EmailRequired");
            }

            var user = await _userManager.FindByEmailAsync(email);
            if (user == null)
            {
                return CreateFailureResult("UserNotFound");
            }

            if (user.Email != null)
            {
                var token = await GenerateEmailToken(user);
                SendConfirmationEmail(user.Email, user.Id, token);
                _logger.LogInformation($"resent confirmation email");
            }
            return IdentityResult.Success;
        }

        /// <summary>
        /// Sends a password reset email to a user.
        /// </summary>
        /// <param name="email">The user's email.</param>
        /// <returns>The result of the forgot password operation.</returns>
        public async Task<IdentityResult> ForgotPasswordAsync(string email)
        {
            if (string.IsNullOrEmpty(email))
            {
                return CreateFailureResult("EmailRequired");
            }

            var user = await _userManager.FindByEmailAsync(email);
            if (user == null)
            {
                return CreateFailureResult("UserNotFound");
            }

            var token = await GeneratePasswordToken(user);
            var emailRequest = new EmailRequest
            {
                To = user.Email,
                Subject = "Reset Password",
                Body = CreateRestPasswordBody(user.Id, token)
            };
            await _emailService.SendEmailAsync(emailRequest);
            _logger.LogInformation($"forgot password email sent");
            return IdentityResult.Success;
        }

        /// <summary>
        /// Updates a user asynchronously.
        /// </summary>
        /// <param name="id">UserId.</param>
        /// <param name="userUpdateDto">User update object</param>
        /// <returns>An IdentityResult indicating the success or failure of the update operation.</returns>
        public async Task<IdentityResult> UpdateUserAsync(string id, UserUpdate userUpdateDto)
        {
            if (string.IsNullOrEmpty(id))
            {
                return CreateFailureResult("IdRequired");
            }
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
            {
                return CreateFailureResult("UserNotFound");
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
            return result;
        }

        /// <summary>
        /// Resets a user's password.
        /// </summary>
        /// <param name="model">The reset password request model.</param>
        /// <returns>The result of the reset password operation.</returns>
        public async Task<IdentityResult> ResetPasswordAsync([FromBody] ResetPasswordRequest model)
        {
            // Check if email, new password, and reset code are provided
            if (string.IsNullOrEmpty(model.Email) || string.IsNullOrEmpty(model.NewPassword) ||
                string.IsNullOrEmpty(model.ResetCode))
            {
                return CreateFailureResult("EmailRequired");
            }

            var user = await _userManager.FindByEmailAsync(model.Email);
            if (user == null)
            {
                return CreateFailureResult("UserNotFound");
            }

            var decodedCode = WebUtility.UrlDecode(model.ResetCode);
            var result = await _userManager.ResetPasswordAsync(user, decodedCode, model.NewPassword);
            return result.Succeeded ? IdentityResult.Success : CreateFailureResult("ResetPasswordFailure");
        }

        /// <summary>
        /// Enables two-factor authentication for a user.
        /// </summary>
        /// <param name="id">The user's ID.</param>
        /// <returns>The result of the enable 2FA operation.</returns>
        public async Task<IdentityResult> Enable2faAsync(string id)
        {
            // Check if ID is provided
            if (string.IsNullOrEmpty(id))
            {
                return CreateFailureResult("IdRequired");
            }

            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
            {
                return CreateFailureResult("UserNotFound");
            }

            var result = await _userManager.SetTwoFactorEnabledAsync(user, true);
            return result.Succeeded ? IdentityResult.Success : CreateFailureResult("Enable2faFailure");
        }

        /// <summary>
        /// Gets the two-factor authentication status for a user.
        /// </summary>
        /// <param name="id">The user's ID.</param>
        /// <returns>True if two-factor authentication is enabled, otherwise false.</returns>
        public async Task<bool> GetInfoAsync(string id)
        {
            // Check if ID is provided
            if (string.IsNullOrEmpty(id))
            {
                return false;
            }

            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
            {
                return false;
            }

            var result = await _userManager.GetTwoFactorEnabledAsync(user);
            return result;
        }

        /// <summary>
        /// Changes a user's password.
        /// </summary>
        /// <param name="model">The change password request model.</param>
        /// <returns>The result of the change password operation.</returns>
        public async Task<IdentityResult> ChangePasswordAsync([FromBody] ChangePasswordRequest model)
        {
            // Check if email, old password, and new password are provided
            if (string.IsNullOrWhiteSpace(model.Email) ||
                string.IsNullOrWhiteSpace(model.OldPassword) || string.IsNullOrWhiteSpace(model.NewPassword))
            {
                return CreateFailureResult("EmailRequired");
            }

            var user = await _userManager.FindByEmailAsync(model.Email);
            if (user == null)
            {
                return CreateFailureResult("UserNotFound");
            }

            var result = await _userManager.ChangePasswordAsync(user, model.OldPassword, model.NewPassword);
            return result.Succeeded ? IdentityResult.Success : CreateFailureResult("ChangePasswordFailure");
        }

        /// <summary>
        /// Logs out the current user.
        /// </summary>
        /// <returns>The result of the logout operation.</returns>
        public async Task<IdentityResult> LogoutAsync()
        {
            await _signInManager.SignOutAsync().ConfigureAwait(false);
            return IdentityResult.Success;
        }

        private string GenerateJwtToken(string email)
        {
            var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]));
            var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

            var claims = new List<Claim>
                {
                    new Claim(ClaimTypes.Email, email)
                };

            var token = new JwtSecurityToken(
                issuer: _configuration["Jwt:Issuer"],
                audience: _configuration["Jwt:Audience"],
                claims: claims,
                expires: DateTime.Now.AddMinutes(int.Parse(_configuration["Jwt:ExpiresInMinutes"])),
                signingCredentials: credentials);

            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        private IdentityResult CreateFailureResult(string code)
        {
            return IdentityResult.Failed(new IdentityError { Code = code, Description = Constants.Message.InvalidRequest });
        }

        private AuthResult CreateFailureResult()
        {
            return new AuthResult { Succeeded = false, Errors = new List<string> { "Authentication failed" }, Token = null };
        }

        private string CreateConfirmEmailBody(Guid id, string token)
        {
            return $"<a href='{_configuration["ConfirmEmailUrl"]}id={id}&token={token}'>Confirm your email</a>";
        }

        private string CreateRestPasswordBody(Guid id, string token)
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
