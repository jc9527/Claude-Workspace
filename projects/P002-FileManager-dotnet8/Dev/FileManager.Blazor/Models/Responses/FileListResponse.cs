using FileManager.Blazor.Models.Domain;

namespace FileManager.Blazor.Models.Responses;

public class FileListResponse
{
    public string Path { get; set; } = string.Empty;
    public string ParentPath { get; set; } = string.Empty;
    public List<FileItem> Items { get; set; } = new();
    public int TotalCount { get; set; }
    public string? FilterApplied { get; set; }
}
