namespace FileManager.Blazor.Models.Responses;

public class MoveResponse
{
    public bool Success { get; set; }
    public int MovedCount { get; set; }
    public List<MoveResultItem> Results { get; set; } = new();
}

public class MoveResultItem
{
    public string Path { get; set; } = string.Empty;
    public string NewPath { get; set; } = string.Empty;
    public bool Success { get; set; }
    public string? Error { get; set; }
}
