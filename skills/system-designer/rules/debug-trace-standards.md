# Debug Trace 設計規範

## 目的

在系統設計階段就規劃好除錯追蹤機制，讓後續 QA 測試和 Developer 除錯能夠有效串聯。

---

## Trace ID 格式

```
P{專案}-{維度}-{功能}-{YYYYMMDD}-{序號}

組成說明：
- P{專案}：專案編號，如 P001
- {維度}：UT / SIT / E2E / API
- {功能}：功能簡稱，如 USER / CONTACT / SEARCH
- {YYYYMMDD}：日期
- {序號}：當日流水號（3位數）

範例：
P001-SIT-001-20260405-001    # 專案001，系統整合測試，第1項，2026/04/05，第1次
P001-E2E-001-20260405-001    # 專案001，端對端測試，第1項，2026/04/05，第1次
P002-API-USER-20260405-001   # 專案002，API，使用者功能，2026/04/05，第1次
```

---

## Debug Header 規格

所有 REST API 必須支援以下 Header：

### Request Header（可選，但 QA 測試時必填）

| Header | 說明 | 範例 |
|--------|------|------|
| `X-Trace-ID` | 追蹤 ID | `P001-SIT-001-20260405-001` |
| `X-Testing-Case` | 測試案例 ID | `P001-SIT-001` |
| `X-QA-Debug-Info` | JSON 格式額外測試資訊 | `{"tester":"QA Agent","case":"新增聯絡人"}` |

### Response Header（必有）

| Header | 說明 | 範例 |
|--------|------|------|
| `X-Trace-ID` | 請求中的 Trace ID（原值回傳） | `P001-SIT-001-20260405-001` |
| `X-Testing-Case` | 請求中的 Testing Case（原值回傳） | `P001-SIT-001` |

---

## Log 點規劃

### 必記錄點

| 位置 | 時機 | 記錄內容 |
|------|------|----------|
| API 入口 | 收到請求時 | timestamp, trace_id, method, path, headers, request_body |
| 商業邏輯 | 主要函式執行 | trace_id, function_name, input, output |
| 資料庫操作 | 讀/寫資料庫 | trace_id, operation, table, query, result |
| API 出口 | 回傳回應時 | trace_id, status_code, response_body, duration |
| 例外處理 | try/catch 區塊 | trace_id, error_type, error_message, stack_trace |

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

---

## 測試資料夾結構

每個測試案例應產生以下檔案：

```
traces/
└── {Trace ID}/
    ├── trace_id.txt           # Trace ID 值
    ├── request.json            # 序列化請求（含 headers, body）
    ├── response.json           # 序列化回應（含 status, body）
    ├── log.json                # 除錯日誌陣列
    └── (若有截圖) screenshot.png
```

範例：
```
traces/
└── P001-SIT-001-20260405-001/
    ├── trace_id.txt
    ├── request.json
    ├── response.json
    └── log.json
```

---

## System Designer 產出檢查清單

- [ ] Trace ID 格式定義文件
- [ ] Debug Header 規格文件
- [ ] Log 點規劃圖（標記在系統架構圖上）
- [ ] 預期 Log 格式範例

---

*最後更新：2026-04-05 18:59 GMT+8*