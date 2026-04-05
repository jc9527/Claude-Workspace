namespace FileManager.Blazor.Models.Config;

public class FileManagerOptions
{
    public string RootFolder { get; set; } = "/app/data";
    public string[] AllowedFileExtensions { get; set; } = ["*"];
    public int MaxRequestLength { get; set; } = 4096;
    public PermissionOptions Permissions { get; set; } = new();
    public UiOptions UI { get; set; } = new();
}

public class PermissionOptions
{
    public bool AllowDownload { get; set; } = true;
    public bool AllowCreate { get; set; } = true;
    public bool AllowRename { get; set; } = true;
    public bool AllowMove { get; set; } = true;
    public bool AllowDelete { get; set; } = true;
    public bool EnabledUpload { get; set; } = true;
    public bool EnableUploadMultiSelect { get; set; } = true;
    public bool EnableDownloadMultiSelect { get; set; } = true;
}

public class UiOptions
{
    public bool ShowPath { get; set; } = true;
    public bool ShowFilterBox { get; set; } = true;
    public bool ShowExpandButtons { get; set; } = true;
    public bool ShowFolderIcons { get; set; } = true;
    public bool ShowTreeLines { get; set; } = true;
    public bool ShowFolders { get; set; } = true;
    public bool ShowParentFolder { get; set; } = true;
    public bool BreadcrumbsVisible { get; set; } = true;
    public int BreadcrumbsPosition { get; set; } = 0;
    public int FileListViewMode { get; set; } = 1;
}
