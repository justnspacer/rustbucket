using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Interfaces;
using RustyTech.Server.Models.Role;

namespace RustyTech.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    [Authorize(Roles = "SuperAdmin")]
    public class RoleController : ControllerBase
    {
        private readonly IRoleService _roleService;

        public RoleController(IRoleService roleService)
        {
            _roleService = roleService;
        }

        [HttpPost("create")]
        public async Task<IActionResult> Create(string roleName)
        {
            var result = await _roleService.CreateRole(roleName);
            return Ok(result);
        }

        [HttpGet("get/all")]
        public async Task<IActionResult> GetAll()
        {
            var result = await _roleService.GetAllRoles();            
            return Ok(result);
        }

        [HttpGet("get")]
        public async Task<IActionResult> GetRoleById(Guid roleId)
        {
            var result = await _roleService.GetRoleById(roleId.ToString());
            return Ok(result);
        }

        [HttpGet("get/name")]
        public async Task<IActionResult> GetRoleByName(string roleName)
        {
            var result = await _roleService.GetRoleByName(roleName);
            return Ok(result);
        }

        [HttpGet("get/user")]
        public async Task<IActionResult> GetUserRoles(Guid userId)
        {
            var result = await _roleService.GetUserRoles(userId);
            return Ok(result);
        }

        [HttpPost("add/user")]
        public async Task<IActionResult> AddRoleToUser([FromBody] RoleRequest request)
        {
            var result = await _roleService.AddRoleToUser(request);
            return Ok(result);
        }

        [HttpDelete("remove/user")]
        public async Task<IActionResult> RemoveRoleFromUser([FromBody] RoleRequest request)
        {
            var result = await _roleService.RemoveRoleFromUser(request);
            return Ok(result);
        }

        [HttpDelete("delete")]
        public async Task<IActionResult> DeleteRole(string roleName)
        {
            var result = await _roleService.DeleteRole(roleName);
            return Ok(result);
        }

        [HttpPost("add/claim")]
        public async Task<IActionResult> AddClaimToRole([FromBody] ClaimRequest request)
        {
            var result = await _roleService.AddClaimToRole(request);
            return Ok(result);
        }

        [HttpGet("get/claims")]
        public async Task<IActionResult> GetRoleClaims(string roleName)
        {
            var result = await _roleService.GetRoleClaims(roleName);
            return Ok(result);
        }

        [HttpDelete("remove/claim")]
        public async Task<IActionResult> RemoveClaimFromRole([FromBody] ClaimRequest request)
        {
            var result = await _roleService.RemoveClaimFromRole(request);
            return Ok(result);
        }
    }
}
