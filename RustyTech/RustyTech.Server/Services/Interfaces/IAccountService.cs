using Microsoft.AspNetCore.Identity.Data;
using RustyTech.Server.Models.Account;
using RustyTech.Server.Models.Dtos;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IAccountService
    {
        Task<ResponseBase> Register(CustomRegisterRequest request);
        Task<LoginResponse> Login(CustomLoginRequest request);
        Task<ResponseBase> VerifyEmail(VerifyEmailRequest request);
        Task<ResponseBase> ResendEmail(string email);
        Task<ResponseBase> ForgotPassword(string email);
        Task<ResponseBase> ResetPassword(CustomResetPasswordRequest request);
        Task<ResponseBase> UpdateUser(UpdateUserRequest userDto);
        Task<ResponseBase> ToggleTwoFactorAuth(Guid id);
        Task<ResponseBase> GetInfo(Guid id);
        Task<ResponseBase> Logout();
    }
}
