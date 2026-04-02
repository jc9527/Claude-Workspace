# 工作區結構與共同規範

適用範圍：**本 repository（Claude-Workspace）根目錄**。路徑皆以專案根目錄為準，不依賴固定本機絕對路徑。

## 1. 目錄結構

| 路徑 | 用途 |
|------|------|
| `prompts/` | 提示詞模板（需 AI 判斷的指令與流程） |
| `notes/` | 跨電腦共用筆記與偏好摘要 |
| `machines/<電腦目錄>/` | 每台電腦一組；內含 `info.md` 與 `plans/` |
| `rules/` | 本工作區共用規範（多 AI 可讀之 Markdown） |
| `scripts/` | 自動化腳本（不需 AI 即可執行） |
| `outputs/` | 產出檔案 |

## 2. 命名規範

- **電腦目錄名**：以 macOS `scutil --get ComputerName` 為準，**空格改為 `-`**（例：`Johnny MBP M2` → `Johnny-MBP-M2`）。
- **Plan 檔名**：`plan-XXX-描述.md`（`XXX` 為序號，`描述` 簡短 kebab 或中文皆可，全 repo 一致即可）。
- **Git commit 訊息前綴**：`feat` / `refactor` / `docs` / `fix`。
- **文件語言**：本工作區規範與主要說明文件以**繁體中文**為主。

## 3. 工作規則

- 每台電腦的 **Plan 僅在該台電腦上執行與追蹤**。
- AI 預設只讀取、只操作 **`machines/<當前電腦目錄>/plans/`** 下的計畫；`<當前電腦目錄>` 規則見上節。
- **跨電腦共用**內容放在 `notes/`（或本 `rules/`），不要只寫在某一台的 `plans/`。

## 4.「menu」快捷行為

當使用者輸入 **「menu」** 時：

1. **Prompts**：列出專案根目錄 `prompts/` 下**最新 3 個** `.md` 檔（依修改時間，新→舊）。
2. **Plans**：列出 `machines/<當前電腦目錄>/plans/` 下**最新 3 個** `.md` 檔（同上）。
3. 以**數字選項**（1、2、3…）呈現，讓使用者選擇。
4. 使用者選定後：**讀取該檔**並執行其對應操作或流程。

若無法取得本機電腦名稱，可請使用者提供，或依使用者目前開啟路徑推斷 `machines/` 下對應子目錄並先確認。

## 5. 與其他規範的關係

- **個人偏好與語氣**：`notes/johnny-preferences.md`。
- **Prompts／Scripts 分工細節**：`rules/prompts-and-scripts.md`。
- **公司產品開發規範**：`devpro-agent-rules` / 各專案 `AGENTS.md`，與本目錄互補、不互相替代。
