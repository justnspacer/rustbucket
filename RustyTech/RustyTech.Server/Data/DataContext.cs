using Microsoft.AspNetCore.Identity;
using RustyTech.Server.Models.Auth;
using RustyTech.Server.Models.Posts;
using RustyTech.Server.Models.Role;
using System.Text;

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

            IdentityRole<string> admin = new IdentityRole<string>
            {
                Id = Guid.NewGuid().ToString(),
                Name = "SuperAdministrator",
                ConcurrencyStamp = "1",
                NormalizedName = "SUPERADMINISTRATOR"
            };
            modelBuilder.Entity<IdentityRole>().HasData(admin);

            User user = CreateUser("admin@rustbucket.io");
            modelBuilder.Entity<User>().HasData(user);

            modelBuilder.Entity<UserRole>().HasData(
                new UserRole()
                {
                    Id = 1,
                    UserId = user.Id,
                    RoleId = admin.Id
                }
                );

            // Configure the relationships and inheritance
            modelBuilder.Entity<Post>()
                .HasDiscriminator<string>("PostType")
                .HasValue<ImagePost>("ImagePost")
                .HasValue<VideoPost>("VideoPost")
                .HasValue<BlogPost>("BlogPost");

            modelBuilder.Entity<Post>(entity =>
            {
                entity.Property(p => p.Title)
                    .HasMaxLength(60)
                    .HasAnnotation("MinLength", 5);

                entity.Property(p => p.Content)
                .HasMaxLength(20000);

                entity.Property(p => p.PlainTextContent)
                .HasMaxLength(20000);

                entity.HasOne(p => p.User)
                    .WithMany(u => u.Posts)
                    .HasForeignKey(p => p.UserId)
                    .OnDelete(DeleteBehavior.Cascade); // Delete all posts when a user is deleted
            });

            modelBuilder.Entity<PostKeyword>()
                .HasOne(pk => pk.Post)
                .WithMany(p => p.Keywords)
                .HasForeignKey(p => p.PostId);

            modelBuilder.Entity<PostKeyword>()
                .HasOne(pk => pk.Keyword)
                .WithMany(k => k.PostKeywords)
                .HasForeignKey(k => k.KeywordId);

            modelBuilder.Entity<Keyword>()
                .Property(k => k.Text)
                .HasMaxLength(30);
        }

        public DbSet<User> Users { get; set; }
        public DbSet<LoginInfo> Logins { get; set; }
        public DbSet<IdentityRole> Roles { get; set; }
        public DbSet<UserRole> UserRoles { get; set; }

        public DbSet<BlogPost> BlogPosts { get; set; }
        public DbSet<ImagePost> ImagePosts { get; set; }
        public DbSet<VideoPost> VideoPosts { get; set; }
        public DbSet<Keyword> Keywords { get; set; }
        public DbSet<PostKeyword> PostKeywords { get; set; }

        private User CreateUser(string email)
        {
            User user = new User()
            {
                Id = Guid.NewGuid(),
                UserName = email,
                Email = email,
                NormalizedEmail = email.ToUpper(),
                NormalizedUserName = email.ToUpper(),
                EmailConfirmed = true,
                VerifiedAt = DateTime.Now
            };

            PasswordHasher<User> hasher = new PasswordHasher<User>();
            user.PasswordHash = Encoding.ASCII.GetBytes(hasher.HashPassword(user, email));
            return user;
        }
    }
}
