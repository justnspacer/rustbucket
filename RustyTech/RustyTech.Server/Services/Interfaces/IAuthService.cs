using Microsoft.AspNetCore.Identity.Data;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Models.Dtos;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IAuthService
    {
        Task<ResponseBase> RegisterAsync(Models.Auth.RegisterRequest request);
        Task<LoginResponse> LoginAsync(Models.Auth.LoginRequest request);
        Task<ResponseBase> VerifyEmailAsync(ConfirmEmailRequest request);
        ResponseBase VerifyJwtToken(string token);
        ResponseBase ResendEmailAsync(string email);
        string GenerateJwtToken(Guid id, string email, List<string> userRoles);
        void CreatePasswordHash(string password, out byte[] passwordHash, out byte[] passwordSalt);
        Task<ResponseBase> ForgotPasswordAsync(string email);
        Task<ResponseBase> ResetPasswordAsync(ResetPasswordRequest request);
        Task<ResponseBase> UpdateUserAsync(UpdateUserRequest userDto);
        Task<ResponseBase> EnableTwoFactorAuthenticationAsync(Guid id);
        ResponseBase GetInfoAsync(Guid id);
        LoginResponse LogoutAsync();
    }
}
