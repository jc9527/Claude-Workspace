using FileManager.Blazor.Models.Domain;
using FileManager.Blazor.Models.Requests;
using FileManager.Blazor.Models.Responses;
using FileManager.Blazor.Services;
using Microsoft.AspNetCore.Mvc;

namespace FileManager.Blazor.Controllers;

[ApiController]
[Route("api/folders")]
public class FoldersController : ControllerBase
{
    private readonly IFolderService _folderService;
    private readonly IConfigService _config;

    public FoldersController(IFolderService folderService, IConfigService config)
    {
        _folderService = folderService;
        _config = config;
    }

    [HttpPost]
    public async Task<ActionResult<ApiResponse<FileOperationResult>>> CreateFolder([FromBody] CreateFolderRequest request)
    {
        try
        {
            var rootPath = _config.GetRootFolder();
            var parentPath = string.IsNullOrEmpty(request.ParentPath) ? rootPath : request.ParentPath;

            var result = await _folderService.CreateFolderAsync(parentPath, request.FolderName);
            if (!result.Success)
            {
                var statusCode = result.ErrorCode switch
                {
                    "PATH_NOT_FOUND" => 404,
                    "PATH_TRAVERSAL_DETECTED" => 403,
                    "PERMISSION_DENIED" => 403,
                    _ => 400
                };
                return StatusCode(statusCode, ApiResponse<FileOperationResult>.Fail(result.Message!, result.ErrorCode));
            }
            return Ok(ApiResponse<FileOperationResult>.Ok(result, result.Message));
        }
        catch (Exception ex)
        {
            return StatusCode(500, ApiResponse<FileOperationResult>.Fail(ex.Message, "SYSTEM_ERROR"));
        }
    }

    [HttpGet("tree")]
    public async Task<ActionResult<ApiResponse<FolderTreeResponse>>> GetFolderTree([FromQuery] string? rootPath)
    {
        try
        {
            var root = string.IsNullOrEmpty(rootPath) ? _config.GetRootFolder() : rootPath;
            var result = await _folderService.GetFolderTreeAsync(root);
            return Ok(ApiResponse<FolderTreeResponse>.Ok(result));
        }
        catch (UnauthorizedAccessException ex)
        {
            return StatusCode(403, ApiResponse<FolderTreeResponse>.Fail(ex.Message, "ACCESS_DENIED"));
        }
        catch (DirectoryNotFoundException ex)
        {
            return NotFound(ApiResponse<FolderTreeResponse>.Fail(ex.Message, "PATH_NOT_FOUND"));
        }
        catch (Exception ex)
        {
            return StatusCode(500, ApiResponse<FolderTreeResponse>.Fail(ex.Message, "SYSTEM_ERROR"));
        }
    }

    [HttpPatch("rename")]
    public async Task<ActionResult<ApiResponse<FileOperationResult>>> RenameFolder([FromBody] RenameRequest request)
    {
        try
        {
            var directory = System.IO.Path.GetDirectoryName(request.CurrentPath) ?? _config.GetRootFolder();
            var result = await _folderService.MoveFolderAsync(request.CurrentPath, directory);
            if (!result.Success)
            {
                var statusCode = result.ErrorCode switch
                {
                    "PATH_NOT_FOUND" => 404,
                    "PATH_TRAVERSAL_DETECTED" => 403,
                    "PERMISSION_DENIED" => 403,
                    _ => 400
                };
                return StatusCode(statusCode, ApiResponse<FileOperationResult>.Fail(result.Message!, result.ErrorCode));
            }
            return Ok(ApiResponse<FileOperationResult>.Ok(result));
        }
        catch (Exception ex)
        {
            return StatusCode(500, ApiResponse<FileOperationResult>.Fail(ex.Message, "SYSTEM_ERROR"));
        }
    }

    [HttpPatch("move")]
    public async Task<ActionResult<ApiResponse<FileOperationResult>>> MoveFolder([FromBody] MoveFolderRequest request)
    {
        try
        {
            var destDir = System.IO.Path.GetDirectoryName(request.NewPath) ?? _config.GetRootFolder();
            var folderName = System.IO.Path.GetFileName(request.NewPath);
            var tempPath = System.IO.Path.Combine(destDir, folderName);

            var result = await _folderService.MoveFolderAsync(request.CurrentPath, destDir);
            if (!result.Success)
            {
                var statusCode = result.ErrorCode switch
                {
                    "PATH_NOT_FOUND" => 404,
                    "PATH_TRAVERSAL_DETECTED" => 403,
                    "PERMISSION_DENIED" => 403,
                    _ => 400
                };
                return StatusCode(statusCode, ApiResponse<FileOperationResult>.Fail(result.Message!, result.ErrorCode));
            }
            return Ok(ApiResponse<FileOperationResult>.Ok(result));
        }
        catch (Exception ex)
        {
            return StatusCode(500, ApiResponse<FileOperationResult>.Fail(ex.Message, "SYSTEM_ERROR"));
        }
    }

    [HttpDelete]
    public async Task<ActionResult<ApiResponse>> DeleteFolder([FromQuery] string path)
    {
        try
        {
            var result = await _folderService.DeleteFolderAsync(path);
            if (!result.Success)
            {
                var statusCode = result.ErrorCode switch
                {
                    "PATH_NOT_FOUND" => 404,
                    "PATH_TRAVERSAL_DETECTED" => 403,
                    "PERMISSION_DENIED" => 403,
                    _ => 400
                };
                return StatusCode(statusCode, ApiResponse.Fail(result.Message!, result.ErrorCode));
            }
            return Ok(ApiResponse.Ok(result.Message));
        }
        catch (Exception ex)
        {
            return StatusCode(500, ApiResponse.Fail(ex.Message, "SYSTEM_ERROR"));
        }
    }
}
