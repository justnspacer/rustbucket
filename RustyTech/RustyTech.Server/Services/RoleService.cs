using AngleSharp.Css;
using Microsoft.AspNetCore.Identity;
using Microsoft.IdentityModel.Tokens;
using RustyTech.Server.Interfaces;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Role;

namespace RustyTech.Server.Services
{
    public class RoleService : IRoleService
    {
        private readonly UserManager<User> _userManager;
        private readonly RoleManager<IdentityRole> _roleManager;

        public RoleService() { }

        public RoleService(RoleManager<IdentityRole> roleManager, UserManager<User> userManager)
        {
            _roleManager = roleManager;
            _userManager = userManager;
        }

        public async Task<string> CreateRoleAsync(string roleName)
        {
            if (string.IsNullOrWhiteSpace(roleName))
            {
                return Constants.Messages.Role.NameRequired;
            }
            var roleExists = await _roleManager.RoleExistsAsync(roleName);
            if (roleExists)
            {
                return Constants.Messages.Role.Exists;
            }
            var role = new IdentityRole { Name = roleName, NormalizedName = roleName.ToUpper(), ConcurrencyStamp = Guid.NewGuid().ToString() };
            await _roleManager.CreateAsync(role);
            return Constants.Messages.Role.Created;
        }

        public async Task<List<GetRoleRequest>> GetAllRolesAsync()
        {
            var roles = await _roleManager.Roles.Select(role => new GetRoleRequest { Id = role.Id, RoleName = role.Name }).ToListAsync();
            return roles;
        }

        public async Task<GetRoleRequest?> GetRoleByIdAsync(string id)
        {
            if (string.IsNullOrEmpty(id))
            {
                return null;
            }
            var role = await _roleManager.Roles.FirstOrDefaultAsync(role => role.Id == id);
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
            var role = await _roleManager.Roles.FirstOrDefaultAsync(role => role.Name == roleName);
            if (role == null)
            {
                return null;
            }
            var roleDto = new GetRoleRequest { Id = role.Id, RoleName = role.Name };
            return roleDto;
        }

        public async Task<IList<string>?> GetUserRolesAsync(Guid id)
        {
            if (id == Guid.Empty)
            {
                return null;
            }
            var user = await _userManager.FindByIdAsync(id.ToString());
            if (user == null)
            {
                return null;
            }
            var userRoles = await _userManager.GetRolesAsync(user);

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

            var user = await _userManager.FindByIdAsync(request.UserId.ToString());
            if (user == null)
            {
                return Constants.Messages.Info.UserNotFound;
            }

            var role = await _roleManager.Roles.FirstOrDefaultAsync(role => role.Name == request.RoleName);

            if (role == null)
            {
                return Constants.Messages.Role.NotFound;
            }
            if (string.IsNullOrEmpty(role.Name))
            {
                return Constants.Messages.Role.NotFound;
            }
            await _userManager.AddToRoleAsync(user, role.Name);
            return Constants.Messages.Role.AddedToUser;
        }

        public async Task<string> RemoveRoleFromUserAsync(RoleRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.RoleId) || request.UserId == Guid.Empty)
            {
                return Constants.Messages.Error.BadRequest;
            }

            var user = await _userManager.FindByIdAsync(request.UserId.ToString());
            if (user == null)
            {
                return Constants.Messages.Info.UserNotFound;
            }
            var role = await _roleManager.FindByNameAsync(request.RoleName);
            if (role == null)
            {
                return Constants.Messages.Role.NotFound;
            }
            if (string.IsNullOrEmpty(role.Name))
            {
                return Constants.Messages.Role.NotFound;
            }
            await _userManager.RemoveFromRoleAsync(user, role.Name);
            return Constants.Messages.Role.Removed;
        }
    }
}
