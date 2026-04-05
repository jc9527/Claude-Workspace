using System.IO;
using FileManager.Blazor.Models.Config;
using FileManager.Blazor.Models.Responses;
using FileManager.Blazor.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;

namespace FileManager.Blazor.Controllers;

[ApiController]
[Route("api/upload")]
public class UploadController : ControllerBase
{
    private readonly IConfigService _config;
    private readonly FileManagerOptions _options;

    public UploadController(IConfigService config, IOptions<FileManagerOptions> options)
    {
        _config = config;
        _options = options.Value;
    }

    [HttpPost]
    public async Task<ActionResult<ApiResponse<UploadResponse>>> Upload(
        [FromForm] IFormFileCollection files,
        [FromForm] string destinationPath,
        [FromForm] bool overwrite = false)
    {
        var response = new UploadResponse
        {
            Success = true,
            UploadedFiles = new List<UploadedFileInfo>(),
            FailedFiles = new List<FailedFileInfo>()
        };

        if (!_config.HasPermission(PermissionKeys.EnabledUpload))
        {
            return StatusCode(403, ApiResponse<UploadResponse>.Fail("Upload is disabled.", "PERMISSION_DENIED"));
        }

        var rootPath = _config.GetRootFolder();
        var destPath = string.IsNullOrEmpty(destinationPath) ? rootPath : destinationPath;

        if (!_config.IsPathAllowed(destPath))
        {
            return StatusCode(403, ApiResponse<UploadResponse>.Fail("Destination path is outside the root folder.", "PATH_TRAVERSAL_DETECTED"));
        }

        if (!Directory.Exists(destPath))
        {
            return NotFound(ApiResponse<UploadResponse>.Fail("Destination folder not found.", "PATH_NOT_FOUND"));
        }

        var maxFiles = _config.HasPermission(PermissionKeys.EnableUploadMultiSelect) ? int.MaxValue : 1;
        var fileArray = files.Take(maxFiles).ToList();

        foreach (var file in fileArray)
        {
            try
            {
                var fileName = Path.GetFileName(file.FileName);
                var ext = Path.GetExtension(fileName).ToLowerInvariant();

                // Check allowed extensions
                if (_options.AllowedFileExtensions.Length > 0 && !_options.AllowedFileExtensions.Contains("*"))
                {
                    if (!_options.AllowedFileExtensions.Any(e => e.Equals(ext, StringComparison.OrdinalIgnoreCase)))
                    {
                        response.FailedFiles.Add(new FailedFileInfo
                        {
                            FileName = fileName,
                            Error = $"File extension {ext} is not allowed."
                        });
                        continue;
                    }
                }

                var destFilePath = Path.Combine(destPath, fileName);

                if (System.IO.File.Exists(destFilePath) && !overwrite)
                {
                    response.FailedFiles.Add(new FailedFileInfo
                    {
                        FileName = fileName,
                        Error = "File already exists. Set overwrite=true to replace."
                    });
                    continue;
                }

                using var stream = new FileStream(destFilePath, FileMode.Create, FileAccess.Write);
                await file.CopyToAsync(stream);

                response.UploadedFiles.Add(new UploadedFileInfo
                {
                    FileName = fileName,
                    Size = file.Length,
                    Path = destFilePath,
                    Success = true
                });
            }
            catch (Exception ex)
            {
                response.FailedFiles.Add(new FailedFileInfo
                {
                    FileName = file.FileName,
                    Error = ex.Message
                });
            }
        }

        response.TotalUploaded = response.UploadedFiles.Count;
        response.Success = response.FailedFiles.Count == 0;

        if (response.TotalUploaded == 0 && response.FailedFiles.Count > 0)
        {
            return BadRequest(ApiResponse<UploadResponse>.Fail("All uploads failed.", "UPLOAD_FAILED"));
        }

        return Ok(ApiResponse<UploadResponse>.Ok(response));
    }
}
