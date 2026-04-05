using FileManager.Blazor.Models.Domain;
using FileManager.Blazor.Models.Requests;
using FileManager.Blazor.Models.Responses;

namespace FileManager.Blazor.Services;

public class FileManagerApi
{
    private readonly HttpClient _httpClient;

    public FileManagerApi(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    // GET /api/files?path={path}
    public async Task<FileListResponse?> GetFilesAsync(string path)
    {
        var response = await _httpClient.GetAsync($"/api/files?path={Uri.EscapeDataString(path)}");
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<FileListResponse>();
    }

    // GET /api/files/tree?rootPath={rootPath}
    public async Task<FolderTreeResponse?> GetFolderTreeAsync(string rootPath)
    {
        var response = await _httpClient.GetAsync($"/api/files/tree?rootPath={Uri.EscapeDataString(rootPath)}");
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<FolderTreeResponse>();
    }

    // POST /api/folders
    public async Task<ApiResponse<string>?> CreateFolderAsync(CreateFolderRequest request)
    {
        var response = await _httpClient.PostAsJsonAsync("/api/folders", request);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<ApiResponse<string>>();
    }

    // PATCH /api/files/rename
    public async Task<ApiResponse<string>?> RenameFileAsync(RenameRequest request)
    {
        var response = await _httpClient.PatchAsJsonAsync("/api/files/rename", request);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<ApiResponse<string>>();
    }

    // DELETE /api/files?path={path}
    public async Task<ApiResponse<string>?> DeleteFileAsync(string path)
    {
        var response = await _httpClient.DeleteAsync($"/api/files?path={Uri.EscapeDataString(path)}");
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<ApiResponse<string>>();
    }
}