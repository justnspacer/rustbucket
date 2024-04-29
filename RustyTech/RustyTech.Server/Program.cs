global using Microsoft.EntityFrameworkCore;
global using RustyTech.Server.Models.User;
global using RustyTech.Server.Data;

using AspNetCoreRateLimit;
using Microsoft.AspNetCore.Identity;
using NLog.Extensions.Logging;
using RustyTech.Server.Services;
using System.Globalization;
using Microsoft.AspNetCore.Localization;
using RustyTech.Server.Models.Role;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddMemoryCache();
builder.Services.Configure<IpRateLimitOptions>(builder.Configuration.GetSection("IpRateLimiting"));
builder.Services.Configure<IpRateLimitPolicies>(builder.Configuration.GetSection("IpRateLimitPolicies"));
builder.Services.AddInMemoryRateLimiting();

// Add CORS policy
builder.Services.AddCors(options =>
{
    options.AddPolicy("MyCorsPolicy", policy =>
    {
        policy.WithOrigins("http://localhost:3000")  // React's URL
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

builder.Services.AddControllers();



// Add authentication
builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = "Bearer";
    options.DefaultChallengeScheme = "Bearer";
})
.AddJwtBearer("Bearer", options =>
{
    options.Authority = "https://some-authentication-authority.com";
    options.Audience = "some-audience";
});

builder.Services.AddAuthorization();

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddRouting(options => options.LowercaseUrls = true);
builder.Services.AddSwaggerGen();

builder.Services.AddDbContext<DataContext>(options =>
       options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));
builder.Services.AddIdentityCore<User>().AddRoles<IdentityRole>().AddEntityFrameworkStores<DataContext>();

builder.Services.AddSingleton<IRateLimitConfiguration, RateLimitConfiguration>();
builder.Services.AddScoped<AuthService, AuthService>();
builder.Services.AddScoped<RoleService, RoleService>();
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IEmailService, EmailService>();

builder.Services.Configure<RequestLocalizationOptions>(options =>
{
    var supportedCultures = new[]
    {
        new CultureInfo("en-US"),
        new CultureInfo("es-ES"),
    };
    options.DefaultRequestCulture = new RequestCulture("en-US");
    options.SupportedCultures = supportedCultures;
    options.SupportedUICultures = supportedCultures;
});

builder.Logging.AddNLog();

var app = builder.Build();

app.UseCors("MyCorsPolicy");

app.UseDefaultFiles();
app.UseStaticFiles();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseIpRateLimiting();

app.UseHttpsRedirection();

app.UseAuthentication();

app.UseRouting();

app.UseAuthorization();

app.MapControllers();

app.MapFallbackToFile("/index.html");

//role management
using (var scope = app.Services.CreateScope())
{
    var roleService = scope.ServiceProvider.GetRequiredService<RoleService>();
    var roles = new[] { "Admin", "Manager", "User", "Guest" };
    foreach (var role in roles)
    {
        await roleService.CreateRoleAsync(role);
    }
}

//create a admin if doesn't exist
using (var scope = app.Services.CreateScope())
{
    var userService = scope.ServiceProvider.GetRequiredService<IUserService>();
    var authService = scope.ServiceProvider.GetRequiredService<AuthService>();
    var roleService = scope.ServiceProvider.GetRequiredService<RoleService>();

    string email = "admin@rustbucket.io";
    string password = "Adm1nTheMadm@n";
    if (await userService.FindByEmailAsync(email) == null)
    {
        var request = new UserRegister() { Email = email, Password = password, ConfirmPassword = password, BirthYear = 1989  };
        await authService.RegisterAsync(request);

        var role = await roleService.GetRoleByNameAsync("Admin");
        var user = await userService.FindByEmailAsync(email);
        var roleRequest = new RoleRequest() { RoleId = role?.Id, UserId = user?.Id };

        await roleService.AddRoleToUserAsync(roleRequest);
    }
}

app.Run();
