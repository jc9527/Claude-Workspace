namespace FileManager.Blazor.Models.Domain;

public class FileItem
{
    public string Name { get; set; } = string.Empty;
    public string Path { get; set; } = string.Empty;
    public bool IsDirectory { get; set; }
    public long Size { get; set; }
    public string? Extension { get; set; }
    public DateTime LastModified { get; set; }
    public DateTime CreatedTime { get; set; }
    public bool CanRead { get; set; } = true;
    public bool CanWrite { get; set; } = true;
}
