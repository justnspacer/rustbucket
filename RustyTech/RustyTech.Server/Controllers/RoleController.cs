﻿using Microsoft.AspNetCore.Authorization;
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

        public RoleController(RoleService roleService)
        {
            _roleService = roleService;
        }

        [Authorize(Roles = "Admin")]
        [HttpPost("create")]
        public async Task<IActionResult> CreateRoleAsync(string roleName)
        {
            var result = await _roleService.CreateRoleAsync(roleName);
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpGet("get/all")]
        public async Task<IActionResult> GetAllAsync()
        {
            var result = await _roleService.GetAllRolesAsync();
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpGet("get/{roleId}")]
        public async Task<IActionResult> GetRoleByIdAsync(string roleId)
        {
            var result = await _roleService.GetRoleByIdAsync(roleId);
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpGet("get/name/{roleName}")]
        public async Task<IActionResult> GetRoleByNameAsync(string roleName)
        {
            var result = await _roleService.GetRoleByNameAsync(roleName);
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpGet("get/user/{userId}")]
        public async Task<IActionResult> GetUserRolesAsync(Guid userId)
        {
            var result = await _roleService.GetUserRolesAsync(userId);
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpPost("add/user")]
        public async Task<IActionResult> AddRoleToUserAsync([FromBody] RoleRequest request)
        {
            var result = await _roleService.AddRoleToUserAsync(request);
            return Ok(result);
        }

        [Authorize(Roles = "Admin")]
        [HttpDelete("remove/user")]
        public async Task<IActionResult> RemoveRoleFromUserAsync([FromBody] RoleRequest request)
        {
            var result = await _roleService.RemoveRoleFromUserAsync(request);
            return Ok(result);
        }
    }
}
