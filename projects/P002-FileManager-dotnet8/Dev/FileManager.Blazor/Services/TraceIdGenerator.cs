namespace FileManager.Blazor.Services;

public class TraceIdGenerator : ITraceIdGenerator
{
    private static int _counter = 0;
    private static readonly object _lock = new();
    private static string _lastDate = string.Empty;

    public string Generate(string dimension, string function)
    {
        var today = DateTime.UtcNow.ToString("yyyyMMdd");

        lock (_lock)
        {
            if (_lastDate != today)
            {
                _lastDate = today;
                _counter = 0;
            }
            _counter++;
            return $"P002-{dimension}-{function}-{today}-{_counter:D6}";
        }
    }
}
