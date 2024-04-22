using Microsoft.AspNetCore.Identity;
using RustyTech.Server.Models.Role;
using RustyTech.Server.Models.User;

namespace RustyTech.Server.Services
{
    public interface IUserService
    {
        Task<List<UserDto>> GetAllAsync();
        Task<UserDto?> GetByIdAsync(string id);
        Task<IdentityResult> DeleteAsync(string id);
        Task<IdentityResult> AddRoleToUserAsync(AddRoleRequest model);
    }
}
