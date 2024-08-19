using Microsoft.AspNetCore.Identity;
using RustyTech.Server.Interfaces;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Role;
using System.Security.Claims;

namespace RustyTech.Server.Services
{
    public class RoleService : IRoleService
    {
        private readonly UserManager<User> _userManager;
        private readonly RoleManager<IdentityRole> _roleManager;
        private readonly ILogger<RoleService> _logger;

        public RoleService(RoleManager<IdentityRole> roleManager, UserManager<User> userManager , ILogger<RoleService> logger)
        {
            _roleManager = roleManager;
            _userManager = userManager;
            _logger = logger;
        }

        public async Task<ResponseBase> CreateRole(string roleName)
        {
            if (string.IsNullOrWhiteSpace(roleName))
            {
                return new ResponseBase { 
                    IsSuccess = false, 
                    Message = Constants.Messages.Role.NameRequired
                };
            }
            var roleExists = await _roleManager.RoleExistsAsync(roleName);
            if (roleExists)
            {
                return new ResponseBase { 
                    IsSuccess = false, 
                    Message = Constants.Messages.Role.Exists
                };
            }
            var result = await _roleManager.CreateAsync(new IdentityRole(roleName));
            if (result.Succeeded)
            {
                var role = await _roleManager.FindByNameAsync(roleName);
                if (role == null)
                {
                    return new ResponseBase { 
                        IsSuccess = false, 
                        Message = Constants.Messages.Role.NotFound 
                    };
                }
                role.ConcurrencyStamp = Guid.NewGuid().ToString();
                await _roleManager.UpdateAsync(role);
                _logger.LogInformation($"Role {roleName} created");
                return new ResponseBase { 
                    IsSuccess = true, 
                    Message = Constants.Messages.Role.Created 
                };
            }
            else
            {
                return new ResponseBase
                {
                    IsSuccess = false,
                    Message = result.Errors.Select(d => d.Description).FirstOrDefault()
                };
            }
        }

        public async Task<List<GetRoleRequest>> GetAllRoles()
        {
            var roles = await _roleManager.Roles.Select(role => new GetRoleRequest { Id = role.Id, RoleName = role.Name }).ToListAsync();
            _logger.LogInformation($"All roles requested");
            return roles;
        }

        public async Task<GetRoleRequest?> GetRoleById(string id)
        {
            if (string.IsNullOrEmpty(id))
            {
                return null;
            }
            var role = await _roleManager.FindByIdAsync(id);
            if (role == null)
            {
                return null;
            }
            var roleDto = new GetRoleRequest { Id = role.Id, RoleName = role.Name };
            return roleDto;
        }

        public async Task<GetRoleRequest?> GetRoleByName(string roleName)
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

        public async Task<IList<string>?> GetUserRoles(Guid id)
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

        public async Task<ResponseBase> AddRoleToUser(RoleRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.RoleName) || request.UserId == Guid.Empty)
            {
                return new ResponseBase { 
                    IsSuccess = false, 
                    Message = Constants.Messages.Error.BadRequest 
                };
            }

            var user = await _userManager.FindByIdAsync(request.UserId.ToString());
            if (user == null)
            {
                return new ResponseBase { 
                    IsSuccess = false, 
                    Message = Constants.Messages.Info.UserNotFound
                };
            }

            var role = await _roleManager.FindByNameAsync(request.RoleName);

