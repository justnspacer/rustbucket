using RustyTech.Server.Models.Role;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RustyTech.Server.Interfaces
{
    public interface IRoleService
    {
        Task<string> CreateRoleAsync(string roleName);
        Task<List<RoleDto>> GetAllRolesAsync();
        Task<RoleDto?> GetRoleByIdAsync(string id);
        Task<RoleDto?> GetRoleByNameAsync(string roleName);
        Task<List<UserRole>?> GetUserRolesAsync(Guid id);
        Task<string> AddRoleToUserAsync(RoleRequest request);
        Task<string> RemoveRoleFromUserAsync(RoleRequest request);
    }
}
