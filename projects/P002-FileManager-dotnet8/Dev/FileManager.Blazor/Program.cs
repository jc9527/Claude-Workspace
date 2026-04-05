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

// Register HttpClient for Blazor SSR
builder.Services.AddHttpClient();

// Register services
builder.Services.AddScoped<IConfigService, ConfigService>();
builder.Services.AddScoped<IFileService, FileService>();
builder.Services.AddScoped<IFolderService, FolderService>();
builder.Services.AddSingleton<ITraceIdGenerator, TraceIdGenerator>();
builder.Services.AddRadzenComponents();

// Add services to the container.
builder.Services.AddControllers();
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

// Debug Trace Middleware
app.UseMiddleware<DebugTraceMiddleware>();

app.MapControllers();
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

Log.Information("FileManager Blazor Server starting...");

app.Run();
