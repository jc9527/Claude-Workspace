namespace FileManager.Blazor.Models.Domain;

public class FileOperationResult
{
    public bool Success { get; set; }
    public string? Message { get; set; }
    public string? ErrorCode { get; set; }
    public string? SourcePath { get; set; }
    public string? DestinationPath { get; set; }
    public string? Path { get; set; }
    public string? NewPath { get; set; }
}
