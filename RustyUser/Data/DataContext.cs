

using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using RustyUser.Models.User;

namespace RustyUser.Data
{
    public class DataContext : IdentityDbContext<User>
    {
        public DataContext(DbContextOptions<DataContext> options) : base(options)
        {
                
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            base.OnConfiguring(optionsBuilder);
            optionsBuilder.UseSqlServer("Server=.\\Rustbucket;Database=UserDb;Trusted_Connection=True;TrustServerCertificate=True");
        }
    }
}
