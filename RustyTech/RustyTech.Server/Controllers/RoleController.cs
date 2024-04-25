using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Models.Role;
using RustyTech.Server.Services;

namespace RustyTech.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class RoleController : ControllerBase
    {
        private readonly RoleManager<IdentityRole> _roleManager;
        private readonly UserManager<User> _userManager;
        private readonly DataContext _context;

        public RoleController(RoleManager<IdentityRole> roleManager, UserManager<User> userManager, DataContext context)
        {
            _roleManager = roleManager;
            _userManager = userManager;
            _context = context;
        }

        [HttpPost("create")]
        public async Task<IActionResult> Create(string roleName)
        {
            var result = await _roleManager.CreateAsync(new IdentityRole(roleName));
            return result.Succeeded ? Ok("Role created"): BadRequest("Role not created");
        }

        [HttpGet("get/{roleId}")]
        public async Task<IActionResult> GetRoleById(string roleId)
        {
            var result = await _roleManager.FindByIdAsync(roleId);
            return Ok(result);
        }

        [HttpPost("get/{roleId}/{userid}")]
        public async Task<IActionResult> AddRoleToUserAsync(string roleId, string roleName, Guid userId)
        {
            if (string.IsNullOrWhiteSpace(roleId) || string.IsNullOrWhiteSpace(roleName))
            {
                return BadRequest("Id/Name required");
            }
            var user = await _context.Users.FirstOrDefaultAsync(user => user.Id == userId);
            if (user == null)
            {
                return BadRequest("User not found");
            }
            var roleExists = await _roleManager.RoleExistsAsync(roleName);
            if (!roleExists)
            {
                //create the role if it doesn't exist, send error message
                await _roleManager.CreateAsync(new IdentityRole(roleName));
                return Ok("Role not created");
            }
            var result = await _userManager.AddToRoleAsync(user, model.RoleName);
            return result.Succeeded ? IdentityResult.Success : CreateFailureResult();
        }
    }
}
