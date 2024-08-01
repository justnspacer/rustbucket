using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Posts;

namespace RustyTech.Server.Services.Interfaces
{
    public interface IKeywordService
    {
        Task<List<string>> GetAllKeywordsAsync();
        Task<List<string>> GetPostKeywordsAsync(int? id);
        void AddKeywords(Post post, List<string>? keywords);
        void RemoveKeywords(Post currentPost, PostDto newData);
    }
}
