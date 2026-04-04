# API 設計模板

---

## 基本格式

```markdown
# [API 名稱] API

**版本**：v1
**基礎路徑**：`/api/v1/[resource]`
**說明**：[API 功能描述]

---

## 認證方式

- [ ] Bearer Token (JWT)
- [ ] API Key
- [ ] OAuth 2.0
- [ ] None

---

## 通用錯誤碼

| HTTP Status | Error Code | 說明 |
|-------------|------------|------|
| 400 | VALIDATION_ERROR | 請求參數驗證失敗 |
| 401 | UNAUTHORIZED | 未授權 |
| 403 | FORBIDDEN | 無權限 |
| 404 | NOT_FOUND | 資源不存在 |
| 500 | INTERNAL_ERROR | 伺服器錯誤 |

---

## API Endpoints

### 1. 取得資源列表

#### Request

| 項目 | 內容 |
|------|------|
| **Method** | GET |
| **URL** | `/api/v1/[resources]` |
| **Headers** | Authorization: Bearer {token} |

#### Query Parameters

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|---------|------|
| page | int | 否 | 1 | 頁碼 |
| pageSize | int | 否 | 20 | 每頁數量 |
| sortBy | string | 否 | createdAt | 排序欄位 |
| sortOrder | string | 否 | desc | asc / desc |
| search | string | 否 | - | 搜尋關鍵字 |

#### Response

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "guid",
        "name": "string",
        "email": "string",
        "createdAt": "datetime"
      }
    ],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "totalItems": 100,
      "totalPages": 5
    }
  }
}
```

---

### 2. 取得單一資源

#### Request

| 項目 | 內容 |
|------|------|
| **Method** | GET |
| **URL** | `/api/v1/[resources]/{id}` |

#### Response

```json
{
  "success": true,
  "data": {
    "id": "guid",
    "name": "string",
    "email": "string",
    "createdAt": "datetime",
    "updatedAt": "datetime"
  }
}
```

---

### 3. 建立資源

#### Request

| 項目 | 內容 |
|------|------|
| **Method** | POST |
| **URL** | `/api/v1/[resources]` |
| **Headers** | Authorization: Bearer {token}<br>Content-Type: application/json |

#### Request Body

```json
{
  "name": "string (required, min:2)",
  "email": "string (required, email format)",
  "phone": "string (optional)"
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "id": "new-guid",
    "name": "string",
    "email": "string"
  },
  "message": "Resource created successfully"
}
```

---

### 4. 更新資源

#### Request

| 項目 | 內容 |
|------|------|
| **Method** | PUT |
| **URL** | `/api/v1/[resources]/{id}` |

#### Request Body

```json
{
  "name": "string (required, min:2)",
  "email": "string (required, email format)",
  "phone": "string (optional)"
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "id": "guid",
    "name": "string",
    "email": "string"
  },
  "message": "Resource updated successfully"
}
```

---

### 5. 刪除資源

#### Request

| 項目 | 內容 |
|------|------|
| **Method** | DELETE |
| **URL** | `/api/v1/[resources]/{id}` |

#### Response

```json
{
  "success": true,
  "message": "Resource deleted successfully"
}
```

---

## 錯誤 Response 格式

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid"
      }
    ]
  }
}
```

---

## 驗證規則

| 欄位 | 規則 |
|------|------|
| name | Required, MinLength(2), MaxLength(100) |
| email | Required, Email format |
| phone | Optional, Phone format |
| status | Required, OneOf(Active, Inactive) |

---

## 範例：會員管理 API

```markdown
# 會員管理 API

**版本**：v1
**基礎路徑**：`/api/v1/members`
**認證**：Bearer Token (JWT)

---

## Endpoints

### GET /api/v1/members

取得會員列表

### GET /api/v1/members/{id}

取得單一會員

### POST /api/v1/members

建立新會員

### PUT /api/v1/members/{id}

更新會員資料

### DELETE /api/v1/members/{id}

刪除會員
```
