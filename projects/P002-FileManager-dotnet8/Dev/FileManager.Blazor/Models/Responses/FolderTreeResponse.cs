namespace FileManager.Blazor.Models.Responses;

public class FolderTreeResponse
{
    public string RootPath { get; set; } = string.Empty;
    public List<FolderTreeNode> Nodes { get; set; } = new();
}

public class FolderTreeNode
{
    public string Path { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public bool HasChildren { get; set; }
    public bool Expanded { get; set; }
    public int Level { get; set; }
    public List<FolderTreeNode> Children { get; set; } = new();
}
