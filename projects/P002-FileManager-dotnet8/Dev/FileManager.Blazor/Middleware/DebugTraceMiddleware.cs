using System.Diagnostics;
using FileManager.Blazor.Services;

namespace FileManager.Blazor.Middleware;

public class DebugTraceMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<DebugTraceMiddleware> _logger;
    private readonly ITraceIdGenerator _traceIdGenerator;

    public DebugTraceMiddleware(
        RequestDelegate next,
        ILogger<DebugTraceMiddleware> logger,
        ITraceIdGenerator traceIdGenerator)
    {
        _next = next;
        _logger = logger;
        _traceIdGenerator = traceIdGenerator;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // Determine dimension and function from path
        var (dimension, function) = DetermineDimensionAndFunction(context.Request.Path);

        // Get or generate Trace ID
        var traceId = context.Request.Headers["X-Trace-ID"].FirstOrDefault()
            ?? _traceIdGenerator.Generate(dimension, function);

        // Start timing
        var stopwatch = Stopwatch.StartNew();

        // Store in HttpContext.Items for downstream access
        context.Items["TraceId"] = traceId;
        context.Items["Dimension"] = dimension;
        context.Items["Function"] = function;

        // Get QA Debug Info if present
        var qaDebugInfo = context.Request.Headers["X-QA-Debug-Info"].FirstOrDefault();
        var testingCase = context.Request.Headers["X-Testing-Case"].FirstOrDefault();

        // Add response headers
        context.Response.OnStarting(() =>
        {
            context.Response.Headers["X-Trace-ID"] = traceId;
            context.Response.Headers["X-Request-Duration-Ms"] = stopwatch.ElapsedMilliseconds.ToString();
            context.Response.Headers["X-Server-Time"] = DateTime.UtcNow.ToString("o");

            if (!string.IsNullOrEmpty(qaDebugInfo))
            {
                context.Response.Headers["X-QA-Debug-Info"] = qaDebugInfo;
            }

            return Task.CompletedTask;
        });

        // Structured logging with scope
        using (_logger.BeginScope(new Dictionary<string, object?>
        {
            ["TraceId"] = traceId,
            ["Dimension"] = dimension,
            ["Function"] = function,
            ["Method"] = context.Request.Method,
            ["Path"] = context.Request.Path.ToString(),
            ["QueryString"] = context.Request.QueryString.ToString(),
            ["TestingCase"] = testingCase,
            ["QADebugInfo"] = qaDebugInfo,
            ["ClientIP"] = context.Connection.RemoteIpAddress?.ToString(),
            ["UserAgent"] = context.Request.Headers["User-Agent"].FirstOrDefault()
        }))
        {
            try
            {
                await _next(context);

                stopwatch.Stop();

                _logger.LogInformation(
                    "Request completed: {Method} {Path} responded {StatusCode} in {DurationMs}ms",
                    context.Request.Method,
                    context.Request.Path,
                    context.Response.StatusCode,
                    stopwatch.ElapsedMilliseconds);
            }
            catch (Exception ex)
            {
                stopwatch.Stop();

                _logger.LogError(ex,
                    "Request failed: {Method} {Path} after {DurationMs}ms - {ErrorMessage}",
                    context.Request.Method,
                    context.Request.Path,
                    stopwatch.ElapsedMilliseconds,
                    ex.Message);

                throw;
            }
        }
    }

    private static (string dimension, string function) DetermineDimensionAndFunction(PathString path)
    {
        var pathValue = path.Value?.ToLowerInvariant() ?? string.Empty;

        if (pathValue.StartsWith("/api/files"))
            return ("API", "Browse");
        if (pathValue.StartsWith("/api/folders"))
            return ("FOLDER", DetermineFolderFunction(pathValue));
        if (pathValue.StartsWith("/api/upload"))
            return ("UPLOAD", "Upload");
        if (pathValue.StartsWith("/api/settings"))
            return ("API", "Settings");

        return ("API", "Unknown");
    }

    private static string DetermineFolderFunction(string path)
    {
        if (path.Contains("/tree"))
            return "Tree";
        if (path.Contains("/rename"))
            return "Rename";
        if (path.Contains("/move"))
            return "Move";
        if (path.Contains("/delete"))
            return "Delete";
        return "Create";
    }
}
