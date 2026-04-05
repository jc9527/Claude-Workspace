# Developer Skill

## 觸發時機

- SystemDesigner 完成 API 設計後
- 需要實作功能時
- 需要修改現有程式碼時

## 前置輸入

- SystemDesigner 產出的 API 規格（含 Debug Trace 設計）
- SystemDesigner 產出的資料庫設計
- UI 設計文件

## 工作流程

### Step 1: 理解規格

- 理解 API 規格
- 理解資料庫 Schema
- 理解需求
- 理解 Trace ID 格式和 Debug Header 規格

### Step 2: 實作

- 實作 Repository/DAO
- 實作 Service 層
- 實作 Controller/API Endpoint
- 實作單元測試

### Step 3: Debug Trace 實作（新增）

- 在 API 加入 Debug Header（X-Trace-ID, X-Testing-Case, X-QA-Debug-Info）
- 在關鍵點加入 Log（JSON 格式）
- 實作 request/response 序列化

### Step 4: Code Review

- 檢視程式碼品質
- 檢視命名規範
- 檢視效能
- 檢視 Debug Trace 是否完整

## Debug Header 實作要求

### Flask API 範例

```python
from flask import request, jsonify
import json
import time

@app.route('/api/contacts', methods=['GET'])
def api_get_contacts():
    trace_id = request.headers.get('X-Trace-ID', '')
    testing_case = request.headers.get('X-Testing-Case', '')
    qa_debug_info = request.headers.get('X-QA-Debug-Info', '{}')
    
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "trace_id": trace_id,
        "level": "INFO",
        "location": "api_entry",
        "method": "GET",
        "path": "/api/contacts",
        "request_headers": dict(request.headers),
        "duration_ms": 0
    }
    
    # 商業邏輯執行
    contacts = load_contacts()
    
    log_entry["response_status"] = 200
    log_entry["response_body"] = contacts
    log_entry["duration_ms"] = elapsed_ms
    
    # Response Header
    resp = jsonify(contacts)
    resp.headers['X-Trace-ID'] = trace_id
    resp.headers['X-Testing-Case'] = testing_case
    
    return resp
```

### Log 格式（JSON）

```json
{
  "timestamp": "2026-04-05T18:00:00.000Z",
  "trace_id": "P001-SIT-001-20260405-001",
  "level": "INFO",
  "location": "api_entry",
  "method": "POST",
  "path": "/api/contacts",
  "request_headers": {...},
  "request_body": {...},
  "response_status": 201,
  "response_body": {...},
  "duration_ms": 45
}
```

### 序列化檔案產出

每個 API 請求/回應需要產出：

| 檔案 | 內容 |
|------|------|
| `{trace_id}_request.json` | 請求完整資訊（headers, body） |
| `{trace_id}_response.json` | 回應完整資訊（status, body） |
| `{trace_id}_log.json` | 除錯日誌陣列 |

---

## 輸出位置

| 產出 | 位置 |
|------|------|
| 程式碼 | `src/` |
| 單元測試 | `tests/` |
| 文件 | `docs/` |
| Debug Trace | `traces/` |

## 模板位置

- 程式碼規範: `references/coding-standards.md`
- 命名規範: `references/naming-conventions.md`

## 規則位置

- Debug Trace 實作: `rules/debug-trace-standards.md`