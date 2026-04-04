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

## 錯誤處理規範（強制）

### Script 執行時

1. **執行前**：使用絕對路徑
   ```bash
   /usr/bin/python3 /path/to/script.py
   ```

2. **執行後**：若 script 退出碼非 0 或有任何錯誤，**停下來，回報給用戶**，不要自行猜測或跳過錯誤繼續執行下一步。

3. **Prompt 裡的任務**：若 Prompt 要求執行的腳本失敗，**先問用戶**「這個腳本執行失敗了，要繼續嗎？還是要我做其他處理？」，不要自己變通執行替代方案。

4. **例外**：若錯誤是因為缺少環境變數或參數，且用戶已經在對話中提供過明確指示，則可以補充缺失項目後重試，但仍須告知用戶你做了什麼調整。

---

## 與 `rules/` 的關係

- 工作區目錄與「menu」行為見 [workspace.md](workspace.md)。
- 本檔定義 **prompts／scripts 職責與命名**，以及**錯誤處理規範**。
