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
        private readonly RoleService _roleService;

        public RoleController(RoleManager<IdentityRole> roleManager, RoleService roleService)
        {
            _roleManager = roleManager;
            _roleService = roleService;
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

        [HttpPost("add/{request}")]
        public async Task<IActionResult> AddRoleToUserAsync(RoleRequest request)
        {
            var result = await _roleService.AddRoleToUserAsync(new RoleRequest { RoleId = request.RoleId, UserId = request.UserId });
            return Ok(result);
        }
    }
}
