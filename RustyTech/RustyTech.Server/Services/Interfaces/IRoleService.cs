using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Role;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RustyTech.Server.Interfaces
{
    public interface IRoleService
    {
        Task<string> CreateRoleAsync(string roleName);
        Task<List<GetRoleRequest>> GetAllRolesAsync();
        Task<GetRoleRequest?> GetRoleByIdAsync(string id);
        Task<GetRoleRequest?> GetRoleByNameAsync(string roleName);
        Task<List<UserRole>?> GetUserRolesAsync(Guid id);
        Task<string> AddRoleToUserAsync(RoleRequest request);
        Task<string> RemoveRoleFromUserAsync(RoleRequest request);
    }
}
