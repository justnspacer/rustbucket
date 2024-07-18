using RustyTech.Server.Models.Auth;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IPostService
    {
        Task<ResponseBase> CreatePostAsync(PostDto post);
        Task<List<PostDto>> GetAllAsync(bool published);
        Task<ResponseBase> TogglePostPublishedStatusAsync<T>(int postId) where T : Post;
        Task<PostDto?> GetPostByIdAsync(int postId);
        Task<ResponseBase> EditPostAsync<T>(PostDto post) where T : Post;
        Task<List<string?>> GetAllKeywordsAsync();
    }
}
