# Claude-Workspace 共用規範（多 AI 可讀）

本目錄為**純 Markdown**，不依賴特定 IDE 的規則格式，便於 Cursor、Claude Code、網頁版或其他工具共用。

## 索引

| 檔案 | 內容 |
|------|------|
| [workspace.md](workspace.md) | 目錄結構、命名、Commit、工作規則、menu 指令 |
| [prompts-and-scripts.md](prompts-and-scripts.md) | `prompts/` 與 `scripts/` 分工與命名 |

## 使用方式

- 新任務開始時：請 AI **先讀** `rules/README.md`，再依需求開啟上述檔案。
- 輸出「menu」且 Scripts 需附**執行時間／檔案 mtime** 時，可用 `scripts/menu_state.py` 的 `suggest_scripts_for_menu_rows`（見 `workspace.md` §4）。
- 與個人語氣、公司背景相關的偏好：見 `notes/johnny-preferences.md`；產品開發規範：見公司 `devpro-agent-rules`／各 repo 的 `AGENTS.md`。

## 更新原則

- 僅調整「工作區慣例」時，優先改 `rules/*.md`，再檢查 `prompts/*.md` 是否仍正確引用。
- 本目錄文件使用**繁體中文**。
