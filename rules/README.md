# Claude-Workspace 共用規範（多 AI 可讀）

本目錄為**純 Markdown**，不依賴特定 IDE 的規則格式，便於 Cursor、Claude Code、網頁版或其他工具共用。

## 索引

| 檔案 | 內容 |
|------|------|
| [workspace.md](workspace.md) | 目錄結構、命名、Commit、工作規則、menu 指令 |
| [prompts-and-scripts.md](prompts-and-scripts.md) | `prompts/` 與 `scripts/` 分工、命名 + 錯誤處理規範 |
| [idea-process.md](idea-process.md) | Idea 處理流程：必須先提供 Plan 與複雜度評估，不可直接執行 |

## 使用方式

- 新任務開始時：請 AI **先讀** `rules/README.md`，再依需求開啟上述檔案。
- 輸出「menu」時：**優先**執行 `python3 scripts/menu.py`（stdout 即 menu）；若 `rules/` 內**任一檔**的 mtime **新於** `scripts/menu.py`，或腳本失敗，則依 `workspace.md` §4 **手動**組 menu。Scripts 排序與時間欄之邏輯見 `scripts/menu_state.py` 的 `suggest_scripts_for_menu_rows`。
- 與個人語氣、公司背景相關的偏好：見 `notes/johnny-preferences.md`；產品開發規範：見公司 `devpro-agent-rules`／各 repo 的 `AGENTS.md`。

## 更新原則

- 僅調整「工作區慣例」時，優先改 `rules/*.md`，再檢查 `prompts/*.md` 是否仍正確引用。
- 本目錄文件使用**繁體中文**。

## 維護規則
- 當 rules/ 下任何規範檔案異動時，應提醒用戶更新 `rule_summary.md`
- `rule_summary.md` 是所有規範的快速摘要，讓 AI 和用戶快速了解現有規則
