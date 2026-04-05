using Microsoft.AspNetCore.Mvc;

namespace FileManager.Blazor.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly Services.IServerAuthService _authService;

    public AuthController(Services.IServerAuthService authService)
    {
        _authService = authService;
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginRequest request)
    {
        if (string.IsNullOrEmpty(request.Email) || string.IsNullOrEmpty(request.Password))
        {
            return BadRequest(new { error = "請輸入 Email 和密碼" });
        }

        var isValid = await _authService.ValidateCredentialsAsync(request.Email, request.Password);
        if (!isValid)
        {
            return Unauthorized(new { error = "Email 或密碼錯誤" });
        }

        var isAdmin = await _authService.IsAdminAsync(request.Email);
        await _authService.SignInAsync(HttpContext, request.Email, isAdmin);
        await _authService.CreateUserFolderAsync(request.Email);

        return Ok(new { email = request.Email, isAdmin });
    }

    [HttpPost("logout")]
    public async Task<IActionResult> Logout()
    {
        await _authService.SignOutAsync(HttpContext);
        return Ok();
    }

    [HttpGet("session")]
    public async Task<IActionResult> GetSession()
    {
        var (email, isAdmin) = await _authService.GetSessionAsync(HttpContext);
        if (string.IsNullOrEmpty(email))
        {
            return Ok(new { isAuthenticated = false });
        }
        return Ok(new { isAuthenticated = true, email, isAdmin });
    }
}

public class LoginRequest
{
    public string Email { get; set; } = "";
    public string Password { get; set; } = "";
}