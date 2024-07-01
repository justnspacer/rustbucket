namespace RustyTech.Server.Services.Interfaces
{
    public interface IPostService
    {
        Task<BlogPost?> CreateBlogPostAsync(BlogPost post);
        Task<ImagePost?> CreateImagePostAsync(ImagePost post);
        Task<VideoPost?> CreateVideoPostAsync(VideoPost post);
        Task<List<PostDto>> GetAllAsync(bool published);
    }
}
