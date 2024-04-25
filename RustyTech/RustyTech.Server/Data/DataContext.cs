using Microsoft.AspNetCore.Identity;
using RustyTech.Server.Models.Auth;

namespace RustyTech.Server.Data
{
    public class DataContext : DbContext
    {
        public DataContext(DbContextOptions<DataContext> options) : base(options) { }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<User>().HasIndex(u => u.Email).IsUnique();
            modelBuilder.Entity<IdentityRole>().HasIndex(r => r.Name).IsUnique();
        }

        public DbSet<User> Users => Set<User>();
        public DbSet<LoginInfo> Logins => Set<LoginInfo>();
        public DbSet<IdentityRole> Roles => Set<IdentityRole>();
        //public DbSet<IdentityUserRole> UserRoles => Set<IdentityUserRole>();
    }
}
