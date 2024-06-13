namespace RustyTech.Server.Services.Interfaces
{
    public interface IUserService
    {
        Task<List<UserDto>> GetAllAsync(bool active);
        Task<UserDto?> GetByIdAsync(Guid id);
        Task<UserDto?> FindByEmailAsync(string email);
        Task<string> DeleteAsync(Guid id);
    }
}
