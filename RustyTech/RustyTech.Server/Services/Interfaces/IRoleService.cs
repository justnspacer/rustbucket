using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Role;
using System.Security.Claims;

namespace RustyTech.Server.Interfaces
{
    public interface IRoleService
    {
        Task<ResponseBase> CreateRole(string roleName);
        Task<List<GetRoleRequest>> GetAllRoles();
        Task<GetRoleRequest?> GetRoleById(string id);
        Task<GetRoleRequest?> GetRoleByName(string roleName);
        Task<IList<string>?> GetUserRoles(Guid id);
        Task<ResponseBase> AddRoleToUser(RoleRequest request);
        Task<ResponseBase> RemoveRoleFromUser(RoleRequest request);
        Task<ResponseBase> DeleteRole(string roleName);
        Task<ResponseBase> AddClaimToRole(ClaimRequest request);
        Task<IList<Claim>?> GetRoleClaims(string roleName);
        Task<ResponseBase> RemoveClaimFromRole(ClaimRequest request);
    }
}
