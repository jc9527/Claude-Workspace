# P002-FileManager-dotnet8 專案回顧與檢討

**日期：** 2026-04-06
**作者：** 龍哥 🐉
**歷程：** 2026-04-05 ~ 2026-04-06

---

## 📋 一、專案背景與目標

### 來源系統
- **原始系統：** devpro-tw/FileManager（.NET Framework 4.7 + DevExpress MVC v18.2，Windows only）
- **痛點：** DevExpress 只能跑在 Windows，無法容器化或移到 Linux

### 目標
將檔案管理系統重建為跨平台版本：
- ✅ Framework：.NET 8
- ✅ UI 框架：Blazor Server（選擇 Radzen Blazor，免費 MIT）
- ✅ 平台：支援 Ubuntu（Linux）
- ✅ 移植 11 項核心功能（FM-001 ~ FM-011）

---

## 🏗️ 二、架構決策

### 2.1 UI 框架選擇歷程

| 階段 | 選擇 | 理由 |
|------|------|------|
| 最初 | DevExpress Blazor | 直接移植，但付費 |
| 評估後 | Radzen Blazor | 完全免費 MIT，.NET 8 支援完整，開源 |

**commit:** `0de44f9` — 確認使用 Radzen Blazor

### 2.2 後端架構

```
Blazor Server (InteractiveServer)
    ├── Program.cs（DI, Middleware, CORS, Auth）
    ├── Controllers/
    │   ├── FilesController    — 檔案操作 API
    │   ├── FoldersController  — 資料夾操作 API
    │   ├── SettingsController — 設定讀取 API
    │   ├── UploadController   — 上傳 API
    │   └── AuthController     — 登入/登出/ session API
    ├── Services/
    │   ├── FileService        — 實作 IFileService
    │   ├── FolderService     — 實作 IFolderService
    │   ├── ConfigService     — 讀取 appsettings.json
    │   └── SessionService    — Auth session（曾用 HttpClient，後改 IJSRuntime）
    └── Middleware/
        └── DebugTraceMiddleware — 全域 Debug Header（X-Trace-ID, X-Request-Duration-Ms, X-Server-Time）
```

### 2.3 關鍵設計

- **RootFolder：** `/home/devpro/data`（非 `app/data`）
- **Debug Header：** 每個 API 回應都附加追蹤 header
- **認證方式：** Session Cookie（`.FileManager.Session`），HttpOnly
- **Render Mode：** `RenderMode.InteractiveServer`（commit `04591c3` 修復了 SignalR circuit 未啟動問題）

---

## 📅 三、Git 開發歷程

### Day 1（2026-04-05）

| Commit | 內容 |
|--------|------|
| `63910da` | 建立專案目錄，確認 Radzen Blazor |
| `0de44f9` | 確認 UI framework |
| `4163a4b` | **大重構**：Index page 從 HttpClient 改 service injection，支援 SSR；加入所有 API controllers；DebugTraceMiddleware |
| `491b52f` | 新增 FM-004 移動、FM-010 多選下載、toolbar UI |
| `838c03b` | Toolbar 按鈕加上文字標籤 |
| `04591c3` | **🔴 重要修復**：Routes 加上 `@rendermode="InteractiveServer"` — 解決 Blazor SSR 無法互動問題 |
| `f040e96` | 整合所有 UI 元件（toolbar, dialogs, context menu, search）|

### Day 2（2026-04-06）

| Commit | 內容 |
|--------|------|
| `e1acc54` | 新增登入系統（AuthController + SessionService + Login.razor） |
| `c36ec95` | SessionService 改用 JS interop，側邊欄依角色過濾 |
| `385d3c5` | **🔴 登入流程修復**：SessionService 從 HttpClient 改 IJSRuntime；performLogin 改 window.location.assign |
| `c6d5a35` | QA 截圖 + 報告（Sub-agent） |
| `99b8026` | 龍哥補測 API + Playwright 截圖 + 合併報告 |
| `20f21d3` | 報告 v2：標註 4 個需補測的截圖 |

---

## 🐞 四、踩到的坑（重要檢討）

### 🔴 坑 1：Blazor SSR 電路中斷導致無限迴圈（最嚴重）

**問題：** Playwright headless 環境中，Login 成功後（API 200 OK）頁面一直卡在 `/login`，URL 不斷重複 redirect。

**根本原因（分階段）：**

1. **第一層：** `SessionService` 原本用 `HttpClient`（伺服器端，無瀏覽器 cookie）→ `/api/auth/session` 永遠回 `IsAuthenticated=false` → redirect `/login`
2. **第二層：** 改用 `IJSRuntime`（瀏覽器端，有 cookie）→ `OnAfterRenderAsync` 在 SSR 時就觸發了，但 SSR 沒有電路 → JS interop 拋異常被 catch → 回 `null` → redirect `/login`
3. **第三層：** Login 用 `Navigation.NavigateTo("/", forceLoad: true)` → Blazor circuit 不穩 → 又觸發 auth check → 迴圈

