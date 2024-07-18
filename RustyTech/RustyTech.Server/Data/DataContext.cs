using Microsoft.AspNetCore.Identity;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Models.Role;

namespace RustyTech.Server.Data
{
    public class DataContext : DbContext
    {
        public DataContext() { }

        public DataContext(DbContextOptions<DataContext> options) : base(options) { }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            base.OnConfiguring(optionsBuilder);
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure the relationships and inheritance
            modelBuilder.Entity<Post>()
                .HasDiscriminator<string>("PostType")
                .HasValue<Image>("ImagePost")
                .HasValue<Video>("VideoPost")
                .HasValue<Blog>("BlogPost");

            modelBuilder.Entity<Post>()
                .HasOne(p => p.User)
                .WithMany(u => u.Posts)
                .HasForeignKey(p => p.UserId)
                .OnDelete(DeleteBehavior.Cascade); // Delete all posts when a user is deleted

            modelBuilder.Entity<PostKeyword>()
                .HasOne(pk => pk.Post)
                .WithMany(p => p.Keywords)
                .HasForeignKey(p => p.PostId)
                .OnDelete(DeleteBehavior.Cascade); // Delete all keywords when a post is deleted
        }

        public DbSet<User> Users { get; set; }
        public DbSet<LoginInfo> Logins { get; set; }
        public DbSet<IdentityRole> Roles { get; set; }
        public DbSet<UserRole> UserRoles { get; set; }

        public DbSet<Blog> BlogPosts { get; set; }
        public DbSet<Image> ImagePosts { get; set; }
        public DbSet<Video> VideoPosts { get; set; }
        public DbSet<Keyword> Keywords { get; set; }
        public DbSet<PostKeyword> PostKeywords { get; set; }
    }
}
