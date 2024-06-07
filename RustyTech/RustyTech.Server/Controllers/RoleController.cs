using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Models.Role;
using RustyTech.Server.Services;

namespace RustyTech.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class RoleController : ControllerBase
    {
        private readonly RoleService _roleService;
        private readonly ILogger<RoleController> _logger;


        public RoleController(RoleService roleService, ILogger<RoleController> logger)
        {
            _roleService = roleService;
            _logger = logger;
        }

        [Authorize(Roles = "Admin")]
        [HttpPost("create")]
        public async Task<IActionResult> CreateRoleAsync(string roleName)
        {
            var result = await _roleService.CreateRoleAsync(roleName);
            _logger.LogInformation($"Role {roleName} created");
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpGet("get/all")]
        public async Task<IActionResult> GetAllAsync()
        {
            var result = await _roleService.GetAllRolesAsync();
            _logger.LogInformation($"All roles requested");
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpGet("get/{roleId}")]
        public async Task<IActionResult> GetRoleByIdAsync(string roleId)
        {
            var result = await _roleService.GetRoleByIdAsync(roleId);
            _logger.LogInformation($"Role requested");
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpGet("get/name/{roleName}")]
        public async Task<IActionResult> GetRoleByNameAsync(string roleName)
        {
            var result = await _roleService.GetRoleByNameAsync(roleName);
            _logger.LogInformation($"Role requested by name");
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpGet("get/user/{userId}")]
        public async Task<IActionResult> GetUserRolesAsync(Guid userId)
        {
            var result = await _roleService.GetUserRolesAsync(userId);
            _logger.LogInformation($"User roles requested");
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpPost("add/user")]
        public async Task<IActionResult> AddRoleToUserAsync([FromBody] RoleRequest request)
        {
            var result = await _roleService.AddRoleToUserAsync(request);
            _logger.LogInformation($"Role {request.RoleName} added to user");
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpDelete("remove/user")]
        public async Task<IActionResult> RemoveRoleFromUserAsync([FromBody] RoleRequest request)
        {
            var result = await _roleService.RemoveRoleFromUserAsync(request);
            _logger.LogInformation($"Role {request.RoleName} removed from user");
            return Ok(result);
        }
    }
}
