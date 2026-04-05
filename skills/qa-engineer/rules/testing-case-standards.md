# 測試案例產生與執行規範 (v3)

## 目的

每個專案啟動時，依據 WBS 識別測試項目，並產出完整的測試案例清單供強哥確認。確保測試結果真實可靠，避免 false positive。建立 QA ↔ Developer 持續修正閉環機制。

---

## 測試層級定義

| 層級 | 說明 | 測試對象 | 負責人 |
|------|------|----------|--------|
| **UT** (Unit Testing) | 單元測試 | 函式、方法、類別 | Developer |
| **SIT** (System Integration Testing) | 系統整合測試 | API、模組之間的介接 | QA / Developer |
| **E2E** (End-to-End Testing) | 端對端測試 | 完整使用者流程 | QA Engineer |

---

## QA ↔ Developer 持續修正閉環機制

```
需求/設計 → 開發 → 測試 → 發現 Bug → 除錯 → 修正 → 驗證 → 持續改善
                            ↑
                            └──────── Bug Trace ID ────────┘
```

### Bug 回報流程（強哥確認後才給 Developer 修正）

```
1. QA 發現 Bug
2. 列出：錯誤描述 + 判斷原因 + 期望結果 + Trace ID
3. → 強哥確認
4. → Develop Agent 修正
5. → QA 驗證
6. → 關閉 Bug + Feedback
```

---

## Bug 回報標準（初期必須遵守）

### 每個 Bug 必須包含

| 欄位 | 說明 | 範例 |
|------|------|------|
| **錯誤描述** | 具體發生了什麼 | 列表頁顯示 404 |
| **判斷原因** | 為什麼這是錯誤 | 頁面應顯示聯絡人列表，但顯示"Not Found" |
| **期望正確結果** | 應該是什麼樣 | 頁面應顯示聯絡人列表，包含搜尋列和新增按鈕 |
| **Trace ID** | 關聯的測試 trace | P001-E2E-001-20260405-180001 |

### 格式範例

```markdown
## Bug 報告：B001

**錯誤描述：**
列表頁在截圖時顯示 404 Not Found，但 HTTP 狀態碼為 200。

**判斷原因：**
截圖顯示頁面內容為「404 - Not Found」，而非預期的聯絡人列表。
這表示頁面內容與預期不符，是 False Positive。

**期望正確結果：**
頁面應顯示「📇 聯絡人管理系統」標題、搜尋列、新增按鈕，
以及聯絡人資料表格。

**Trace ID：**
P001-E2E-001-20260405-180001

**嚴重度：**
High（影響主要功能）
```

---

## E2E 測試防呆機制

### 截圖前必須檢查

```
1. 先確認 HTTP 200
   - curl -I http://localhost:5000/
   - 若非 200，等 3 秒後重試，最多 3 次

2. 截圖後驗證內容
   - 使用 Playwright 檢查頁面關鍵文字
   - 例如：列表頁應包含「聯絡人」或「新增」
   - 若內容不符預期，判定 Fail，重新截圖
```

### E2E 失敗判定

| 情況 | 判定 |
|------|------|
| HTTP 404/500 | **Fail** |
| 截圖顯示錯誤頁面 | **Fail** |
| 頁面內容與預期不符 | **Fail** |
| 截圖時間超過 30 秒 | **Timeout → Fail** |

---

## 除錯追蹤機制

### Trace ID 格式

```
P{專案}-{維度}-{功能}-{YYYYMMDD}-{序號}
範例：P001-SIT-001-20260405-001
```

### API Debug Header

```http
GET /api/contacts HTTP/1.1
X-Trace-ID: P001-SIT-001-20260405-001
X-Testing-Case: P001-SIT-001
X-QA-Debug-Info: {"tester":"QA Agent","timestamp":"2026-04-05T18:00:00Z"}
```

### Log 格式（Developer 實作）

```json
{
  "trace_id": "P001-SIT-001-20260405-001",
  "timestamp": "2026-04-05T18:00:00Z",
  "method": "GET",
  "endpoint": "/api/contacts",
  "request": {...},
  "response": {...},
  "status": "Pass/Fail"
}
```

### 測試案例檔案結構

```
P001-SIT-001/
├── trace_id.txt          # P001-SIT-001-20260405-001
├── request.json          # 序列化請求
├── response.json         # 序列化回應
└── log.txt               # 除錯日誌

P001-E2E-001/
├── trace_id.txt
├── screenshot.png        # E2E 截圖
└── log.txt
```

---

## 測試案例產生流程

```
需求輸入 → 識別 WBS → 識別測試點 → 產生測試案例 → 強哥確認 → 執行
```

---

## 測試報告格式

### 每個測試項目報告包含

1. **測試案例總表**（Pass/Fail 統計）
2. **個別測試結果**（Pass / Fail / Blocked）
3. **附屬資料**
   - Log 檔案（UT/SIT）
   - 截圖（E2E，需通過內容驗證）
   - API Request/Response（序列化）
4. **問題記錄**（Bug 回報需含判斷原因）

---

## 附屬資料命名規則

```
{專案編號}-{TC編號}-{維度}-{時間戳}.{副檔名}

範例：
P001-SIT-001-API-20260405_1800.log
P001-E2E-001-UI-20260405_1800.png
P001-SIT-001-request-20260405_1800.json
P001-SIT-001-response-20260405_1800.json
```

---

## Timeout 設定

| 任務類型 | 建議逾時 |
|----------|----------|
| 一般訊息回覆 | 60s |
| 開發任務（複雜） | 360s（6分鐘） |
| 簡單 Script | 120s |

**派工時使用 `timeoutSeconds` 參數指定**

---

## 注意事項

1. **每個 WBS 項目都應有對應的測試案例**
2. **UT 由 Developer 自行執行，需附 Log**
3. **SIT 和 E2E 由 QA Engineer 執行**
4. **E2E 截圖必須驗證內容，避免 false positive**
5. **所有測試結果都需記錄並回報**
6. **Fail 的項目需記錄問題並追蹤**
7. **Bug 回報必須包含：錯誤描述、判斷原因、期望結果、Trace ID**
8. **Bug 需經強哥確認後才給 Developer 修正**

---

## System Designer（SD）需定義

| 項目 | 說明 |
|------|------|
| Trace ID 格式 | 統一命名規則 |
| Log 點規劃 | 哪些 function 需要打 log |
| Debug Header | API 要哪些 debug header |

## Developer 需實作

| 項目 | 說明 |
|------|------|
| API Debug Header | X-Trace-ID, X-Testing-Case, X-QA-Debug-Info |
| Log 格式 | JSON，含 timestamp、trace_id、request、response |
| 序列化檔案 | 每個 API 測試的 input/output |

---

*最後更新：2026-04-05 18:58 GMT+8 v3*