using System.IO;
using FileManager.Blazor.Models.Domain;
using FileManager.Blazor.Models.Requests;
using FileManager.Blazor.Models.Responses;
using FileManager.Blazor.Services;
using Microsoft.AspNetCore.Mvc;

namespace FileManager.Blazor.Controllers;

[ApiController]
[Route("api/files")]
public class FilesController : ControllerBase
{
    private readonly IFileService _fileService;
    private readonly IConfigService _config;

    public FilesController(IFileService fileService, IConfigService config)
    {
        _fileService = fileService;
        _config = config;
    }

    [HttpGet]
    public async Task<ActionResult<ApiResponse<FileListResponse>>> GetFiles(
        [FromQuery] string? path,
        [FromQuery] string? filter)
    {
        try
        {
            var rootPath = _config.GetRootFolder();
            var targetPath = string.IsNullOrEmpty(path) ? rootPath : path;
            var result = await _fileService.GetFilesAsync(targetPath, filter);
            return Ok(ApiResponse<FileListResponse>.Ok(result));
        }
        catch (UnauthorizedAccessException ex)
        {
            return StatusCode(403, ApiResponse<FileListResponse>.Fail(ex.Message, "ACCESS_DENIED"));
        }
        catch (DirectoryNotFoundException ex)
        {
            return NotFound(ApiResponse<FileListResponse>.Fail(ex.Message, "PATH_NOT_FOUND"));
        }
        catch (Exception ex)
        {
            return StatusCode(500, ApiResponse<FileListResponse>.Fail(ex.Message, "SYSTEM_ERROR"));
        }
    }

    [HttpPost("search")]
    public async Task<ActionResult<ApiResponse<SearchResponse>>> SearchFiles([FromBody] SearchRequest request)
    {
        try
        {
            if (string.IsNullOrEmpty(request.SearchPath))
                request.SearchPath = _config.GetRootFolder();

            var result = await _fileService.SearchFilesAsync(request);
            return Ok(ApiResponse<SearchResponse>.Ok(result));
        }
        catch (UnauthorizedAccessException ex)
        {
            return StatusCode(403, ApiResponse<SearchResponse>.Fail(ex.Message, "ACCESS_DENIED"));
        }
        catch (DirectoryNotFoundException ex)
        {
            return NotFound(ApiResponse<SearchResponse>.Fail(ex.Message, "PATH_NOT_FOUND"));
        }
        catch (Exception ex)
        {
            return StatusCode(500, ApiResponse<SearchResponse>.Fail(ex.Message, "SYSTEM_ERROR"));
        }
    }

    [HttpPatch("rename")]
    public async Task<ActionResult<ApiResponse<FileOperationResult>>> RenameFile([FromBody] RenameRequest request)
    {
        try
        {
            var result = await _fileService.RenameFileAsync(request.CurrentPath, request.NewName);
            if (!result.Success)
            {
                var statusCode = result.ErrorCode switch
                {
                    "PATH_NOT_FOUND" => 404,
                    "PATH_TRAVERSAL_DETECTED" => 403,
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
    public async Task<ActionResult<ApiResponse<MoveResponse>>> MoveFile([FromBody] MoveRequest request)
    {
        try
        {
            var result = await _fileService.MoveFileAsync(request.SourcePaths, request.DestinationPath);
            if (!result.Success)
            {
                return BadRequest(ApiResponse<MoveResponse>.Fail("Some files could not be moved.", "PARTIAL_FAILURE"));
            }
            return Ok(ApiResponse<MoveResponse>.Ok(result));
        }
        catch (Exception ex)
        {
            return StatusCode(500, ApiResponse<MoveResponse>.Fail(ex.Message, "SYSTEM_ERROR"));
        }
    }

    [HttpDelete]
    public async Task<ActionResult<ApiResponse>> DeleteFile([FromQuery] string path)
    {
        try
        {
            var result = await _fileService.DeleteFileAsync(path);
            if (!result.Success)
            {
                var statusCode = result.ErrorCode switch
                {
                    "PATH_NOT_FOUND" => 404,
                    "PATH_TRAVERSAL_DETECTED" => 403,
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

    [HttpGet("download/{**path}")]
    public async Task<IActionResult> DownloadFile(string path)
    {
        try
        {
            var (stream, fileName, error) = await _fileService.DownloadFileAsync(path);
            if (stream == null)
            {
                if (error == "File not found.") return NotFound(error);
                if (error == "Path is outside the root folder.") return Forbid();
                return BadRequest(error ?? "Download failed");
            }

            return File(stream, "application/octet-stream", fileName!);
        }
        catch (Exception ex)
        {
            return StatusCode(500, ex.Message);
        }
    }

    [HttpPost("download")]
    public async Task<IActionResult> DownloadMultiple([FromBody] DownloadRequest request)
    {
        try
        {
            if (request.Paths.Count == 0)
                return BadRequest("No files specified.");

            if (request.Paths.Count == 1)
            {
                var (stream, fileName, error) = await _fileService.DownloadFileAsync(request.Paths[0]);
                if (stream == null) return NotFound(error ?? "File not found");
                return File(stream, "application/octet-stream", fileName!);
            }

            // Multiple files - return ZIP
            var memoryStream = new MemoryStream();
            using (var archive = new System.IO.Compression.ZipArchive(memoryStream, System.IO.Compression.ZipArchiveMode.Create, true))
            {
                foreach (var filePath in request.Paths)
                {
                    if (!_config.IsPathAllowed(filePath) || !System.IO.File.Exists(filePath)) continue;

                    var fileName = Path.GetFileName(filePath);
                    var entry = archive.CreateEntry(fileName, System.IO.Compression.CompressionLevel.Fastest);
                    using var entryStream = entry.Open();
                    using var fileStream = System.IO.File.OpenRead(filePath);
                    await fileStream.CopyToAsync(entryStream);
                }
            }

            memoryStream.Position = 0;
            return File(memoryStream, "application/zip", "files.zip");
        }
        catch (Exception ex)
        {
            return StatusCode(500, ex.Message);
        }
    }
}
