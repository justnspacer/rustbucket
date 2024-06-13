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
            optionsBuilder.UseSqlServer("Server=.\\Rustbucket;Database=RustyTech;Trusted_Connection=True;TrustServerCertificate=True");
        }

        public DbSet<User> Users { get; set; }
        public DbSet<LoginInfo> Logins { get; set; }
        public DbSet<IdentityRole> Roles { get; set; }
        public DbSet<UserRole> UserRoles { get; set; }
    }
}
