﻿using Microsoft.AspNetCore.Identity;
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
                .HasValue<ImagePost>("ImagePost")
                .HasValue<VideoPost>("VideoPost")
                .HasValue<BlogPost>("BlogPost");

            modelBuilder.Entity<Post>()
                .HasOne(p => p.User)
                .WithMany(u => u.Posts)
                .HasForeignKey(p => p.UserId);
        }

        public DbSet<User> Users { get; set; }
        public DbSet<LoginInfo> Logins { get; set; }
        public DbSet<IdentityRole> Roles { get; set; }
        public DbSet<UserRole> UserRoles { get; set; }

        public DbSet<BlogPost> BlogPosts { get; set; }
        public DbSet<ImagePost> ImagePosts { get; set; }
        public DbSet<VideoPost> VideoPosts { get; set; }
    }
}
