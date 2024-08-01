using RustyTech.Server.Models.Auth;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Posts;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IPostService
    {
        Task<ResponseBase> CreatePostAsync(PostDto post);
        Task<List<PostReadDto>> GetAllAsync(bool published);
        Task<ResponseBase> TogglePostPublishedStatusAsync<T>(int postId) where T : Post;
        Task<PostDto?> GetPostByIdAsync(int postId);
        Task<ResponseBase> EditPostAsync<T>(PostDto post) where T : Post;
    }
}
