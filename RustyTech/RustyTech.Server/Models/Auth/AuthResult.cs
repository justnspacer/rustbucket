namespace RustyTech.Server.Models.Auth
{
    public class AuthResult
    {
        public bool Succeeded { get; set; }
        public IEnumerable<string>? Errors { get; set; }
        public string? Token { get; set; }
    }
}
