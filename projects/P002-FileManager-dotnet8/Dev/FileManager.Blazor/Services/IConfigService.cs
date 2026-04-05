using FileManager.Blazor.Models.Config;

namespace FileManager.Blazor.Services;

public interface IConfigService
{
    FileManagerOptions Options { get; }
    string GetRootFolder();
    List<string> GetAllowedDomains();
    bool IsPathAllowed(string path);
    bool HasPermission(string permission);
}

public static class PermissionKeys
{
    public const string AllowDownload = "AllowDownload";
    public const string AllowCreate = "AllowCreate";
    public const string AllowRename = "AllowRename";
    public const string AllowMove = "AllowMove";
    public const string AllowDelete = "AllowDelete";
    public const string EnabledUpload = "EnabledUpload";
    public const string EnableUploadMultiSelect = "EnableUploadMultiSelect";
    public const string EnableDownloadMultiSelect = "EnableDownloadMultiSelect";
}