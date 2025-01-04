using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Posts;
using RustyTech.Server.Services.Interfaces;
using RustyTech.Server.Utilities;

namespace RustyTech.Server.Services
{
    public class KeywordService : IKeywordService
    {
        private readonly DataContext _context;

        public KeywordService(DataContext context)
        {
            _context = context;
        }

        public async Task<List<string>> GetAllKeywordsAsync() => await _context.Keywords.Select(k => k.Text).ToListAsync();

        public async Task<List<string>> GetPostKeywordsAsync(int? id) => await _context.PostKeywords.Where(pk => pk.PostId == id).Select(k => k.Keyword.Text).ToListAsync();

        public async void AddPostKeywords(Post post, List<string>? keywords)
        {
            if (keywords != null)
            {
                var normalizedKeywords = KeywordNormalizer.NormalizeKeywords(keywords);
                foreach (var text in normalizedKeywords)
                {
                    var existingKeyword = _context.Keywords.FirstOrDefault(k => k.Text == text);
                    if (existingKeyword == null)
                    {
                        Keyword keyword = new Keyword { Text = text };
                        await _context.Keywords.AddAsync(keyword);
                        await AddPostKeyword(post, keyword);
                    }
                    else
                    {
                        // Check if the post already has the keyword
                        var postKeywordExists = post.Keywords.Any(pk => pk.KeywordId == existingKeyword.Id);
                        if (!postKeywordExists)
                        {
                            await AddPostKeyword(post, existingKeyword);
                        }
                    }
                }
            }
        }

        public void RemovePostKeywords(Post currentPost, UpdatePostRequest newData)
        {
            if (newData.Keywords != null)
            {
                var normailizedKeywords = KeywordNormalizer.NormalizeKeywords(newData.Keywords);
                var keywordsToRemove = _context.PostKeywords.Where(pk => !normailizedKeywords.Contains(pk.Keyword.Text)).ToList();
                foreach (var postKeyword in keywordsToRemove)
                {
                    currentPost.Keywords.Remove(postKeyword);
                    _context.PostKeywords.Remove(postKeyword);
                }
            }
        }

        private async Task AddPostKeyword(Post post, Keyword keyword)
        {
            PostKeyword postKeyword = new PostKeyword { Post = post, Keyword = keyword };
            post.Keywords.Add(postKeyword);
            await _context.PostKeywords.AddAsync(postKeyword);
        }
    }
}
