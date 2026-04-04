# 命名規範

---

## C# / .NET 命名

| 類型 | 規範 | 範例 |
|------|------|------|
| Class | PascalCase | `UserService`, `OrderController` |
| Method | PascalCase | `GetUserById`, `CreateOrder` |
| Property | PascalCase | `UserName`, `IsActive` |
| Private Field | _camelCase | `_userRepository`, `_config` |
| Protected Field | _camelCase | `_baseUrl` |
| Constant | PascalCase | `MaxRetryCount`, `DefaultPageSize` |
| Interface | I + PascalCase | `IUserRepository`, `IOrderService` |
| Enum | PascalCase | `OrderStatus`, `PaymentMethod` |
| Enum Value | PascalCase | `OrderStatus.Pending` |
| Parameter | camelCase | `userId`, `orderDate` |
| Local Variable | camelCase | `var userList = new List<User>()` |
| Namespace | PascalCase | `Devpro.WatchDog.Services` |
| File Name | 與 Class 同名 | `UserService.cs` |

---

## 資料庫命名

| 類型 | 規範 | 範例 |
|------|------|------|
| Table | PascalCase, 單數 | `User`, `OrderDetail` |
| Column | PascalCase | `UserName`, `CreatedAt` |
| Primary Key | `{TableName}Id` | `UserId`, `OrderId` |
| Foreign Key | `{ReferencedTableName}Id` | `UserId` (in Order) |
| Index | `IX_{TableName}_{ColumnName}` | `IX_User_Email` |
| Unique Index | `UX_{TableName}_{ColumnName}` | `UX_User_Email` |

---

## API 命名

| 類型 | 規範 | 範例 |
|------|------|------|
| Endpoint URL | kebab-case,複數 | `/api/v1/user-accounts` |
| HTTP Method | 大寫 | `GET`, `POST`, `PUT`, `DELETE` |
| Query Parameter | camelCase | `pageSize`, `sortBy` |
| Request Body | PascalCase | `{ "userName": "..." }` |
| Response | PascalCase | `{ "success": true }` |

---

## 變數命名原則

### Good

```csharp
var userName = "John";                    // 具體
var orderList = new List<Order>();         // 清楚表示類型
var isActive = true;                      // 布林用 is/isNot 開頭
var totalAmount = 100m;                   // 明確的單位
var createdDate = DateTime.Now;           // 清楚表達意圖
```

### Bad

```csharp
var x = "John";                           // 意義不明
var data = new List<Order>();             // 太模糊
var flag = true;                           // 不夠明確
var total = 100;                           // 缺少單位
var dt = DateTime.Now;                     // 不夠清楚
```

---

## Boolean 命名

```csharp
// Good
var isActive = true;
var hasPermission = false;
var canEdit = true;
var isNotFound = false;

// Bad
var active = true;
var permission = false;
var edit = true;
var found = false;
```

---

## Method 命名

```csharp
// Good - 動詞開頭
GetUserById()
CreateOrder()
UpdateUserPassword()
DeleteOrder()
ValidateInput()

// Bad - 名詞開頭
UserGetById()
OrderCreate()
```

---

## Collection 命名

```csharp
// Good - 複數或清楚表示
var users = new List<User>();
var userIds = new List<Guid>();
var userMap = new Dictionary<Guid, User>();

// Bad - 單數
var user = new List<User>();    // 應該是 users
```
