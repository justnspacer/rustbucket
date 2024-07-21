using RustyTech.Server.Models.Auth;
using RustyTech.Server.Models.Dtos;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IUserService
    {
        Task<List<UserDto>> GetAllAsync(bool active);
        Task<UserDto?> GetByIdAsync(Guid id);
        Task<ResponseBase> DeleteAsync(Guid id);
    }
}
