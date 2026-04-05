using System.IO;
using System.Diagnostics;
using FileManager.Blazor.Models.Config;
using FileManager.Blazor.Models.Domain;
using FileManager.Blazor.Models.Requests;
using FileManager.Blazor.Models.Responses;
using Microsoft.Extensions.Options;

namespace FileManager.Blazor.Services;

public class FileService : IFileService
{
    private readonly FileManagerOptions _options;
    private readonly IConfigService _config;

    public FileService(IOptions<FileManagerOptions> options, IConfigService config)
    {
        _options = options.Value;
        _config = config;
    }

    public Task<FileListResponse> GetFilesAsync(string path, string? filter = null)
    {
        var rootPath = _config.GetRootFolder();
        var targetPath = string.IsNullOrEmpty(path) ? rootPath : path;

        if (!_config.IsPathAllowed(targetPath))
            throw new UnauthorizedAccessException("Path is outside the root folder.");

        if (!Directory.Exists(targetPath))
            throw new DirectoryNotFoundException($"Directory not found: {targetPath}");

        var dirInfo = new DirectoryInfo(targetPath);
        var items = new List<FileItem>();

        // Parent folder
        if (targetPath != rootPath)
        {
            var parentPath = Directory.GetParent(targetPath)?.FullName ?? rootPath;
            items.Add(new FileItem
            {
                Name = "..",
                Path = parentPath,
                IsDirectory = true,
                Size = 0,
                LastModified = DateTime.UtcNow,
                CreatedTime = DateTime.UtcNow
            });
        }

        // Directories
        foreach (var dir in dirInfo.GetDirectories())
        {
            if ((_options.UI.ShowFolders || dir.Name != ".filesmanager") && !dir.Attributes.HasFlag(FileAttributes.Hidden))
            {
                items.Add(new FileItem
                {
                    Name = dir.Name,
                    Path = dir.FullName,
                    IsDirectory = true,
                    Size = 0,
                    Extension = null,
                    LastModified = dir.LastWriteTimeUtc,
                    CreatedTime = dir.CreationTimeUtc
                });
            }
        }

        // Files
        foreach (var file in dirInfo.GetFiles())
        {
            if (file.Attributes.HasFlag(FileAttributes.Hidden)) continue;

            // Apply filter
            if (!string.IsNullOrEmpty(filter) && filter != "*")
            {
                var pattern = filter.Replace(".", "\\.").Replace("*", ".*").Replace("?", ".");
                if (!System.Text.RegularExpressions.Regex.IsMatch(file.Name, pattern, System.Text.RegularExpressions.RegexOptions.IgnoreCase))
                    continue;
            }

            // Check extension allowed
            if (_options.AllowedFileExtensions.Length > 0 && !_options.AllowedFileExtensions.Contains("*"))
            {
                var ext = file.Extension.ToLowerInvariant();
                if (!_options.AllowedFileExtensions.Any(e => e.Equals(ext, StringComparison.OrdinalIgnoreCase)))
                    continue;
            }

            items.Add(new FileItem
            {
                Name = file.Name,
                Path = file.FullName,
                IsDirectory = false,
                Size = file.Length,
                Extension = file.Extension,
                LastModified = file.LastWriteTimeUtc,
                CreatedTime = file.CreationTimeUtc
            });
        }

        var parentDir = Directory.GetParent(targetPath);
        return Task.FromResult(new FileListResponse
        {
            Path = targetPath,
            ParentPath = parentDir?.FullName ?? rootPath,
            Items = items,
            TotalCount = items.Count,
            FilterApplied = filter
        });
    }

    public Task<SearchResponse> SearchFilesAsync(SearchRequest request)
    {
        var sw = Stopwatch.StartNew();

        if (!_config.IsPathAllowed(request.SearchPath))
            throw new UnauthorizedAccessException("Search path is outside the root folder.");

        if (!Directory.Exists(request.SearchPath))
            throw new DirectoryNotFoundException($"Search directory not found: {request.SearchPath}");

        var results = new List<FileItem>();
        var searchOption = SearchOption.AllDirectories;

        var allFiles = Directory.EnumerateFiles(request.SearchPath, "*", searchOption);

        foreach (var filePath in allFiles)
        {
            var fileName = Path.GetFileName(filePath);

            // Keyword filter
            if (!string.IsNullOrEmpty(request.Keyword))
            {
                var comparison = request.CaseSensitive
                    ? StringComparison.Ordinal
                    : StringComparison.OrdinalIgnoreCase;
                if (!fileName.Contains(request.Keyword, comparison))
                    continue;
            }

            // Extension filter
            if (request.FileExtensions != null && request.FileExtensions.Length > 0)
            {
                var ext = Path.GetExtension(filePath).ToLowerInvariant();
                if (!request.FileExtensions.Any(e => e.Equals(ext, StringComparison.OrdinalIgnoreCase)))
                    continue;
            }

            var fileInfo = new FileInfo(filePath);
            results.Add(new FileItem
            {
                Name = fileName,
                Path = filePath,
                IsDirectory = false,
                Size = fileInfo.Length,
                Extension = fileInfo.Extension,
                LastModified = fileInfo.LastWriteTimeUtc,
                CreatedTime = fileInfo.CreationTimeUtc
            });
        }

        sw.Stop();
        sw.Stop();
        return Task.FromResult(new SearchResponse
        {
            Results = results,
            TotalCount = results.Count,
            SearchTimeMs = sw.ElapsedMilliseconds
        });
    }

