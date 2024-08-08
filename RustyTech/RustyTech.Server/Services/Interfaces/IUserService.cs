using RustyTech.Server.Models.Dtos;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IUserService
    {
        Task<List<GetUserRequest>> GetAllAsync(bool active);
        Task<GetUserRequest?> GetByIdAsync(Guid id);
        Task<ResponseBase> DeleteAsync(Guid id);
    }
}