**修復嘗試：**
- ❌ 5秒延遲 + 3次重試 → 無效
- ❌ `IJSInProcessRuntime` 檢查 → 無效
- ❌ `PersistentComponentState` → 未實作
- ✅ `window.location.assign('/')` 純 JS 導航 → 緩解但未完全解決

**教訓：** Blazor Server 的 SSR 和 InteractiveServer 混合模式中，`OnAfterRenderAsync` 在兩種情境都會以 `firstRender=true` 觸發，電路連線時序極難用程式碼可靠判斷。**建議：改用 Blazor WebAssembly 或在 SSR 用 HttpContextAccessor 做 auth check。**

**commit:** `385d3c5`（部分修復）

---

### 🔴 坑 2：Routes 缺少 `@rendermode` 導致 SignalR 未啟動

**問題：** 初期所有元件點擊無反應，Blazor 無法互動。

**根本原因：** `Routes.razor` 沒加 `@rendermode="InteractiveServer"`，整個 app 以 SSR 模式渲染，沒有 SignalR 電路。

**修復：** `04591c3` — `Components/Routes.razor` 加入 `@rendermode`。

---

### 🔴 坑 3：Index.razor 直接用 HttpClient 呼叫 API

**問題：** `OnInitializedAsync` 中用 `HttpClient` 直接呼叫 `http://localhost:5220/api/...`，在 Blazor SSR 環境 HTTP 要求發不出去。

**根本原因：** SSR 是純伺服器端渲染，沒有 `HttpClient` 的客戶端綁定，直接呼叫外部 URL 會失敗。

**修復：** `4163a4b` — 改用 service injection（`IFileService`, `IFolderService`），這些 service 在 DI 中已設定 `HttpClient` BaseAddress。

---

### 🟡 坑 4：DevExpress → Radzen 功能落差

| DevExpress 功能 | Radzen 替代 |
|----------------|-------------|
| FileManager 元件 | 無，需自建 |
| 拖拉上傳 | 需自建 UI |
| 縮圖檢視 | 需自建 |

**影響：** UI 元件 100% 需自建，比預期多工時。

---

### 🟡 坑 5：Blazor Server headless Playwright 不穩

**問題：** QA 需要 Playwright 截圖，但 Blazor Server 的 SignalR 電路在 headless Chrome 環境連線慢、容易斷。

**影響：** TC-004、TC-005、TC-109、TC-110 四個登入後的截圖無法在自動化環境取得。

**建議：** 改用 Blazor WebAssembly（pure client-side，無 SignalR 電路問題）或使用真實瀏覽器截圖。

---

## ✅ 五、目前完成進度

### 功能完成度

| 功能 | 狀態 | 備註 |
|------|------|------|
| FM-001 資料夾瀏覽 | ✅ 完成 | |
| FM-002 建立資料夾 | ✅ 完成 | |
| FM-003 重新命名 | ✅ 完成 | API + UI 截圖 |
| FM-004 移動檔案 | ✅ 完成 | API + UI 截圖 |
| FM-005 刪除 | ✅ 完成 | API + UI 截圖 |
| FM-006 單一上傳 | ✅ 完成 | API + UI 截圖 |
| FM-007 多重上傳 | ✅ 完成（API） | UI 复用上傳對話框 |
| FM-008 拖拉上傳 | ⏸️ 未實作 | 建議後續新增 |
| FM-009 下載 | ✅ 完成 | API 正常，瀏覽器直接下載 |
| FM-010 多重下載 | ✅ 完成 | API 回傳 ZIP |
| FM-011 搜尋 | ✅ 完成 | API + UI 截圖 |

### QA 測試結果

| 項目 | 結果 |
|------|------|
| API 測試 | 12/12 PASS |
| UI 截圖（已取得） | 19 張 |
| UI 截圖（需補測） | 4 張（TC-004/005/109/110）|
| 安全性測試 | ✅ 路徑遍歷防護、rootFolder 隔離 |

---

## 📊 六、數據統計

| 指標 | 數值 |
|------|------|
| 開發天數 | 2 天 |
| Git Commits | 31 個 |
| 核心功能數 | 11 個（FM-001 ~ FM-011）|
| 程式碼變更 | ~9,665 行新增 |
| 測試截圖 | 33 張 |
| QA 報告 | 3 個版本 |

---

## 🎯 七、後續建議

### 高優先
1. **補測 4 張截圖**（TC-004/005/109/110）— 用真實瀏覽器驗證登入後 Dashboard
2. **FM-008 拖拉上傳 UI** — 目前缺口，需實作

### 中優先
3. **驗證程式碼修復後的登入流程** — commit `385d3c5` 需要在真實瀏覽器確認
4. **.unit tests** — 目前只有 ConfigServiceTests，其他 service 缺少 UT

### 低優先
5. **Blazor WASM 改造** — 從 Blazor Server 改為 WASM，解決 headless 自動化問題
6. **FM-007 多重上傳 UI** — 確認多檔選擇 UI 是否正常
7. **FV-001 縮圖模式** — 目前只有清單模式

---

_本文件由龍哥整理，最後更新：2026-04-06 15:00 GMT+8_
