# System Designer Skill

## 觸發時機

- SystemArchitect 完成 System Architecture 後
- 需要實作詳細設計時
- 需要定義 API 介面時
- 需要設計 UI 畫面時

## 前置輸入

- SystemArchitect 產出的 System Architecture Document
- Application 清單（每個 Application 的類型：Web/WinForm/Console/API）
- User Stories 和 Use Cases

## 工作流程

### Step 1: 分析需求

- 理解 System Architecture
- 理解每個 Application 的目標
- 理解 User Stories 和 Use Cases

### Step 2: API 設計（針對 API Service）

- 定義 Endpoint
- 設計 Request/Response 格式
- 定義錯誤碼
- 設計驗證規則

### Step 3: UI 設計（針對 Web/WinForm）

- 設計頁面結構
- 定義欄位
- 定義按鍵功能
- 定義狀態（正常、錯誤、loading）

### Step 4: 資料庫設計

- 設計 Table Schema
- 定義欄位和類型
- 設計索引
- 定義關聯

### Step 5: 類圖 / 時序圖

- 繪製類圖
- 繪製時序圖

### Step 6: 除錯追蹤設計（新增）

- 定義 Trace ID 格式
- 規劃 Log 點
- 設計 Debug Header

---

## 除錯追蹤設計（Debug Trace Design）

### Trace ID 格式

```
P{專案}-{維度}-{功能}-{YYYYMMDD}-{序號}

範例：
P001-SIT-001-20260405-001
P001-E2E-001-20260405-001
P002-API-USER-20260405-001
```

### Log 點規劃

| 位置 | 說明 | 必填 |
|------|------|------|
| API 入口 | 收到請求時 | ✅ |
| 商業邏輯 | 主要函式執行 | ✅ |
| 資料庫操作 | 讀/寫資料庫 | ✅ |
| API 出口 | 回傳回應時 | ✅ |
| 例外處理 | try/catch 區塊 | ✅ |

### Debug Header 規格

所有 API 必須支援以下 Header：

| Header | 說明 | 範例 |
|--------|------|------|
| `X-Trace-ID` | 追蹤 ID | `P001-SIT-001-20260405-001` |
| `X-Testing-Case` | 測試案例 ID | `P001-SIT-001` |
| `X-QA-Debug-Info` | JSON 格式額外資訊 | `{"tester":"QA","timestamp":"..."}` |

### 系統架構圖標記

在系統架構圖中標記：
- Log 點位置（⚙️ 圖示）
- Debug Header 流向
- Trace ID 傳遞路徑

---

## 輸出位置

| 產出 | 位置 |
|------|------|
| API 規格 | `architecture/api-design/` |
| UI 設計 | `architecture/ui-design/` |
| 資料庫設計 | `architecture/database/` |
| 除錯追蹤設計 | `architecture/debug-trace/` |

## 模板位置

- API 設計模板: `references/api-design-template.md`
- UI 設計模板: `references/ui-design-template.md`
- 資料庫設計模板: `references/database-design-template.md`
- 類圖指南: `references/class-diagram-guide.md`
- 時序圖指南: `references/sequence-diagram-guide.md`
- Debug Trace 設計模板: `references/debug-trace-template.md`（新建）

## 規則位置

- 除錯追蹤規範: `rules/debug-trace-standards.md`（新建）