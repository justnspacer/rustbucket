using Ganss.Xss;
using HtmlAgilityPack;

namespace RustyTech.Server.Utilities
{
    public class StringHelper
    {    
        public static string SanitizeString(string? text)
        {
            if (text != null)
            {
                var sanitizer = new HtmlSanitizer();
                return sanitizer.Sanitize(text);
            }
            return string.Empty;
        }

        public static string ConvertHtmlToPlainText(string htmlContent)
        {
            var htmlDoc = new HtmlDocument();
            htmlDoc.LoadHtml(htmlContent);
            return htmlDoc.DocumentNode.InnerText;
        }
    }
}
