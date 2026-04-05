using System.IO;
using FileManager.Blazor.Models.Config;
using FileManager.Blazor.Models.Domain;
using FileManager.Blazor.Models.Responses;
using Microsoft.Extensions.Options;

namespace FileManager.Blazor.Services;

public class FolderService : IFolderService
{
    private readonly FileManagerOptions _options;
    private readonly IConfigService _config;

    public FolderService(IOptions<FileManagerOptions> options, IConfigService config)
    {
        _options = options.Value;
        _config = config;
    }

    public Task<FileOperationResult> CreateFolderAsync(string parentPath, string folderName)
    {
        if (!_config.IsPathAllowed(parentPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_TRAVERSAL_DETECTED",
                Message = "Path is outside the root folder."
            });

        if (!_config.HasPermission(PermissionKeys.AllowCreate))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PERMISSION_DENIED",
                Message = "Create permission is disabled."
            });

        if (!Directory.Exists(parentPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_NOT_FOUND",
                Message = "Parent directory not found."
            });

        var newPath = Path.Combine(parentPath, folderName);

        if (!_config.IsPathAllowed(newPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_TRAVERSAL_DETECTED",
                Message = "New path is outside the root folder."
            });

        if (Directory.Exists(newPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "FOLDER_EXISTS",
                Message = "A folder with this name already exists."
            });

        try
        {
            Directory.CreateDirectory(newPath);
            return Task.FromResult(new FileOperationResult
            {
                Success = true,
                Path = newPath,
                Message = "Folder created successfully."
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

    public Task<FolderTreeResponse> GetFolderTreeAsync(string rootPath)
    {
        if (!_config.IsPathAllowed(rootPath))
            throw new UnauthorizedAccessException("Path is outside the root folder.");

        var rootDir = string.IsNullOrEmpty(rootPath) ? _config.GetRootFolder() : rootPath;

        if (!Directory.Exists(rootDir))
            throw new DirectoryNotFoundException($"Directory not found: {rootDir}");

        var response = new FolderTreeResponse
        {
            RootPath = rootDir,
            Nodes = new List<FolderTreeNode>()
        };

        BuildFolderTree(rootDir, response.Nodes, 0);

        return Task.FromResult(response);
    }

    private void BuildFolderTree(string path, List<FolderTreeNode> nodes, int level)
    {
        try
        {
            var dirInfo = new DirectoryInfo(path);
            if (dirInfo.Attributes.HasFlag(FileAttributes.Hidden)) return;

            foreach (var dir in dirInfo.GetDirectories())
            {
                if (dir.Attributes.HasFlag(FileAttributes.Hidden)) continue;
                if (dir.Name == ".filesmanager") continue;

                var hasChildren = HasSubDirectories(dir.FullName);
                var node = new FolderTreeNode
                {
                    Path = dir.FullName,
                    Name = dir.Name,
                    HasChildren = hasChildren,
                    Expanded = false,
                    Level = level + 1,
                    Children = new List<FolderTreeNode>()
                };
                nodes.Add(node);

                if (hasChildren)
                {
                    BuildFolderTree(dir.FullName, node.Children, level + 1);
                }
            }
        }
        catch (UnauthorizedAccessException) { }
        catch (DirectoryNotFoundException) { }
    }

    private static bool HasSubDirectories(string path)
    {
        try
        {
            var dirInfo = new DirectoryInfo(path);
            return dirInfo.GetDirectories().Any(d =>
                !d.Attributes.HasFlag(FileAttributes.Hidden) && d.Name != ".filesmanager");
        }
        catch
        {
            return false;
        }
    }

    public Task<FileOperationResult> DeleteFolderAsync(string path)
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

        if (!Directory.Exists(path))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_NOT_FOUND",
                Message = "Folder not found."
            });

        var rootPath = _config.GetRootFolder();
        if (Path.GetFullPath(path) == Path.GetFullPath(rootPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "CANNOT_DELETE_ROOT",
                Message = "Cannot delete the root folder."
            });

        try
        {
            Directory.Delete(path, recursive: true);
            return Task.FromResult(new FileOperationResult
            {
                Success = true,
                Path = path,
                Message = "Folder deleted successfully."
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

    public Task<FileOperationResult> MoveFolderAsync(string sourcePath, string destPath)
    {
        if (!_config.IsPathAllowed(sourcePath) || !_config.IsPathAllowed(destPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_TRAVERSAL_DETECTED",
                Message = "Path is outside the root folder."
            });

        if (!_config.HasPermission(PermissionKeys.AllowMove))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PERMISSION_DENIED",
                Message = "Move permission is disabled."
            });

        if (!Directory.Exists(sourcePath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_NOT_FOUND",
                Message = "Source folder not found."
            });

        if (!Directory.Exists(destPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_NOT_FOUND",
                Message = "Destination folder not found."
            });

        var rootPath = _config.GetRootFolder();
        if (Path.GetFullPath(sourcePath) == Path.GetFullPath(rootPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "CANNOT_MOVE_ROOT",
                Message = "Cannot move the root folder."
            });

        var folderName = Path.GetFileName(sourcePath);
        var newPath = Path.Combine(destPath, folderName);

        if (!_config.IsPathAllowed(newPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "PATH_TRAVERSAL_DETECTED",
                Message = "New path is outside the root folder."
            });

        if (Directory.Exists(newPath))
            return Task.FromResult(new FileOperationResult
            {
                Success = false,
                ErrorCode = "FOLDER_EXISTS",
                Message = "A folder with this name already exists at the destination."
            });

        try
        {
            Directory.Move(sourcePath, newPath);
            return Task.FromResult(new FileOperationResult
            {
                Success = true,
                SourcePath = sourcePath,
                DestinationPath = newPath,
                Path = sourcePath,
                NewPath = newPath,
                Message = "Folder moved successfully."
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
}
