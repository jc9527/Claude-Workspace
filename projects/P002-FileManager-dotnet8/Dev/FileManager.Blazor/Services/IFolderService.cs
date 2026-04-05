using FileManager.Blazor.Models.Domain;
using FileManager.Blazor.Models.Responses;

namespace FileManager.Blazor.Services;

public interface IFolderService
{
    Task<FileOperationResult> CreateFolderAsync(string parentPath, string folderName);
    Task<FolderTreeResponse> GetFolderTreeAsync(string rootPath);
    Task<FileOperationResult> DeleteFolderAsync(string path);
    Task<FileOperationResult> MoveFolderAsync(string sourcePath, string destPath);
}
