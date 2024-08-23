using System.Net;
using RustyTech.Server.Models.Account;
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
        private readonly SignInManager<User> _signInManager;
        private readonly IEmailService _emailService;
        private readonly IRoleService _roleService;
        private readonly IConfiguration _configuration;
        private readonly ILogger<IAccountService> _logger;

        public AccountService(UserManager<User> userManager, 
            SignInManager<User> signInManager, 
            IEmailService emailService, 
            IRoleService roleService, 
            IConfiguration configuration,
            ILogger<IAccountService> logger)
        {
            _userManager = userManager;
            _signInManager = signInManager;
            _emailService = emailService;
            _configuration = configuration;
            _logger = logger;
            _roleService = roleService;
        }

        public async Task<ResponseBase> Register(CustomRegisterRequest request)
        {
            var existingUserName = await _userManager
                .FindByNameAsync(request.UserName);

            if (existingUserName != null)
            {
                return new ResponseBase()
                {
                    IsSuccess = false,
                    Message = "Username already exists"
                };
            }

            if (!EmailValidator.IsValidEmail(request.Email))
            {
                return new ResponseBase()
                {
                    IsSuccess = false,
                    Message = Constants.Messages.Error.InvalidEmail
                };
            }

            var existingEmail = await _userManager
                .FindByEmailAsync(request.Email);

            if (existingEmail != null)
            {
                return new ResponseBase()
                {
                    IsSuccess = false,
                    Message = Constants.Messages.Error.BadRequest
                };
            }

            var user = new User
            {
                UserName = request.UserName,
                Email = request.Email,
                NormalizedEmail = request.Email.ToUpper(),
                NormalizedUserName = request.UserName.ToUpper(),
                BirthYear = request.BirthYear,
            };

            user.VerificationToken = await _userManager.GenerateEmailConfirmationTokenAsync(user);

            var result = await _userManager.CreateAsync(user, request.Password);
            if (!result.Succeeded)
            {
                return new ResponseBase()
                {
                    IsSuccess = false,
                    Message = result.Errors.Select(e => e.Description).FirstOrDefault()
                };
            }
            SendConfirmationEmail(user.Email, user.Id, WebUtility.UrlEncode(user.VerificationToken));
            _logger.LogInformation($"register email sent");

            return new ResponseBase()
            {
                IsSuccess = true,
                Message = Constants.Messages.Info.UserRegistered
            };
        }

        public async Task<LoginResponse> Login(CustomLoginRequest request)
        {
            var user = await _userManager.FindByEmailAsync(request.Email);
            if (user == null)
            {
                return UserNotFoundResponse();
            }
            if (user.VerifiedAt == null || user.VerifiedAt == DateTime.MinValue)
            {
                return new LoginResponse()
                {
                    IsAuthenticated = false,
                    Message = Constants.Messages.Info.UserNotVerified
                };
            }

            if (user != null)
            {
                var result = await _signInManager.PasswordSignInAsync(user, request.Password, isPersistent: request.RememberMe, lockoutOnFailure: true);
                if (result.Succeeded)
                {
                    var userDto = new GetUserRequest
                    {
                        Id = user.Id,
                        Email = user.Email,
                    };
                    await AddLoginRecord(user);
                    await _userManager.SetLockoutEnabledAsync(user, false);
                    user.AccessFailedCount = 0;
                    user.LockoutEnd = null;
                    await _userManager.UpdateAsync(user);
                    return new LoginResponse() { IsAuthenticated = true, IsSuccess = true, User = userDto };
                }
                else if (result.IsLockedOut)
                {
                    return new LoginResponse() { IsAuthenticated = false, IsSuccess = false, Message = "User is locked out, please try again later" };
                }
                else if (result.RequiresTwoFactor)
                {
                    return new LoginResponse() { IsAuthenticated = false, IsSuccess = false, Message = "User requires two factor auth" };
                }
                else if (result.IsNotAllowed)
                {
                    return new LoginResponse() { IsAuthenticated = false, IsSuccess = false, Message = "User not verified" };
                }
                else
                {
                    if (user.AccessFailedCount == 5)//from program.cs
                    {
                        await _userManager.AccessFailedAsync(user);
                        await _userManager.SetLockoutEnabledAsync(user, true);
                        return new LoginResponse() { IsAuthenticated = false, IsSuccess = false, Message = "User is locked out, please try again later" };
                    }
                    else
                    {
                        await _userManager.AccessFailedAsync(user);
                        return new LoginResponse() { IsAuthenticated = false, IsSuccess = false, Message = "User login error" };
                    }
                }
            }
            return new LoginResponse()
            {
                IsAuthenticated = false,
                IsSuccess = false,
                Message = Constants.Messages.Error.InvalidCredentials
            };
        }

        public async Task<ResponseBase> VerifyEmail(VerifyEmailRequest request)
        {            
            if (string.IsNullOrEmpty(request.Token))
            {
                return InvalidTokenResponse();
            }
            var decodedToken = WebUtility.UrlDecode(request.Token);
            var user = _userManager.Users
                .FirstOrDefault(user => user.VerificationToken == decodedToken);

            if (user == null)
            {
                return UserNotFoundResponse();
            }

            user.VerifiedAt = DateTime.UtcNow;
            var result = await _userManager.ConfirmEmailAsync(user, decodedToken);
            if (!result.Succeeded)
            {
                return new ResponseBase() { IsSuccess = false, Message = result.Errors.Select(e => e.Description).FirstOrDefault() };
            }
            await _userManager.SetLockoutEnabledAsync(user, false);
            await _userManager.UpdateAsync(user);
            return new ResponseBase() { IsSuccess = true, Message = "User email verified" };
        }

        public async Task<ResponseBase> ResendEmail(string email)
        {
            if (string.IsNullOrEmpty(email))
            {
                return new ResponseBase()
                {
                    IsSuccess = false,
                    Message = Constants.Messages.EmailRequired
                };
            }

            var user = await _userManager.FindByEmailAsync(email);
            if (user == null)
            {
                return UserNotFoundResponse();
            }

            if (user.Email != null)
            {
                if (user.VerificationToken != null)
                {
                    var newtoken = await _userManager.GenerateEmailConfirmationTokenAsync(user);
                    user.VerificationToken = newtoken;
                    await _userManager.UpdateAsync(user);
                    SendConfirmationEmail(user.Email, user.Id, WebUtility.UrlEncode(newtoken));
                    _logger.LogInformation($"resent confirmation email");
                }
            }
            return new ResponseBase()
            {
                IsSuccess = true,
                Message = Constants.Messages.Info.ResendEmail
            };
        }

        public async Task<ResponseBase> ForgotPassword(string email)
        {
            var tokenExpiry = _configuration["ResetTokenExpiresInDays"];
            var user = await _userManager.FindByEmailAsync(email);
            if (user == null)
            {
                return UserNotFoundResponse();
            }
            if (tokenExpiry != null)
            {
                user.PasswordResetToken = await _userManager.GeneratePasswordResetTokenAsync(user);
                user.ResetTokenExpires =
                    DateTime.UtcNow.AddDays(int.Parse(tokenExpiry));
                await _userManager.UpdateAsync(user);
                var emailRequest = new EmailRequest
                {
                    To = user.Email,
                    Subject = "Reset Password",
                    Body = CreateResetPasswordBody(user.Id, WebUtility.UrlEncode(user.PasswordResetToken))
                };

                await _emailService.SendEmailAsync(emailRequest);
                _logger.LogInformation($"forgot password email sent");
                return new ResponseBase()
                {
                    IsSuccess = true,
                    Message = Constants.Messages.Info.UserPasswordReset
                };
            }
            return new ResponseBase()
            {
                IsSuccess = false,
                Message = "Token expiration needed"
            };
        }

        public async Task<ResponseBase> ResetPassword(CustomResetPasswordRequest request)
        {            
            if (!IsPasswordValid(request.NewPassword))
            {
                return PasswordErrorResponse();
            }           

            var user = await _userManager.FindByEmailAsync(request.Email);
            if (user == null)
            {
                return UserNotFoundResponse();
            }

            var decodedCode = WebUtility.UrlDecode(request.ResetCode);
            if (user.PasswordResetToken != decodedCode)
            {
                return InvalidTokenResponse();
            }
            if (DateTime.UtcNow >= user.ResetTokenExpires || user.ResetTokenExpires == DateTime.MinValue )
            {
                return new ResponseBase()
                {
                    IsSuccess = false,
                    Message = Constants.Messages.Token.Expired
                };
            }
            
            var result = await _userManager.ResetPasswordAsync(user, decodedCode, request.NewPassword);
            if (result.Succeeded)
            {
                user.PasswordResetToken = null;
                user.ResetTokenExpires = null;
                await _userManager.UpdateAsync(user);
                return new ResponseBase()
                {
                    IsSuccess = true,
                    Message = Constants.Messages.Info.UserPasswordChanged
                };
            }            
            return new ResponseBase()
            {
                IsSuccess = false,
                Message = result.Errors.ToString()
            };
        }

        public async Task<ResponseBase> UpdateUser(UpdateUserRequest userDto)
        {
            if (userDto.UserId == null)
            {
                return IdRequiredResponse();
            }
            var user = await _userManager.FindByIdAsync(userDto.UserId);
            if (user == null)
            {
                return UserNotFoundResponse();
            }

            if (userDto.UserName != null)
            {
                var existingUserName = await _userManager.FindByNameAsync(userDto.UserName);
                if (existingUserName != null)
                {
                    return new ResponseBase()
                    {
                        IsSuccess = false,
                        Message = "Username already exists"
                    };
                }
                user.UserName = userDto.UserName;
                await _userManager.UpdateNormalizedUserNameAsync(user);
            }

            if (userDto.BirthYear != 0)
            {
                user.BirthYear = userDto.BirthYear;
            }

            if (userDto.Email != null)
            {
                user.Email = userDto.Email;
                await _userManager.UpdateNormalizedEmailAsync(user);
                user.VerifiedAt = null;
                user.EmailConfirmed = false;

                if (user.Email != null)
                {
                    user.VerificationToken = await _userManager.GenerateEmailConfirmationTokenAsync(user);
                    SendConfirmationEmail(user.Email, user.Id, WebUtility.UrlEncode(user.VerificationToken));
                    _logger.LogInformation($"email reverification sent");
                    await _userManager.UpdateAsync(user);
                    return new ResponseBase()
                    {
                        IsSuccess = true,
                        Message = "User data updated, email reverification required"
                    };
                }
            }
            await _userManager.UpdateAsync(user);
            return new ResponseBase()
            {
                IsSuccess = true,
                Message = "User data updated"
            };
        }

        public async Task<ResponseBase> ToggleTwoFactorAuth(string id)
        {
            var user = await _userManager.FindByIdAsync(id);

            if (user == null)
            {
                return UserNotFoundResponse();
            }
            if (user.TwoFactorEnabled)
            {
                await _userManager.SetTwoFactorEnabledAsync(user, false);
            }
            else
            {
                await _userManager.SetTwoFactorEnabledAsync(user, true);
            }
            await _userManager.UpdateSecurityStampAsync(user);
            return new ResponseBase()
            {
                IsSuccess = true,
                Message = $"Two factor updated for user {user.Id}"
            };
        }

        public async Task<ResponseBase> GetInfo(string id)
        {
            if (id == null)
            {
                return IdRequiredResponse();
            }

            var user = await _userManager.FindByIdAsync(id.ToString());
            if (user == null)
            {
                return UserNotFoundResponse();
            }
            return new ResponseBase()
            {
                IsSuccess = true,
                Message = $"Two factor enabled? {user.TwoFactorEnabled}"
            };
        }

        public async Task<ResponseBase> Logout()
        {
            await _signInManager.SignOutAsync();
            return new ResponseBase()
            {
                IsSuccess = true,
                Message = Constants.Messages.Info.UserLoggedOut
            };
        }

        //helper methods
        private string CreateConfirmEmailBody(string id, string token)
        {
            return $"<a href='{_configuration["ConfirmEmailUrl"]}id={id}&token={token}'>Confirm your email</a>";
        }
        private string CreateResetPasswordBody(string id, string token)
        {
            return $"<a href='{_configuration["ResetPasswordUrl"]}id={id}&token={token}'>Reset your password</a>";
        }
        private void SendConfirmationEmail(string email, string id, string token)
        {
            var emailRequest = new EmailRequest
            {
                To = email,
                Subject = "Confirm Email",
                Body = CreateConfirmEmailBody(id, token)
            };
            _emailService.SendEmailAsync(emailRequest);
        }
        private async Task AddLoginRecord(User user)
        {
            var provider = _configuration["LoginInfo:DefaultProvider:ProviderName"];
            var key = _configuration["LoginInfo:DefaultProvider:ProviderKey"];
            var name = _configuration["LoginInfo:DefaultProvider:ProviderName"];
            if (provider != null && key != null && name != null)
            {
                var userLogin = new UserLoginInfo(provider, key, name);
                await _userManager.AddLoginAsync(user, userLogin);
            }
            
        }
        private bool IsPasswordValid(string password)
        {
            string pattern = Constants.PasswordRegex.Pattern;
            Regex regex = new Regex(pattern);
            return regex.IsMatch(password);
        }
        private LoginResponse UserNotFoundResponse()
        {
            return new LoginResponse()
            {
                IsAuthenticated = false,
                Message = Constants.Messages.Info.UserNotFound
            };
        }
        private ResponseBase InvalidTokenResponse()
        {
            return new ResponseBase()
            {
                IsSuccess = false,
                Message = Constants.Messages.Token.Invalid
            };
        }
        private ResponseBase IdRequiredResponse()
        {
            return new ResponseBase()
            {
                IsSuccess = false,
                Message = Constants.Messages.IdRequired
            };
        }
        private ResponseBase PasswordErrorResponse()
        {
            return new ResponseBase()
            {
                IsSuccess = false,
                Message = Constants.Messages.Error.PasswordError
            };
        }
    }
}
