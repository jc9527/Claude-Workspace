using Microsoft.AspNetCore.Components;
using Microsoft.JSInterop;

namespace FileManager.Blazor.Services;

public interface ISessionService
{
    Task<(string? email, bool isAdmin)> GetCurrentUserAsync();
    Task<bool> IsAuthenticatedAsync();
    Task LogoutAsync();
}

public class SessionService : ISessionService
{
    private readonly IJSRuntime _js;

    public SessionService(IJSRuntime js)
    {
        _js = js;
    }

    public async Task<(string? email, bool isAdmin)> GetCurrentUserAsync()
    {
        try
        {
            var result = await _js.InvokeAsync<SessionResponse>("getCurrentUser");
            if (result?.IsAuthenticated == true)
            {
                return (result.Email, result.IsAdmin);
            }
        }
        catch
        {
            // Ignore errors (e.g., circuit not ready)
        }
        return (null, false);
    }

    public async Task<bool> IsAuthenticatedAsync()
    {
        var (email, _) = await GetCurrentUserAsync();
        return !string.IsNullOrEmpty(email);
    }

    public async Task LogoutAsync()
    {
        try
        {
            await _js.InvokeVoidAsync("performLogout");
        }
        catch
        {
            // Ignore errors
        }
    }
}

public class SessionResponse
{
    public bool IsAuthenticated { get; set; }
    public string? Email { get; set; }
    public bool IsAdmin { get; set; }
}
