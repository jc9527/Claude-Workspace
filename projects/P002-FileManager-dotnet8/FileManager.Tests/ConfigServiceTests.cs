using FileManager.Blazor.Models.Config;
using FileManager.Blazor.Services;
using FluentAssertions;
using Microsoft.Extensions.Options;
using Moq;

namespace FileManager.Tests;

public class ConfigServiceTests
{
    private static FileManagerOptions DefaultOptions() => new()
    {
        RootFolder = "/app/data",
        AllowedFileExtensions = ["*"],
        MaxRequestLength = 4096,
        Permissions = new PermissionOptions
        {
            AllowDownload = true,
            AllowCreate = true,
            AllowRename = true,
            AllowMove = true,
            AllowDelete = true,
            EnabledUpload = true,
            EnableUploadMultiSelect = true,
            EnableDownloadMultiSelect = true
        },
        UI = new UiOptions { ShowFolders = true }
    };

    private static ConfigService CreateService(FileManagerOptions? options = null)
    {
        var opts = Options.Create(options ?? DefaultOptions());
        return new ConfigService(opts);
    }

    [Fact]
    public void GetRootFolder_ReturnsRootFolder()
    {
        var service = CreateService();
        service.GetRootFolder().Should().Be("/app/data");
    }

    [Fact]
    public void GetRootFolder_CustomRoot_ReturnsCustomRoot()
    {
        var options = DefaultOptions();
        options.RootFolder = "/custom/root";
        var service = CreateService(options);
        service.GetRootFolder().Should().Be("/custom/root");
    }

    [Theory]
    [InlineData("AllowDownload", true)]
    [InlineData("AllowCreate", true)]
    [InlineData("AllowRename", true)]
    [InlineData("AllowMove", true)]
    [InlineData("AllowDelete", true)]
    [InlineData("EnabledUpload", true)]
    [InlineData("EnableUploadMultiSelect", true)]
    [InlineData("EnableDownloadMultiSelect", true)]
    public void HasPermission_AllowedPermissions_ReturnsTrue(string permission, bool expected)
    {
        var service = CreateService();
        service.HasPermission(permission).Should().Be(expected);
    }

    [Fact]
    public void HasPermission_DisabledPermission_ReturnsFalse()
    {
        var options = DefaultOptions();
        options.Permissions.AllowDownload = false;
        var service = CreateService(options);
        service.HasPermission("AllowDownload").Should().BeFalse();
    }

    [Theory]
    [InlineData("UnknownPermission")]
    [InlineData("")]
    [InlineData("RandomKey")]
    public void HasPermission_UnknownPermission_ReturnsFalse(string permission)
    {
        var service = CreateService();
        service.HasPermission(permission).Should().BeFalse();
    }

    [Fact]
    public void IsPathAllowed_NullPath_ReturnsFalse()
    {
        var service = CreateService();
        service.IsPathAllowed(null!).Should().BeFalse();
    }

    [Fact]
    public void IsPathAllowed_EmptyPath_ReturnsFalse()
    {
        var service = CreateService();
        service.IsPathAllowed("").Should().BeFalse();
    }

    [Fact]
    public void IsPathAllowed_RootFolder_ReturnsTrue()
    {
        var service = CreateService();
        service.IsPathAllowed("/app/data").Should().BeTrue();
    }

    [Fact]
    public void IsPathAllowed_Subfolder_ReturnsTrue()
    {
        var service = CreateService();
        service.IsPathAllowed("/app/data/subfolder").Should().BeTrue();
    }

    [Fact]
    public void IsPathAllowed_NestedSubfolder_ReturnsTrue()
    {
        var service = CreateService();
        service.IsPathAllowed("/app/data/subfolder/nested").Should().BeTrue();
    }

    [Fact]
    public void IsPathAllowed_ParentOutsideRoot_ReturnsFalse()
    {
        var service = CreateService();
        service.IsPathAllowed("/app").Should().BeFalse();
    }

    [Fact]
    public void IsPathAllowed_CompletelyOutsideRoot_ReturnsFalse()
    {
        var service = CreateService();
        service.IsPathAllowed("/etc/passwd").Should().BeFalse();
    }

    [Fact]
    public void IsPathAllowed_PathTraversalAttempt_ReturnsFalse()
    {
        var service = CreateService();
        service.IsPathAllowed("/app/data/../../../etc/passwd").Should().BeFalse();
    }

    [Fact]
    public void IsPathAllowed_WindowsStyleTraversal_ReturnsFalse()
    {
        var options = DefaultOptions();
        options.RootFolder = "C:\\Data";
        var service = CreateService(options);
        service.IsPathAllowed("C:\\Data\\..\\..\\Windows\\System32").Should().BeFalse();
    }

    [Fact]
    public void IsPathAllowed_CaseInsensitiveMatch_ReturnsTrue()
    {
        var service = CreateService();
        service.IsPathAllowed("/APP/DATA/SUBFOLDER").Should().BeTrue();
    }

    [Fact]
    public void IsPathAllowed_SymlinkOutsideRoot_ReturnsFalse()
    {
        // Even if symlink resolves outside, normalized path should be blocked
        var service = CreateService();
        service.IsPathAllowed("/app/data/../../tmp").Should().BeFalse();
    }
}