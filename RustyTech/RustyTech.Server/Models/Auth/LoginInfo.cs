namespace RustyTech.Server.Models.Auth
{
    public class LoginInfo
    {
        public int Id { get; set; }
        public Guid UserId { get; set; }
        public DateTime LoginTime { get; set; }
    }
}
