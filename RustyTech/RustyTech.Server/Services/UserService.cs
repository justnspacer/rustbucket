using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using RustyTech.Server.Models.Role;
using RustyTech.Server.Models.User;

namespace RustyTech.Server.Services
{
    public class UserService : IUserService
    {
        private readonly UserManager<User> _userManager;
        private readonly RoleManager<IdentityRole> _roleManager;
        private readonly ILogger<UserService> _logger;

        public UserService(UserManager<User> user, 
            RoleManager<IdentityRole> roleManager,
            ILogger<UserService> logger)
        {
            _userManager = user;
            _roleManager = roleManager;
            _logger = logger;
        }

        /// <summary>
        /// Retrieves all users asynchronously.
        /// </summary>
        /// <returns>A list of UserDto objects representing the users.</returns>
        public async Task<List<UserDto>> GetAllAsync()
        {
            var users = await _userManager.Users
                .Select(user => new UserDto { Id = user.Id, Email = user.Email }).ToListAsync();
            return users;
        }

        /// <summary>
        /// Retrieves a user by their ID asynchronously.
        /// </summary>
        /// <param name="id">The ID of the user to retrieve.</param>
        /// <returns>A UserDto object representing the user, or null if not found.</returns>
        public async Task<UserDto?> GetByIdAsync(string id)
        {
            if (string.IsNullOrEmpty(id))
            {
                return null;
            }
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
            {
                return null;
            }
            var userDto = new UserDto { Id = user.Id, Email = user.Email };
            return userDto;
        }

        /// <summary>
        /// Deletes a user asynchronously.
        /// </summary>
        /// <param name="id">The ID of the user to delete.</param>
        /// <returns>An IdentityResult indicating the success or failure of the delete operation.</returns>
        public async Task<IdentityResult> DeleteAsync(string id)
        {
            if (string.IsNullOrEmpty(id))
            {
                return CreateFailureResult();
            }
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
            {
                return CreateFailureResult();
            }
            var result = await _userManager.DeleteAsync(user);
            _logger.LogInformation($"User deleted");
            return result;
        }

        /// <summary>
        /// Adds a role to a user asynchronously.
        /// </summary>
        /// <param name="model">The AddRoleRequest model containing the user ID and role name.</param>
        /// <returns>An IdentityResult indicating the success or failure of the add role operation.</returns>
        public async Task<IdentityResult> AddRoleToUserAsync(AddRoleRequest model)
        {
            if (string.IsNullOrWhiteSpace(model.Id) || string.IsNullOrWhiteSpace(model.RoleName))
            {
                return CreateFailureResult();
            }
            var user = await _userManager.FindByIdAsync(model.Id);
            if (user == null)
            {
                return CreateFailureResult();
            }
            var roleExists = await _roleManager.RoleExistsAsync(model.RoleName);
            if (!roleExists)
            {
                //create the role if it doesn't exist, send error message
                await _roleManager.CreateAsync(new IdentityRole(model.RoleName));
                return CreateFailureResult();
            }
            var result = await _userManager.AddToRoleAsync(user, model.RoleName);
            return result.Succeeded ? IdentityResult.Success : CreateFailureResult();
        }

        private IdentityResult CreateFailureResult()
        {
            return IdentityResult.Failed(new IdentityError { Description = Constants.Message.InvalidRequest });
        }
    }
}
