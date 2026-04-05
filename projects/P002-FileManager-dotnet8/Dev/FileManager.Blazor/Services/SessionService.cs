using System.Net.Http.Json;
using Microsoft.AspNetCore.Components;

namespace FileManager.Blazor.Services;

public interface ISessionService
{
    Task<(string? email, bool isAdmin)> GetCurrentUserAsync();
    Task<bool> IsAuthenticatedAsync();
    Task LogoutAsync();
}

public class SessionService : ISessionService
{
    private readonly HttpClient _http;

    public SessionService(HttpClient http)
    {
        _http = http;
    }

    public async Task<(string? email, bool isAdmin)> GetCurrentUserAsync()
    {
        try
        {
            var response = await _http.GetAsync("api/auth/session");
            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content.ReadFromJsonAsync<SessionResponse>();
                if (result?.IsAuthenticated == true)
                {
                    return (result.Email, result.IsAdmin);
                }
            }
        }
        catch
        {
            // Ignore errors
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
            await _http.PostAsync("api/auth/logout", null);
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