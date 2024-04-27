using Microsoft.AspNetCore.Identity;
using RustyTech.Server.Models.Role;

namespace RustyTech.Server.Services
{
    public class RoleService
    {
        private readonly DataContext _context;

        public RoleService(DataContext context)
        {
            _context = context;
        }

        public async Task<List<RoleDto>> GetAllAsync()
        {
            var roles = await _context.Roles.Select(role => new RoleDto { Id = role.Id, RoleName = role.Name }).ToListAsync();
            return roles;
        }

        public async Task<RoleDto?> GetRoleById(string id)
        {
            if (string.IsNullOrEmpty(id))
            {
                return null;
            }
            var role = await _context.Roles.FirstOrDefaultAsync(role => role.Id == id);
            if (role == null)
            {
                return null;
            }
            var roleDto = new RoleDto { Id = role.Id, RoleName = role.Name };
            return roleDto;
        }

        public async Task<List<UserRole>?> GetUserRoles(Guid id)
        {
            if (id == Guid.Empty)
            {
                return null;
            }

            var userRoles = await _context.UserRoles
                .Where(role => role.UserId == id).ToListAsync();

            if (userRoles == null)
            {
                return null;
            }

            return userRoles;
        }

        public async Task<string> AddRoleToUserAsync(RoleRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.RoleId) || request.UserId == Guid.Empty)
            {
                return "Bad request";
            }

            var user = await _context.Users.FirstOrDefaultAsync(user => user.Id == request.UserId);
            if (user == null)
            {
                return "User not found";
            }

            var role = await _context.Roles.FirstOrDefaultAsync(role => role.Id == request.RoleId);

            if (role == null)
            {
                return "Role does not exist";
            }

            var userRole = new UserRole { RoleId = role.Id, UserId = user.Id, CreatedAt = DateTime.UtcNow };
            _context.UserRoles.Add(userRole);
            await _context.SaveChangesAsync();

            return "Role added to user";
        }

        public async Task<string> RemoveRoleFromUserAsync(RoleRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.RoleId) || request.UserId == Guid.Empty)
            {
                return "Bad request";
            }

            var userRole = _context.UserRoles.FirstOrDefault(ur => ur.UserId == request.UserId && ur.RoleId == request.RoleId);
            if (userRole == null)
            {
                return "User role not found";
            }

            _context.UserRoles.Remove(userRole);
            await _context.SaveChangesAsync();

            return "Role added to user";
        }
    }
}
