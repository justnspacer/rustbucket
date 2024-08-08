using AutoMapper;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Services.Interfaces;

namespace RustyTech.Server.Services
{
    public class UserService : IUserService
    {
        private readonly DataContext _context;
        private readonly IMapper _mapper;
        private readonly ILogger<IUserService> _logger;

        public UserService(DataContext context, IMapper mapper, ILogger<IUserService> logger)
        {
            _context = context;
            _mapper = mapper;
            _logger = logger;
        }

        public async Task<List<GetUserRequest>> GetAllAsync(bool active = true)
        {
            var users = new List<GetUserRequest>();
            if (active)
            {
                users = await _context.Users.Where(confirmed => confirmed.EmailConfirmed).Select(user => _mapper.Map<GetUserRequest>(user)).ToListAsync();
            }
            else
            {
                users = await _context.Users.Select(user => _mapper.Map<GetUserRequest>(user)).ToListAsync();
            }
            return users;
        }

        public async Task<GetUserRequest?> GetByIdAsync(Guid id)
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
            var userDto = _mapper.Map<GetUserRequest>(user);
            return userDto;
        }

        public async Task<ResponseBase> DeleteAsync(Guid id)
        {
            if (id == Guid.Empty)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.IdRequired };
            }

            var userToDelete = await _context.Users.FirstOrDefaultAsync(user => user.Id == id);
            if (userToDelete == null)
            {
                return new ResponseBase() { IsSuccess = false, Message = Constants.Messages.Error.BadRequest };
            }
            _context.Users.Remove(userToDelete);
            await _context.SaveChangesAsync();
            _logger.LogInformation($"User {id} deleted");
            return new ResponseBase() { IsSuccess = true, Message = Constants.Messages.Info.UserDeleted };
        }
    }
}
