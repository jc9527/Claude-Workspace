# 程式碼撰寫規範

---

## 通用原則

| 原則 | 說明 |
|------|------|
| **KISS** | Keep It Simple, Stupid |
| **DRY** | Don't Repeat Yourself |
| **SOLID** | 單一職責、開封原則、里氏替換、介面隔離、依賴反轉 |

---

## 命名規範

### C# / .NET

| 類型 | 規範 | 範例 |
|------|------|------|
| Class | PascalCase | `UserService` |
| Method | PascalCase | `GetUserById` |
| Property | PascalCase | `UserName` |
| Private Field | _camelCase | `_userRepository` |
| Constant | PascalCase | `MaxRetryCount` |
| Interface | I + PascalCase | `IUserRepository` |
| Enum | PascalCase | `OrderStatus` |
| Enum Value | PascalCase | `OrderStatus.Pending` |

### 變數命名

```csharp
// Good
var userName = "John";
var orderList = new List<Order>();
var isActive = true;

// Bad
var x = "John";
var data = new List<Order>();
var flag = true;
```

---

## 程式碼結構

### Controller 範例

```csharp
[ApiController]
[Route("api/v1/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;

    public UsersController(IUserService userService)
    {
        _userService = userService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<UserDto>>> GetUsers()
    {
        var users = await _userService.GetAllAsync();
        return Ok(users);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<UserDto>> GetUser(Guid id)
    {
        var user = await _userService.GetByIdAsync(id);
        if (user == null)
            return NotFound();
        return Ok(user);
    }

    [HttpPost]
    public async Task<ActionResult<UserDto>> CreateUser(CreateUserDto dto)
    {
        var user = await _userService.CreateAsync(dto);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }
}
```

### Service 範例

```csharp
public class UserService : IUserService
{
    private readonly IUserRepository _userRepository;
    private readonly IMapper _mapper;

    public UserService(IUserRepository userRepository, IMapper mapper)
    {
        _userRepository = userRepository;
        _mapper = mapper;
    }

    public async Task<IEnumerable<UserDto>> GetAllAsync()
    {
        var users = await _userRepository.GetAllAsync();
        return _mapper.Map<IEnumerable<UserDto>>(users);
    }
}
```

---

## 錯誤處理

```csharp
// Good
try
{
    var user = await _userRepository.GetByIdAsync(id);
    if (user == null)
        throw new NotFoundException($"User {id} not found");
    return user;
}
catch (NotFoundException)
{
    throw;
}
catch (Exception ex)
{
    _logger.LogError(ex, "Error getting user {Id}", id);
    throw new ApplicationException("Error getting user", ex);
}

// Bad - 吞掉錯誤
try { }
catch { }
```

---

## Repository 模式

```csharp
public interface IUserRepository
{
    Task<User> GetByIdAsync(Guid id);
    Task<IEnumerable<User>> GetAllAsync();
    Task<User> AddAsync(User user);
    Task UpdateAsync(User user);
    Task DeleteAsync(Guid id);
}

public class UserRepository : IUserRepository
{
    private readonly ApplicationDbContext _context;

    public UserRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<User> GetByIdAsync(Guid id)
    {
        return await _context.Users.FindAsync(id);
    }
}
```

---

## 檢查清單

- [ ] 命名符合規範
- [ ] 有适当的錯誤處理
- [ ] 有 Log 記錄
- [ ] 非同步方法有 `async/await`
- [ ] 沒有 magic strings/numbers
- [ ] 有适当的存取修飾符
- [ ] 有 XML 文件註解（公開 API）
