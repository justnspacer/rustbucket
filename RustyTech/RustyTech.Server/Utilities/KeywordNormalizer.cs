using System.Text.RegularExpressions;

namespace RustyTech.Server.Utilities
{
    public class KeywordNormalizer
    {
        public static string Normalize(string keyword)
        {
            if(string.IsNullOrEmpty(keyword)) return string.Empty;

            //convert to lowercase
            keyword = keyword.ToLowerInvariant(); 
            
            //remove special characters
            keyword = Regex.Replace(keyword, @"[^0-9a-zA-Z]+", "");

            return keyword;
        }

        public static List<string> NormalizeKeywords(List<string> keywords)
        {
            return keywords.Select(Normalize).Where(keyword => !string.IsNullOrEmpty(keyword)).Distinct().ToList();
        }
    }
}
