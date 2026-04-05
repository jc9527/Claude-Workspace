using FileManager.Blazor.Models.Domain;
using FileManager.Blazor.Models.Requests;
using FileManager.Blazor.Models.Responses;

namespace FileManager.Blazor.Services;

public interface IFileService
{
    Task<FileListResponse> GetFilesAsync(string path, string? filter = null);
    Task<SearchResponse> SearchFilesAsync(SearchRequest request);
    Task<FileOperationResult> RenameFileAsync(string oldPath, string newName);
    Task<MoveResponse> MoveFileAsync(List<string> sourcePaths, string destPath);
    Task<FileOperationResult> DeleteFileAsync(string path);
    Task<(Stream? stream, string? fileName, string? contentType)> DownloadFileAsync(string path);
}
