using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Posts;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IKeywordService
    {
        Task<List<string>> GetAllKeywordsAsync();
        Task<List<string>> GetPostKeywordsAsync(int? id);
        void AddPostKeywords(Post post, List<string>? keywords);
        void RemovePostKeywords(Post currentPost, UpdatePostRequest newData);
    }
}
