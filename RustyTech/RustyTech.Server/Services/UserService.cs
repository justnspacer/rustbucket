using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Services
{
    public class UserService : IUserService
    {
        private readonly ILogger<IUserService> _logger;
        private readonly DataContext _context;

        public UserService(DataContext context, ILogger<IUserService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<List<UserDto>> GetAllAsync(bool active = true)
        {
            var users = new List<UserDto>();
            if (active)
            {
                users = await _context.Users.Where(confirmed => confirmed.EmailConfirmed).Select(user => new UserDto { Id = user.Id, Email = user.Email }).ToListAsync();
            }
            else
            {
                users = await _context.Users.Select(user => new UserDto { Id = user.Id, Email = user.Email }).ToListAsync();
            }
            return users;
        }

        public async Task<UserDto?> GetByIdAsync(Guid id)
        {
            if (id == Guid.Empty)
            {
                return null;
            }
            var user = await _context.Users.FirstOrDefaultAsync(user => user.Id == id);
            if (user == null)
            {
                return null;
            }
            var userDto = new UserDto { Id = user.Id, Email = user.Email };
            return userDto;
        }

        public async Task<UserDto?> FindByEmailAsync(string email)
        {
            if (string.IsNullOrEmpty(email))
            {
                return null;
            }
            var user = await _context.Users.FirstOrDefaultAsync(user => user.Email == email);
            if (user == null)
            {
                return null;
            }
            var userDto = new UserDto { Id = user.Id, Email = user.Email };
            return userDto;
        }

        public async Task<string> DeleteAsync(Guid id)
        {
            if (id == Guid.Empty)
            {
                return "id is required";
            }
            var user = await _context.Users.FirstOrDefaultAsync(user => user.Id == id);
            if (user == null)
            {
                return "User not found";
            }
            _context.Users.Remove(user);
            _logger.LogInformation($"User {id} deleted");
            return $"User deleted";
        }
    }
}
