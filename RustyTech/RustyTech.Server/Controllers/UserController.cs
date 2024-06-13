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
        private readonly ILogger<UserController> _logger;

        public UserController(IUserService userService, ILogger<UserController> logger)
        {
            _userService = userService;
            _logger = logger;
        }

        [HttpGet("get/all")]
        public async Task<IActionResult> GetAllAsync(bool active = true)
        {
            var users = await _userService.GetAllAsync(active);
            return Ok(users);
        }

        [HttpGet("get/{id}")]
        public async Task<IActionResult> GetByIdAsync(Guid id)
        {
            var user = await _userService.GetByIdAsync(id);
            return Ok(user);
        }

        [Authorize(Roles = "Admin")]
        [HttpGet("find/{email}")]
        public async Task<IActionResult> FindByEmailAsync(string email)
        {
            var user = await _userService.FindByEmailAsync(email);
            _logger.LogInformation($"User {email} found by email");
            return Ok(user);
        }

        [Authorize(Roles = "Admin")]
        [HttpDelete("delete/{id}")]
        public async Task<IActionResult> DeleteAsync(Guid id)
        {
            var result = await _userService.DeleteAsync(id);
            _logger.LogInformation($"User {id} deleted");
            return Ok(result);
        }
    }
}
