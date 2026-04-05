using FileManager.Blazor.Models.Domain;

namespace FileManager.Blazor.Models.Responses;

public class SearchResponse
{
    public List<FileItem> Results { get; set; } = new();
    public int TotalCount { get; set; }
    public long SearchTimeMs { get; set; }
}
