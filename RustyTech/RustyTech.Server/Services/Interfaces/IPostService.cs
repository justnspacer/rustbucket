using RustyTech.Server.Models.Auth;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IPostService
    {
        Task<ResponseBase> CreatePostAsync<T>(T post) where T : Post;
        Task<List<PostDto>> GetAllAsync(bool published);
        Task<ResponseBase> TogglePostPublishedStatusAsync<T>(int postId) where T : Post;
        Task<PostDto?> GetPostByIdAsync(int postId);
        Task<ResponseBase> EditPostAsync<T>(PostEditRequest request) where T : Post;
        Task<List<string?>> GetAllKeywordsAsync();
    }
}
