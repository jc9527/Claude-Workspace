using FileManager.Blazor.Models.Config;
using Microsoft.Extensions.Options;

namespace FileManager.Blazor.Services;

public class ConfigService : IConfigService
{
    private readonly FileManagerOptions _options;

    public ConfigService(IOptions<FileManagerOptions> options)
    {
        _options = options.Value;
    }

    public FileManagerOptions Options => _options;

    public string GetRootFolder() => _options.RootFolder;

    public List<string> GetAllowedDomains() => new() { "sinopac.com", "skl.com", "devpro.com.tw" };

    public bool IsPathAllowed(string path)
    {
        if (string.IsNullOrEmpty(path)) return false;
        var rootPath = Path.GetFullPath(_options.RootFolder).TrimEnd(Path.DirectorySeparatorChar);
        var fullPath = Path.GetFullPath(path).TrimEnd(Path.DirectorySeparatorChar);
        return fullPath.StartsWith(rootPath + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase)
               || fullPath.Equals(rootPath, StringComparison.OrdinalIgnoreCase);
    }

    public bool HasPermission(string permission)
    {
        return permission switch
        {
            PermissionKeys.AllowDownload => _options.Permissions.AllowDownload,
            PermissionKeys.AllowCreate => _options.Permissions.AllowCreate,
            PermissionKeys.AllowRename => _options.Permissions.AllowRename,
            PermissionKeys.AllowMove => _options.Permissions.AllowMove,
            PermissionKeys.AllowDelete => _options.Permissions.AllowDelete,
            PermissionKeys.EnabledUpload => _options.Permissions.EnabledUpload,
            PermissionKeys.EnableUploadMultiSelect => _options.Permissions.EnableUploadMultiSelect,
            PermissionKeys.EnableDownloadMultiSelect => _options.Permissions.EnableDownloadMultiSelect,
            _ => false
        };
    }
}
