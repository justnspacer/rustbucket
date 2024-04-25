using Microsoft.AspNetCore.Identity;
using RustyTech.Server.Models.Role;
using System.Linq;

namespace RustyTech.Server.Services
{
    public class RoleService
    {
        private readonly IUserService _userService;
        private readonly DataContext _context;

        public RoleService(IUserService userService, DataContext context)
        {
            _userService = userService;
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

        public async Task<List<RoleDto>?> GetUserRoles(Guid id)
        {
            if (id == Guid.Empty)
            {
                return null;
            }
            var roles = await _context.Roles
                .Select(role => new RoleDto { Id = role.Id, RoleName = role.Name })
                .Where(role => role.Id == id.ToString()).ToListAsync();
            if (roles == null)
            {
                return null;
            }
            return roles;
        }

        public async Task<string> AddRoleToUserAsync(AddRoleRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.Id) || 
                string.IsNullOrWhiteSpace(request.RoleName) || 
                request.UserId == Guid.Empty)
            {
                return "Bad request";
            }
            var user = await _context.Users.FirstOrDefaultAsync(user => user.Id == request.UserId);
            if (user == null)
            {
                return "User not found";
            }
            var role = await _context.Roles.FirstOrDefaultAsync(role => role.Id == request.Id);
            if (role == null)
            {
                //create the role if it doesn't exist, send error message
                var newRole = new IdentityRole { Name = request.RoleName };
                _context.Roles.Add(newRole);
                await _context.SaveChangesAsync();
                return "Role does not exist";
            }
            var result = await _userManager.AddToRoleAsync(user, request.RoleName);
            return "Role added to user";
        }

        private IdentityResult CreateFailureResult()
        {
            return IdentityResult.Failed(new IdentityError { Description = Constants.Message.InvalidRequest });
        }
    }
}
