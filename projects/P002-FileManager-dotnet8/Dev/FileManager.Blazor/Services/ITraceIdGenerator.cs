namespace FileManager.Blazor.Services;

public interface ITraceIdGenerator
{
    string Generate(string dimension, string function);
}
