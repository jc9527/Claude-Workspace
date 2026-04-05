using FileManager.Blazor.Components;
using FileManager.Blazor.Middleware;
using FileManager.Blazor.Models.Config;
using FileManager.Blazor.Services;
using Microsoft.Extensions.Options;
using Radzen;
using Serilog;
using Serilog.Events;
using Serilog.Formatting.Compact;

var builder = WebApplication.CreateBuilder(args);

// Configure Serilog
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Debug()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Information)
    .MinimumLevel.Override("Microsoft.AspNetCore", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .Enrich.WithProperty("Application", "FileManager")
    .Enrich.WithProperty("Version", "1.0.0")
    .WriteTo.Console(new CompactJsonFormatter())
    .CreateLogger();

builder.Host.UseSerilog();

// Configure FileManager options
builder.Services.Configure<FileManagerOptions>(
    builder.Configuration.GetSection("FileManager"));

// Add Session
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromDays(7);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
    options.Cookie.Name = ".FileManager.Session";
});

// Add HttpContext accessor for HttpClient configuration
builder.Services.AddHttpContextAccessor();

// Register HttpClient for Blazor SSR
builder.Services.AddHttpClient("ServerAPI", (services, client) =>
{
    var httpContextAccessor = services.GetService<IHttpContextAccessor>();
    var request = httpContextAccessor?.HttpContext?.Request;
    if (request != null)
    {
        client.BaseAddress = new Uri($"{request.Scheme}://{request.Host}/");
    }
})
.ConfigurePrimaryHttpMessageHandler(() => new HttpClientHandler
{
    UseCookies = true,
    CookieContainer = new System.Net.CookieContainer()
});

// Register services
builder.Services.AddScoped<IConfigService, ConfigService>();
builder.Services.AddScoped<IServerAuthService, ServerAuthService>();
builder.Services.AddScoped<ISessionService, SessionService>();
builder.Services.AddScoped<IFileService, FileService>();
builder.Services.AddScoped<IFolderService, FolderService>();
builder.Services.AddSingleton<ITraceIdGenerator, TraceIdGenerator>();
builder.Services.AddRadzenComponents();

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddRazorPages();  // Add Razor Pages for _Host.cshtml
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
}

app.UseStaticFiles();
app.UseAntiforgery();
app.UseSession();

// Debug Trace Middleware
app.UseMiddleware<DebugTraceMiddleware>();

app.MapControllers();
app.MapRazorPages();  // Map Razor Pages
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

Log.Information("FileManager Blazor Server starting...");

app.Run();
