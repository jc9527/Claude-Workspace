using FileManager.Blazor.Models.Config;
using FileManager.Blazor.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;

namespace FileManager.Blazor.Controllers;

[ApiController]
[Route("api/settings")]
public class SettingsController : ControllerBase
{
    private readonly IConfigService _config;
    private readonly FileManagerOptions _options;

    public SettingsController(IConfigService config, IOptions<FileManagerOptions> options)
    {
        _config = config;
        _options = options.Value;
    }

    [HttpGet]
    public ActionResult<FileManagerOptions> GetAllSettings()
    {
        return Ok(_options);
    }

    [HttpGet("permissions")]
    public ActionResult<PermissionOptions> GetPermissions()
    {
        return Ok(_options.Permissions);
    }

    [HttpGet("ui")]
    public ActionResult<UiOptions> GetUiSettings()
    {
        return Ok(_options.UI);
    }

    [HttpGet("limits")]
    public ActionResult<object> GetLimits()
    {
        return Ok(new
        {
            _options.MaxRequestLength,
            _options.AllowedFileExtensions
        });
    }

    [HttpGet("root")]
    public ActionResult<object> GetRootFolder()
    {
        return Ok(new { rootFolder = _config.GetRootFolder() });
    }
}
