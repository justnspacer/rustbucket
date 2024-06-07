global using Microsoft.EntityFrameworkCore;
global using RustyTech.Server.Models.User;
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
        policy.WithOrigins("https://localhost:5173")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

builder.Services.AddControllers();
builder.Services.AddAntiforgery(options =>
{
    options.HeaderName = "X-CSRF-TOKEN"; // Set the header name to be used in AJAX requests
});


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
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateAudience = true,
        ValidateIssuer = true,
        ValidateLifetime = true,
        ValidateIssuerSigningKey = true,
        ValidIssuer = builder.Configuration.GetSection("Jwt:Issuer").Value,
        ValidAudience = builder.Configuration.GetSection("Jwt:Audience").Value,
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(builder.Configuration.GetSection("Jwt:Key").Value))
    };
});

builder.Services.AddAuthorization();

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddRouting(options => options.LowercaseUrls = true);
builder.Services.AddSwaggerGen(config =>
{
    config.SwaggerDoc("v1", new() { Title = "RustyTech.Server", Version = "v1" });

    config.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        In = ParameterLocation.Header,
        Description = "Please enter JWT with Bearer into field",
        Name = "Authorization",
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });

    config.AddSecurityRequirement(new OpenApiSecurityRequirement {
            {
                new OpenApiSecurityScheme
                {
                    Reference = new OpenApiReference
                    {
                        Type = ReferenceType.SecurityScheme,
                        Id = "Bearer"
                    }
                },
                new string[] { }
            }
        });
});
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

//middleware
app.UseCors("MyCorsPolicy");

app.UseDefaultFiles();
app.UseStaticFiles();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "RustyTech.Server v1");
    });
}

//middleware
app.UseMiddleware<ResponseMiddleware>();
app.UseMiddleware<ExceptionMiddleware>();

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

app.Run();
