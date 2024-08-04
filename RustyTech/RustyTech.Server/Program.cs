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
using Microsoft.IdentityModel.Tokens;
using System.Text;
using Microsoft.OpenApi.Models;
using RustyTech.Server.Services.Interfaces;
using RustyTech.Server.Interfaces;
using Microsoft.AspNetCore.Antiforgery;
using RustyTech.Server.Utilities;

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
builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = "Bearer"; // Set the default authentication scheme to "Bearer".
    options.DefaultChallengeScheme = "Bearer"; // Set the default challenge scheme to "Bearer".
})
.AddJwtBearer("Bearer", options =>
{
    options.Authority = "https://some-authentication-authority.com"; // Set the authority for token validation.
    options.Audience = "some-audience"; // Set the expected audience for the token.
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateAudience = true, // Validate the audience in the token.
        ValidateIssuer = true, // Validate the issuer in the token.
        ValidateLifetime = true, // Validate the token's lifetime.
        ValidateIssuerSigningKey = true, // Validate the token's signing key.
        ValidIssuer = builder.Configuration.GetSection("Jwt:Issuer").Value, // Set the valid issuer from configuration.
        ValidAudience = builder.Configuration.GetSection("Jwt:Audience").Value, // Set the valid audience from configuration.
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(builder.Configuration.GetSection("Jwt:Key").Value)) // Set the signing key from configuration.
    };
});

builder.Services.AddAuthorization(); // Add authorization services.

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer(); // Add endpoint API explorer for Swagger.
builder.Services.AddRouting(options => options.LowercaseUrls = true); // Configure routing to use lowercase URLs.
builder.Services.AddSwaggerGen(config =>
{
    config.SwaggerDoc("v1", new() { Title = "RustyTech.Server", Version = "v1" }); // Configure Swagger document.
    config.OperationFilter<AddFileUploadParams>(); // Add file upload parameters to Swagger UI.

    config.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        In = ParameterLocation.Header, // Define the location of the security scheme (header).
        Description = "Please enter JWT with Bearer into field", // Description for the security scheme.
        Name = "Authorization", // Name of the security scheme.
        Type = SecuritySchemeType.ApiKey, // Type of the security scheme (API key).
        Scheme = "Bearer" // The scheme name (Bearer).
    });

    config.AddSecurityRequirement(new OpenApiSecurityRequirement {
            {
                new OpenApiSecurityScheme
                {
                    Reference = new OpenApiReference
                    {
                        Type = ReferenceType.SecurityScheme, // Reference type is a security scheme.
                        Id = "Bearer" // The ID of the security scheme.
                    }
                },
                new string[] { } // Required scopes for the security scheme.
            }
        });
});

builder.Services.AddDbContext<DataContext>(options => options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection"))); // Add Entity Framework Core services with SQL Server configuration.


builder.Services.AddIdentityCore<User>().AddRoles<IdentityRole>().AddEntityFrameworkStores<DataContext>(); // Add ASP.NET Core Identity services with roles and EF Core store.

builder.Services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies());

builder.Services.AddSingleton<IRateLimitConfiguration, RateLimitConfiguration>(); // Add rate limit configuration as a singleton.
builder.Services.AddSingleton<Ganss.Xss.HtmlSanitizer>();
builder.Services.AddScoped<ISmtpClientService, SmtpClientService>(); // Add smtp client service with scoped lifetime.
builder.Services.AddScoped<IAuthService, AuthService>(); // Add authentication service with scoped lifetime.
builder.Services.AddScoped<IRoleService, RoleService>(); // Add role service with scoped lifetime.
builder.Services.AddScoped<IUserService, UserService>(); // Add user service with scoped lifetime.
builder.Services.AddScoped<IEmailService, EmailService>(); // Add email service with scoped lifetime.
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

app.UseDefaultFiles(); // Enable default file mapping for the app.
app.UseStaticFiles(); // Enable static file serving.

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

app.UseAuthentication(); // Enable authentication middleware.

app.UseRouting(); // Enable routing middleware.

app.UseAuthorization(); // Enable authorization middleware.

//CSRF token is generated and stored in a cookie named XSRF-TOKEN
app.Use(next => context =>
{
    var antiforgery = context.RequestServices.GetRequiredService<IAntiforgery>();
    var tokens = antiforgery.GetAndStoreTokens(context);
    context.Response.Cookies.Append("XSRF-TOKEN", tokens.RequestToken!, new CookieOptions { HttpOnly = false });

    return next(context);
});

app.MapControllers(); // Map controller routes.

app.MapFallbackToFile("/index.html"); // Map fallback route to serve index.html for SPA.

app.Run(); // Run the application.
