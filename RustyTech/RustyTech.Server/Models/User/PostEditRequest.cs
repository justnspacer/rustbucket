namespace RustyTech.Server.Models.User
{
    public class PostEditRequest
    {
        public int PostId { get; set; }
        public Post? UpdatedPost { get; set; }
        public Guid UserId { get; set; }
    }
}