            if (role == null)
            {
                return new ResponseBase { 
                    IsSuccess = false, 
                    Message = Constants.Messages.Role.NotFound
                };
            }
            if (string.IsNullOrEmpty(role.Name))
            {
                return new ResponseBase { 
                    IsSuccess = false, 
                    Message = Constants.Messages.Role.NotFound
                };
            }
            var result = await _userManager.AddToRoleAsync(user, role.Name);
            if (result.Succeeded)
            {
                _logger.LogInformation($"Role {role.Name} added to user");
                return new ResponseBase { 
                    IsSuccess = true, 
                    Message = Constants.Messages.Role.AddedToUser
                };
            }
            else
            {
                return new ResponseBase
                {
                    IsSuccess = false,
                    Message = result.Errors.Select(d => d.Description).FirstOrDefault()
                };
            }
        }

        public async Task<ResponseBase> RemoveRoleFromUser(RoleRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.RoleId) || request.UserId == Guid.Empty)
            {
                return new ResponseBase
                {
                    IsSuccess = false,
                    Message = Constants.Messages.Error.BadRequest
                };
            }

            var user = await _userManager.FindByIdAsync(request.UserId.ToString());
            if (user == null)
            {
                return new ResponseBase
                {
                    IsSuccess = false,
                    Message = Constants.Messages.Info.UserNotFound
                };
            }
            var role = await _roleManager.FindByNameAsync(request.RoleName);
            if (role == null)
            {
                return new ResponseBase
                {
                    IsSuccess = false,
                    Message = Constants.Messages.Role.NotFound
                };
            }
            if (string.IsNullOrEmpty(role.Name))
            {
                return new ResponseBase
                {
                    IsSuccess = false,
                    Message = Constants.Messages.Role.NotFound
                };
            }
            _logger.LogInformation($"Role {role.Name} removed from user");
            await _userManager.RemoveFromRoleAsync(user, role.Name);
            return new ResponseBase 
            { 
                IsSuccess = false, 
                Message = Constants.Messages.Role.Removed 
            };
        }

        public async Task<ResponseBase> DeleteRole(string roleName)
        {
            var role = await _roleManager.FindByNameAsync(roleName);
            if (role != null)
            {
                var result = await _roleManager.DeleteAsync(role);
                if (result.Succeeded)
                {
                    _logger.LogInformation($"Role {role.Name} deleted");
                    return new ResponseBase { IsSuccess = true, Message = "Role deleted" };
                }
                else
                {
                    return new ResponseBase
                    {
                        IsSuccess = false,
                        Message = result.Errors.Select(d => d.Description).FirstOrDefault()
                    };
                }
            }
            return new ResponseBase { IsSuccess = false, Message = Constants.Messages.Role.NotFound };
        }

        public async Task<ResponseBase> AddClaimToRole(ClaimRequest request)
        {
            var role = await _roleManager.FindByNameAsync(request.RoleName);
            if (role != null)
            {
                var claims = await _roleManager.GetClaimsAsync(role);
                if (claims.Count != 0)
                {
                    foreach (var claim in claims)
                    {
                        if (claim.Type == request.ClaimType && claim.Value == request.ClaimValue)
                        {
                            return new ResponseBase { IsSuccess = false, Message = "Claim already exists" };
                        }
                    }
                }
                
                var result = await _roleManager.AddClaimAsync(role, new Claim(request.ClaimType, request.ClaimValue));
                if (result.Succeeded)
                {
                    _logger.LogInformation($"Claim added to {role.Name}");
                    return new ResponseBase { IsSuccess = true, Message = "Claim added to role" };
                }
            }
            return new ResponseBase { IsSuccess = false, Message = Constants.Messages.Role.NotFound };
        }

        public async Task<IList<Claim>?> GetRoleClaims(string roleName)
        {
            var role = await _roleManager.FindByNameAsync(roleName);
            if (role != null)
            {
                var result = await _roleManager.GetClaimsAsync(role);
                return result;
            }
            return null;
        }

        public async Task<ResponseBase> RemoveClaimFromRole(ClaimRequest request)
        {
            var role = await _roleManager.FindByNameAsync(request.RoleName);
            if (role != null)
            {
                var claim = new Claim(request.ClaimType, request.ClaimValue);
                var result = await _roleManager.RemoveClaimAsync(role, claim);
                if (result.Succeeded)
                {
                    _logger.LogInformation($"Claim removed from role {role.Name}");
                    return new ResponseBase 
                    { 
                        IsSuccess = true, 
                        Message = "Claim removed from role" 
                    };
                }
                else
                {
                    return new ResponseBase
                    {
                        IsSuccess = false,
                        Message = result.Errors.Select(d => d.Description).FirstOrDefault()
                    };
                }
            }
            return new ResponseBase { 
                IsSuccess = false, 
                Message = Constants.Messages.Role.NotFound };
        }
    }
}
