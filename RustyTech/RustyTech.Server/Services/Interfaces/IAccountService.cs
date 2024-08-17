using Microsoft.AspNetCore.Identity.Data;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Models.Dtos;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IAccountService
    {
        Task<ResponseBase> Register(CustomRegisterRequest request);
        Task<LoginResponse> LoginAsync(Models.Auth.LoginRequest_old request);
        Task<ResponseBase> VerifyEmail(VerifyEmailRequest request);
        ResponseBase VerifyJwtToken(string token);
        Task<ResponseBase> ResendEmailAsync(string email);
        string GenerateJwtToken(Guid id, string email, List<string> userRoles);
        void CreatePasswordHash(string password, out byte[] passwordHash, out byte[] passwordSalt);
        Task<ResponseBase> ForgotPasswordAsync(string email);
        Task<ResponseBase> ResetPasswordAsync(ResetPasswordRequest request);
        Task<ResponseBase> UpdateUserAsync(UpdateUserRequest userDto);
        Task<ResponseBase> EnableTwoFactorAuthenticationAsync(Guid id);
        Task<ResponseBase> GetInfoAsync(Guid id);
        LoginResponse LogoutAsync();
    }
}
