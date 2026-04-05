namespace FileManager.Blazor.Services;

public interface IServerAuthService
{
    Task<bool> ValidateCredentialsAsync(string email, string password);
    Task<bool> IsAdminAsync(string email);
    Task CreateUserFolderAsync(string email);
    Task SignInAsync(HttpContext context, string email, bool isAdmin);
    Task<(string? email, bool isAdmin)> GetSessionAsync(HttpContext context);
    Task SignOutAsync(HttpContext context);
}

public class ServerAuthService : IServerAuthService
{
    private readonly IConfigService _configService;

    public ServerAuthService(IConfigService configService)
    {
        _configService = configService;
    }

    public Task<bool> ValidateCredentialsAsync(string email, string password)
    {
        if (string.IsNullOrEmpty(password) || password.Length < 3)
            return Task.FromResult(false);

        var allowedDomains = _configService.GetAllowedDomains();
        var emailDomain = email.Contains('@') ? email.Split('@').Last().ToLower() : "";

        if (string.IsNullOrEmpty(emailDomain) || !allowedDomains.Contains(emailDomain))
            return Task.FromResult(false);

        return Task.FromResult(password == email);
    }

    public Task<bool> IsAdminAsync(string email)
    {
        if (string.IsNullOrEmpty(email) || !email.Contains('@'))
            return Task.FromResult(false);

        var domain = email.Split('@').Last().ToLower();
        return Task.FromResult(domain == "devpro.com.tw");
    }

    public async Task CreateUserFolderAsync(string email)
    {
        if (string.IsNullOrEmpty(email) || !email.Contains('@'))
            return;

        var domain = email.Split('@').Last().ToLower();
        var rootFolder = _configService.GetRootFolder();
        var userPath = Path.Combine(rootFolder, "users", domain, email);

        if (!Directory.Exists(userPath))
        {
            await Task.Run(() => Directory.CreateDirectory(userPath));
        }
    }

    public Task SignInAsync(HttpContext context, string email, bool isAdmin)
    {
        context.Session.SetString("userEmail", email);
        context.Session.SetString("isAdmin", isAdmin.ToString().ToLower());
        return Task.CompletedTask;
    }

    public Task<(string? email, bool isAdmin)> GetSessionAsync(HttpContext context)
    {
        var email = context.Session.GetString("userEmail");
        var isAdminStr = context.Session.GetString("isAdmin");
        var isAdmin = isAdminStr == "true";
        return Task.FromResult((email, isAdmin));
    }

    public Task SignOutAsync(HttpContext context)
    {
        context.Session.Clear();
        return Task.CompletedTask;
    }
}