    public Task<FileOperationResult> RenameFileAsync(string oldPath, string newName)
    {
        if (!_config.IsPathAllowed(oldPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_TRAVERSAL_DETECTED",
                Message = "Path is outside the root folder."
            });

        if (!_config.HasPermission(PermissionKeys.AllowRename))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PERMISSION_DENIED",
                Message = "Rename permission is disabled."
            });

        if (!File.Exists(oldPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_NOT_FOUND",
                Message = "File not found."
            });

        var directory = Path.GetDirectoryName(oldPath) ?? _config.GetRootFolder();
        var newPath = Path.Combine(directory, newName);

        if (!_config.IsPathAllowed(newPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_TRAVERSAL_DETECTED",
                Message = "New path is outside the root folder."
            });

        if (File.Exists(newPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "FILE_EXISTS",
                Message = "A file with this name already exists."
            });

        try
        {
            File.Move(oldPath, newPath);
            return Task.FromResult(new FileOperationResult
            {
                Success = true,
                SourcePath = oldPath,
                DestinationPath = newPath,
                Path = oldPath,
                NewPath = newPath,
                Message = "File renamed successfully."
            });
        }
        catch (Exception ex)
        {
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "SYSTEM_ERROR",
                Message = ex.Message
            });
        }
    }

    public Task<MoveResponse> MoveFileAsync(List<string> sourcePaths, string destPath)
    {
        var response = new MoveResponse { Success = true, Results = new List<MoveResultItem>() };

        if (!_config.IsPathAllowed(destPath))
        {
            response.Success = false;
            return Task.FromResult(response);
        }

        if (!_config.HasPermission(PermissionKeys.AllowMove))
        {
            response.Success = false;
            return Task.FromResult(response);
        }

        if (!Directory.Exists(destPath))
        {
            response.Success = false;
            return Task.FromResult(response);
        }

        foreach (var sourcePath in sourcePaths)
        {
            if (!_config.IsPathAllowed(sourcePath))
            {
                response.Results.Add(new MoveResultItem
                {
                    Path = sourcePath,
                    NewPath = "",
                    Success = false,
                    Error = "Path traversal detected"
                });
                response.Success = false;
                continue;
            }

            if (!File.Exists(sourcePath))
            {
                response.Results.Add(new MoveResultItem
                {
                    Path = sourcePath,
                    NewPath = "",
                    Success = false,
                    Error = "File not found"
                });
                response.Success = false;
                continue;
            }

            var fileName = Path.GetFileName(sourcePath);
            var newPath = Path.Combine(destPath, fileName);

            if (!_config.IsPathAllowed(newPath))
            {
                response.Results.Add(new MoveResultItem
                {
                    Path = sourcePath,
                    NewPath = "",
                    Success = false,
                    Error = "Destination path outside root"
                });
                response.Success = false;
                continue;
            }

            try
            {
                File.Move(sourcePath, newPath, overwrite: false);
                response.Results.Add(new MoveResultItem
                {
                    Path = sourcePath,
                    NewPath = newPath,
                    Success = true
                });
            }
            catch (Exception ex)
            {
                response.Results.Add(new MoveResultItem
                {
                    Path = sourcePath,
                    NewPath = "",
                    Success = false,
                    Error = ex.Message
                });
                response.Success = false;
            }
        }

        response.MovedCount = response.Results.Count(r => r.Success);
        return Task.FromResult(response);
    }

    public Task<FileOperationResult> DeleteFileAsync(string path)
    {
        if (!_config.IsPathAllowed(path))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_TRAVERSAL_DETECTED",
                Message = "Path is outside the root folder."
            });

        if (!_config.HasPermission(PermissionKeys.AllowDelete))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PERMISSION_DENIED",
                Message = "Delete permission is disabled."
            });

        if (!File.Exists(path))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_NOT_FOUND",
                Message = "File not found."
            });

        try
        {
            File.Delete(path);
            return Task.FromResult(new FileOperationResult
            {
                Success = true,
                Path = path,
                Message = "File deleted successfully."
            });
        }
        catch (Exception ex)
        {
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "SYSTEM_ERROR",
                Message = ex.Message
            });
        }
    }

    public Task<(Stream? stream, string? fileName, string? contentType)> DownloadFileAsync(string path)
    {
        if (!_config.IsPathAllowed(path))
            return Task.FromResult<(Stream?, string?, string?)>((null, null, "Path is outside the root folder."));

        if (!_config.HasPermission(PermissionKeys.AllowDownload))
            return Task.FromResult<(Stream?, string?, string?)>((null, null, "Download permission is disabled."));

        if (!File.Exists(path))
            return Task.FromResult<(Stream?, string?, string?)>((null, null, "File not found."));

        var fileName = Path.GetFileName(path);
        var contentType = GetContentType(fileName);
        var stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read);

        return Task.FromResult<(Stream?, string?, string?)>((stream, fileName, contentType));
    }

    private static string GetContentType(string fileName)
    {
        var ext = Path.GetExtension(fileName).ToLowerInvariant();
        return ext switch
        {
            ".pdf" => "application/pdf",
            ".png" => "image/png",
            ".jpg" or ".jpeg" => "image/jpeg",
            ".gif" => "image/gif",
            ".txt" => "text/plain",
            ".html" => "text/html",
            ".css" => "text/css",
            ".js" => "application/javascript",
            ".json" => "application/json",
            ".xml" => "application/xml",
            ".zip" => "application/zip",
            ".doc" => "application/msword",
            ".docx" => "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".xls" => "application/vnd.ms-excel",
            ".xlsx" => "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".csv" => "text/csv",
            _ => "application/octet-stream"
        };
    }
}
