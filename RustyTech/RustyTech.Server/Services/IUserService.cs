namespace RustyTech.Server.Services
{
    public interface IUserService
    {
        Task<List<UserDto>> GetAllAsync();
        Task<UserDto?> GetByIdAsync(Guid id);
        Task<UserDto?> FindByEmailAsync(string email);
        Task<string> DeleteAsync(Guid id);
    }
}
