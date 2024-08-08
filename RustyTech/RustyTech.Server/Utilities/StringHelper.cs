using Ganss.Xss;
using HtmlAgilityPack;
using System.Text.RegularExpressions;

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
            string pattern = "</";
            string result = Regex.Replace(htmlContent, pattern, $" </"); //add space before closing tag
            htmlDoc.LoadHtml(result);
            return htmlDoc.DocumentNode.InnerText;
        }
    }
}
