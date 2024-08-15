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
using Microsoft.AspNetCore.Antiforgery;
using RustyTech.Server.Utilities;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Identity.UI.Services;

var builder = WebApplication.CreateBuilder(args); // Create a WebApplication builder instance.

// Add services to the container.

builder.Services.AddMemoryCache(); // Add in-memory caching services.

// Rate limiting configuration.
builder.Services.Configure<IpRateLimitOptions>(builder.Configuration.GetSection("IpRateLimiting")); // Configure IP rate limit options from configuration.
builder.Services.Configure<IpRateLimitPolicies>(builder.Configuration.GetSection("IpRateLimitPolicies")); // Configure IP rate limit policies from configuration.
builder.Services.AddInMemoryRateLimiting(); // Add in-memory rate limiting services.

// Add CORS policy
builder.Services.AddCors(options =>
{
    options.AddPolicy("MyCorsPolicy", policy =>
    {
        policy.WithOrigins("https://localhost:5173") // Allow requests from this origin.
              .AllowAnyHeader() // Allow any header.
              .AllowAnyMethod(); // Allow any HTTP method.
    });
});

// Add services for controllers
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull; // Ignore null values when serializing.
    });

builder.Services.AddAntiforgery(options =>
{
    options.HeaderName = "X-CSRF-TOKEN"; // Set the header name for CSRF tokens in AJAX requests.
    options.Cookie.Name = "XSRF-TOKEN";
    options.FormFieldName = "XSRF-TOKEN";
});

// Add authentication

/*
builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = CookieAuthenticationDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = CookieAuthenticationDefaults.AuthenticationScheme;
    options.DefaultSignInScheme = CookieAuthenticationDefaults.AuthenticationScheme;

}).AddCookie(CookieAuthenticationDefaults.AuthenticationScheme, option =>
{
    option.LoginPath = "/auth/login";
    option.LogoutPath = "/auth/logout";
    option.AccessDeniedPath = "/auth/access-denied";
    option.SlidingExpiration = true;
    option.ExpireTimeSpan = TimeSpan.FromMinutes(60);
    option.Cookie.HttpOnly = true;
    option.Cookie.SecurePolicy = CookieSecurePolicy.Always;
});
*/

builder.Services.AddAuthorization(); // Add authorization services.

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer(); // Add endpoint API explorer for Swagger.
builder.Services.AddRouting(options => options.LowercaseUrls = true); // Configure routing to use lowercase URLs.

builder.Services.AddSwaggerGen(config =>
{
    config.SwaggerDoc("v1", new() { Title = "RustyTech.Server", Version = "v1" }); // Configure Swagger document.
    config.OperationFilter<AddFileUploadParams>(); // Add file upload parameters to Swagger UI.
});

builder.Services.AddDbContext<DataContext>(options => options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection"))); // Add Entity Framework Core services with SQL Server configuration.

builder.Services.AddIdentity<User, IdentityRole>(options => options.SignIn.RequireConfirmedAccount = true).AddEntityFrameworkStores<DataContext>(); // Add ASP.NET Core Identity services with roles and EF Core store.
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
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
    options.Lockout.MaxFailedAccessAttempts = 5;
    options.Lockout.AllowedForNewUsers = true;

    //user settings
    options.User.AllowedUserNameCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._@+";
    options.User.RequireUniqueEmail = true;
});

builder.Services.ConfigureApplicationCookie(options =>
{
    //cookie settings
    options.Cookie.HttpOnly = true;
    options.ExpireTimeSpan = TimeSpan.FromMinutes(5); //double check this!!!!!!!!!!!!!!!!!!!!!!!!!!!
    options.LoginPath = "/auth/login";
    options.AccessDeniedPath = "/auth/access-denied";
    options.SlidingExpiration = true;
});
builder.Services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies());

builder.Services.AddSingleton<IRateLimitConfiguration, RateLimitConfiguration>(); // Add rate limit configuration as a singleton.
builder.Services.AddSingleton<Ganss.Xss.HtmlSanitizer>();
builder.Services.AddTransient<ISmtpClientService, SmtpClientService>(); // Add smtp client service with transient lifetime.
builder.Services.AddScoped<IAuthService, AuthService>(); // Add authentication service with scoped lifetime.
builder.Services.AddScoped<IRoleService, RoleService>(); // Add role service with scoped lifetime.
builder.Services.AddScoped<IUserService, UserService>(); // Add user service with scoped lifetime.
builder.Services.AddTransient<IEmailService, EmailService>(); // Add email service with transient lifetime.
builder.Services.AddTransient<IEmailSender, EmailSender>(); // Add email sender with transient lifetime.
builder.Services.AddScoped<IPostService, PostService>(); // Add post service with scoped lifetime.
builder.Services.AddScoped<IImageService, ImageService>(); // Add image service with scoped lifetime.
builder.Services.AddScoped<IVideoService, VideoService>(); // Add video service with scoped lifetime.
builder.Services.AddScoped<IKeywordService, KeywordService>(); // Add keyword service with scoped lifetime.

builder.Services.Configure<RequestLocalizationOptions>(options =>
{
    var supportedCultures = new[]
    {
        new CultureInfo("en-US"), // Add US English culture.
        new CultureInfo("es-ES"), // Add Spanish culture.
    };
    options.DefaultRequestCulture = new RequestCulture("en-US"); // Set default request culture to US English.
    options.SupportedCultures = supportedCultures; // Set supported cultures.
    options.SupportedUICultures = supportedCultures; // Set supported UI cultures.
});

builder.Logging.ClearProviders(); // Clear default logging providers.
builder.Logging.AddNLog(); // Add NLog provider for logging.
builder.Logging.AddConsole(); // Add console provider for logging.
builder.Logging.AddDebug(); // Add debug provider for logging.

var app = builder.Build(); // Build the WebApplication.

// Middleware to use CORS policy.
app.UseCors("MyCorsPolicy");

app.UseCookiePolicy(new CookiePolicyOptions
{
    MinimumSameSitePolicy = SameSiteMode.Strict, // Set the minimum same site policy to strict.
});



// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger(); // Enable Swagger middleware.
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "RustyTech.Server v1"); // Configure Swagger endpoint.
    });
}

// Middleware for handling responses and exceptions.
app.UseMiddleware<ResponseMiddleware>(); // Use custom response middleware.
app.UseMiddleware<ExceptionMiddleware>(); // Use custom exception middleware.

app.UseIpRateLimiting(); // Enable IP rate limiting.

app.UseHttpsRedirection(); // Redirect HTTP requests to HTTPS.
app.UseDefaultFiles(); // Enable default file mapping for the app.
app.UseStaticFiles(); // Enable static file serving.

app.UseRouting(); // Enable routing middleware.

app.UseAuthentication(); // Enable authentication middleware.
app.UseAuthorization(); // Enable authorization middleware.

//CSRF token is generated and stored in a cookie named XSRF-TOKEN
/*
app.Use(next => context =>
{
    var antiforgery = context.RequestServices.GetRequiredService<IAntiforgery>();
    var tokens = antiforgery.GetAndStoreTokens(context);
    context.Response.Cookies.Append("XSRF-TOKEN", tokens.RequestToken!, new CookieOptions { HttpOnly = false });

    return next(context);
});
*/

app.MapControllers(); // Map controller routes.
app.MapFallbackToFile("/index.html"); // Map fallback route to serve index.html for SPA.

app.Run(); // Run the application.
