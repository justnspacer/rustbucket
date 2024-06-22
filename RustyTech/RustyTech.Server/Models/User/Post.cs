namespace RustyTech.Server.Models.User
{
    public abstract class Post
    {
        public int Id { get; set; }
        public string? Title { get; set; }
        public string? Content { get; set; }
        public bool IsPublished { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }

        public Guid UserId { get; set; } // Foreign key

        public UserDto? User { get; set; } // Navigation property

        public abstract void Display();
    }
}
