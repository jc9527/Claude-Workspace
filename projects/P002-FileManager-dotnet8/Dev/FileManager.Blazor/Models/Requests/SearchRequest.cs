namespace FileManager.Blazor.Models.Requests;

public class SearchRequest
{
    public string SearchPath { get; set; } = string.Empty;
    public string? Keyword { get; set; }
    public string[]? FileExtensions { get; set; }
    public bool IncludeDirectories { get; set; } = true;
    public bool CaseSensitive { get; set; } = false;
}

public class RenameRequest
{
    public string CurrentPath { get; set; } = string.Empty;
    public string NewName { get; set; } = string.Empty;
}

public class MoveRequest
{
    public List<string> SourcePaths { get; set; } = new();
    public string DestinationPath { get; set; } = string.Empty;
}

public class CreateFolderRequest
{
    public string ParentPath { get; set; } = string.Empty;
    public string FolderName { get; set; } = string.Empty;
}

public class MoveFolderRequest
{
    public string CurrentPath { get; set; } = string.Empty;
    public string NewPath { get; set; } = string.Empty;
}

public class DownloadRequest
{
    public List<string> Paths { get; set; } = new();
}
