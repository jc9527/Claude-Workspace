# Prompts 與 Scripts 分工

適用範圍：本 repository 內 `prompts/` 與 `scripts/`。

## Scripts（`scripts/`）

- **技術**：以 **Python（`.py`）** 撰寫，優先維持**跨平台**（macOS／Windows／Linux）。
- **適用**：收集電腦資訊、安裝工具、建立目錄、抓取資料、產生報表、純檔案操作等。
- **原則**：**不需要 AI 介入**即可在機器上重複執行。
- **檔名**：`snake_case`，例如 `setup_machine.py`、`monthly_report.py`。

### Scripts 執行規則

- 當 Script 輸出檔案已存在時，預設不覆蓋，需向用戶確認是否重新產生
- 使用 `--force` 參數可強制重新產生
- 此規則適用於所有會產生輸出檔案的 Script

## Prompts（`prompts/`）

- **技術**：**Markdown（`.md`）**。
- **適用**：需求分析、系統設計、Code Review、文件撰寫、需脈絡判斷的決策等。
- **原則**：需要 **AI 理解上下文並做判斷**。
- **檔名**：`kebab-case`，例如 `new-machine-setup.md`、`code-review.md`。

## 混合型工作

- **資料／事實收集** → Script；**分析、摘要、決策建議** → Prompt。
- 例：Script 輸出 Git commits 的 JSON／CSV → Prompt 分析趨勢並產出月報。
- **優先腳本化**：能寫成 Script 就寫成 Script，只把必須由 AI 處理的部分留在 Prompt。

## 與 `rules/` 的關係

- 工作區目錄與「menu」行為見 [workspace.md](workspace.md)。
- 本檔只定義 **prompts／scripts 職責與命名**。
