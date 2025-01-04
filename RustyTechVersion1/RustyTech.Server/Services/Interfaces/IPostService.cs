using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Posts;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IPostService
    {
        Task<ResponseBase> CreateBlogPostAsync(CreateBlogRequest post);
        Task<ResponseBase> CreateVideoPostAsync(CreateVideoRequest post);
        Task<ResponseBase> CreateImagePostAsync(CreateImageRequest post);
        Task<List<GetPostRequest>> GetAllAsync(bool published);
        Task<List<GetPostRequest>> GetUserPostsAsync(string userId);
        Task<ResponseBase> TogglePostPublishedStatusAsync<T>(int postId) where T : Post;
        Task<GetPostRequest?> GetPostByIdAsync(int postId);
        Task<ResponseBase> EditPostAsync<T>(UpdatePostRequest post) where T : Post;
    }
}
