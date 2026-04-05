namespace FileManager.Blazor.Models.Responses;

public class UploadResponse
{
    public bool Success { get; set; }
    public List<UploadedFileInfo> UploadedFiles { get; set; } = new();
    public List<FailedFileInfo> FailedFiles { get; set; } = new();
    public int TotalUploaded { get; set; }
}

public class UploadedFileInfo
{
    public string FileName { get; set; } = string.Empty;
    public long Size { get; set; }
    public string Path { get; set; } = string.Empty;
    public bool Success { get; set; }
}

public class FailedFileInfo
{
    public string FileName { get; set; } = string.Empty;
    public string? Error { get; set; }
}
