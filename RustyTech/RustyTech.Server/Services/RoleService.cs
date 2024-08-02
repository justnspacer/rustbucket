using Microsoft.AspNetCore.Identity;
using RustyTech.Server.Interfaces;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Role;

namespace RustyTech.Server.Services
{
    public class RoleService : IRoleService
    {
        private readonly DataContext _context;

        public RoleService() { }

        public RoleService(DataContext context)
        {
            _context = context;
        }

        public async Task<string> CreateRoleAsync(string roleName)
        {
            if (string.IsNullOrWhiteSpace(roleName))
            {
                return Constants.Messages.Role.NameRequired;
            }
            var roleExists = await _context.Roles.FirstOrDefaultAsync(role => role.Name == roleName);
            if (roleExists != null)
            {
                return Constants.Messages.Role.Exists;
            }
            var role = new IdentityRole { Name = roleName, NormalizedName = roleName.ToUpper(), ConcurrencyStamp = Guid.NewGuid().ToString() };
            await _context.Roles.AddAsync(role);
            await _context.SaveChangesAsync();
            return Constants.Messages.Role.Created;
        }

        public async Task<List<GetRoleRequest>> GetAllRolesAsync()
        {
            var roles = await _context.Roles.Select(role => new GetRoleRequest { Id = role.Id, RoleName = role.Name }).ToListAsync();
            return roles;
        }

        public async Task<GetRoleRequest?> GetRoleByIdAsync(string id)
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
            var roleDto = new GetRoleRequest { Id = role.Id, RoleName = role.Name };
            return roleDto;
        }

        public async Task<GetRoleRequest?> GetRoleByNameAsync(string roleName)
        {
            if (string.IsNullOrEmpty(roleName))
            {
                return null;
            }
            var role = await _context.Roles.FirstOrDefaultAsync(role => role.Name == roleName);
            if (role == null)
            {
                return null;
            }
            var roleDto = new GetRoleRequest { Id = role.Id, RoleName = role.Name };
            return roleDto;
        }

        public async Task<List<UserRole>?> GetUserRolesAsync(Guid id)
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
            if (string.IsNullOrWhiteSpace(request.RoleName) || request.UserId == Guid.Empty)
            {
                return Constants.Messages.Error.BadRequest;
            }

            var user = await _context.Users.FirstOrDefaultAsync(user => user.Id == request.UserId);
            if (user == null)
            {
                return Constants.Messages.Info.UserNotFound;
            }

            var role = await _context.Roles.FirstOrDefaultAsync(role => role.Name == request.RoleName);

            if (role == null)
            {
                return Constants.Messages.Role.NotFound;
            }

            var userRole = new UserRole { RoleId = role.Id, UserId = user.Id, CreatedAt = DateTime.UtcNow };
            _context.UserRoles.Add(userRole);
            await _context.SaveChangesAsync();

            return Constants.Messages.Role.AddedToUser;
        }

        public async Task<string> RemoveRoleFromUserAsync(RoleRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.RoleId) || request.UserId == Guid.Empty)
            {
                return Constants.Messages.Error.BadRequest;
            }

            var userRole = _context.UserRoles.FirstOrDefault(ur => ur.UserId == request.UserId && ur.RoleId == request.RoleId);
            if (userRole == null)
            {
                return Constants.Messages.Info.UserNotFound;
            }

            _context.UserRoles.Remove(userRole);
            await _context.SaveChangesAsync();

            return Constants.Messages.Role.Removed;
        }
    }
}
