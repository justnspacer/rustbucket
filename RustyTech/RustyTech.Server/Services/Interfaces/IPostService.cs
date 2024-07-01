using RustyTech.Server.Models.Auth;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IPostService
    {
        Task<ResponseBase> CreateBlogPostAsync(BlogPost post);
        Task<ResponseBase> CreateImagePostAsync(ImagePost post);
        Task<ResponseBase> CreateVideoPostAsync(VideoPost post);
        Task<List<PostDto>> GetAllAsync(bool published);
        Task<ResponseBase> TogglePostPublishedStatusAsync<T>(int postId) where T : Post;
        Task<PostDto?> GetPostByIdAsync(int postId);
    }
}
