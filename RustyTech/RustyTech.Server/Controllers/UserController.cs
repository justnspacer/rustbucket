using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class UserController : ControllerBase
    {
        private readonly IUserService _userService;

        public UserController(IUserService userService)
        {
            _userService = userService;
        }

        [HttpGet("get/all")]
        public async Task<IActionResult> GetAllAsync(bool active = true)
        {
            var users = await _userService.GetAllAsync(active);
            return Ok(users);
        }

        [HttpGet("get/{id}")]
        public async Task<IActionResult> GetByIdAsync(string id)
        {
            var user = await _userService.GetByIdAsync(id);
            return Ok(user);
        }

        [Authorize(Roles = "Administrator")]
        [HttpDelete("delete/{id}")]
        public async Task<IActionResult> DeleteAsync(string id)
        {
            var result = await _userService.DeleteAsync(id);
            return Ok(result);
        }
    }
}
