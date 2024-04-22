namespace RustyTech.Server.Models.Auth
{
    public class ConfirmEmailRequest
    {
        public string? Id { get; set; }
        public string? Token { get; set; }
    }
}
