global using Microsoft.EntityFrameworkCore;
global using RustyTech.Server.Models;
global using RustyTech.Server.Data;

using AspNetCoreRateLimit;
using Microsoft.AspNetCore.Identity;
using NLog.Extensions.Logging;
using RustyTech.Server.Services;
using System.Globalization;
using Microsoft.AspNetCore.Localization;
using RustyTech.Server.Middleware;
using RustyTech.Server.Services.Interfaces;
using RustyTech.Server.Interfaces;
using RustyTech.Server.Utilities;

var builder = WebApplication.CreateBuilder(args); // Create a WebApplication builder instance.

// Add services to the container.

builder.Services.AddMemoryCache(); // Add in-memory caching services.

// Rate limiting configuration.
builder.Services.Configure<IpRateLimitOptions>(builder.Configuration.GetSection("IpRateLimiting")); // Configure IP rate limit options from configuration.
builder.Services.Configure<IpRateLimitPolicies>(builder.Configuration.GetSection("IpRateLimitPolicies")); // Configure IP rate limit policies from configuration.
builder.Services.AddInMemoryRateLimiting();

// Add CORS policy
builder.Services.AddCors(options =>
{
    options.AddPolicy("MyCorsPolicy", policy =>
    {
        policy.WithOrigins("https://localhost:5173")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
});

// Add services for controllers
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull; // Ignore null values when serializing.
    });


builder.Services.AddAuthorization();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddRouting(options => options.LowercaseUrls = true);

builder.Services.AddSwaggerGen(config =>
{
    config.SwaggerDoc("v1", new() { Title = "RustyTech.Server", Version = "v1" });
    config.OperationFilter<AddFileUploadParams>();
});

builder.Services.AddDbContext<DataContext>(options => options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection"))); // Add Entity Framework Core services with SQL Server configuration.

builder.Services.AddIdentity<User, IdentityRole>(options => options.SignIn.RequireConfirmedAccount = true)
    .AddEntityFrameworkStores<DataContext>().AddDefaultTokenProviders();
builder.Services.Configure<IdentityOptions>(options =>
{
    //password settings
    options.Password.RequireDigit = true;
    options.Password.RequireLowercase = true;
    options.Password.RequireNonAlphanumeric = true;
    options.Password.RequireUppercase = true;
    options.Password.RequiredLength = 8;
    options.Password.RequiredUniqueChars = 1;

    //lockout settings
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(10);
    options.Lockout.MaxFailedAccessAttempts = 6;
    options.Lockout.AllowedForNewUsers = true;

    //user settings
    options.User.AllowedUserNameCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._@+";
    options.User.RequireUniqueEmail = true;
});

builder.Services.Configure<DataProtectionTokenProviderOptions>(options =>
{
    options.TokenLifespan = TimeSpan.FromHours(3);
});

builder.Services.ConfigureApplicationCookie(options =>
{
    //cookie settings
    options.Cookie.HttpOnly = true;
    options.ExpireTimeSpan = TimeSpan.FromMinutes(30); //double check this!!!!!!!!!!!!!!!!!!!!!!!!!!!
    options.LoginPath = "/login";
    options.AccessDeniedPath = "/access-denied";
    options.SlidingExpiration = true;
    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
});
builder.Services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies());

builder.Services.AddSingleton<IRateLimitConfiguration, RateLimitConfiguration>(); 
builder.Services.AddSingleton<Ganss.Xss.HtmlSanitizer>();
builder.Services.AddTransient<ISmtpClientService, SmtpClientService>(); 
builder.Services.AddScoped<IAccountService, AccountService>(); 
builder.Services.AddScoped<IRoleService, RoleService>(); 
builder.Services.AddScoped<IUserService, UserService>(); 
builder.Services.AddTransient<IEmailService, EmailService>(); 
builder.Services.AddScoped<IPostService, PostService>(); 
builder.Services.AddScoped<IImageService, ImageService>();
builder.Services.AddScoped<IVideoService, VideoService>();
builder.Services.AddScoped<IKeywordService, KeywordService>();
builder.Services.Configure<RequestLocalizationOptions>(options =>
{
    var supportedCultures = new[]
    {
        new CultureInfo("en-US"), // Add US English culture.
        new CultureInfo("es-ES"), // Add Spanish culture.
    };
    options.DefaultRequestCulture = new RequestCulture("en-US");
    options.SupportedCultures = supportedCultures;
    options.SupportedUICultures = supportedCultures; 
});

builder.Logging.ClearProviders();
builder.Logging.AddNLog();
builder.Logging.AddConsole();
builder.Logging.AddDebug();

var superadminUserExists = await CheckSuperadminUserExistsAsync(builder.Services);

if (!superadminUserExists)
{
    await CreateSuperadminUserAsync(builder.Services);
}

var app = builder.Build();


app.UseCors("MyCorsPolicy");

app.UseCookiePolicy(new CookiePolicyOptions
{
    MinimumSameSitePolicy = SameSiteMode.Strict,
});

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "RustyTech.Server v1");
    });
}

app.UseMiddleware<ResponseMiddleware>();
app.UseMiddleware<ExceptionMiddleware>();

app.UseIpRateLimiting();

app.UseHttpsRedirection();
app.UseDefaultFiles();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();
app.MapFallbackToFile("/index.html");

async Task<bool> CheckSuperadminUserExistsAsync(IServiceCollection services)
{
    using (var scope = services.BuildServiceProvider().CreateScope())
    {
        var userManager = scope.ServiceProvider.GetRequiredService<UserManager<User>>();
        var user = await userManager.FindByEmailAsync("justin@rustbucket.io");

        return user != null;
    }
}

async Task CreateSuperadminUserAsync(IServiceCollection services)
{
    using (var scope = services.BuildServiceProvider().CreateScope())
    {
        var adminPassword = builder.Configuration.GetSection("AdminUser:Password").Value;
        var userManager = scope.ServiceProvider.GetRequiredService<UserManager<User>>();
        var roleManager = scope.ServiceProvider.GetRequiredService<RoleManager<IdentityRole>>();

        // Create the superadmin role if it doesn't exist
        var roleExists = await roleManager.RoleExistsAsync("SuperAdmin");
        if (!roleExists)
        {
            await roleManager.CreateAsync(new IdentityRole("SuperAdmin"));
        }

        var user = new User
        {
            UserName = builder.Configuration.GetSection("AdminUser:Email").Value,
            Email = builder.Configuration.GetSection("AdminUser:Email").Value,
            VerifiedAt = DateTime.Now,
            EmailConfirmed = true            
        };

        if (adminPassword == null)
        {
            throw new Exception("Admin password required.");
        }

        var result = await userManager.CreateAsync(user, adminPassword);

        if (result.Succeeded)
        {
            await userManager.AddToRoleAsync(user, "SuperAdmin");
        }
        else
        {
            throw new Exception("Failed to create superadmin user.");
        }
    }
}

app.Run();

