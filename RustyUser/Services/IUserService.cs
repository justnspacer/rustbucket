using Microsoft.AspNetCore.Identity;
using RustyUser.Models.Role;
using RustyUser.Models.User;

namespace RustyUser.Services
{
    public interface IUserService
    {
        Task<List<UserDto>> GetAllAsync();
        Task<UserDto?> GetByIdAsync(string id);
        Task<IdentityResult> DeleteAsync(string id);
        Task<IdentityResult> AddRoleToUserAsync(AddRoleRequest model);
    }
}
