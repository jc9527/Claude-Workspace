# Rules 摘要

最後更新：2026-04-18

## 規範清單

### 1. workspace.md — 工作區規範
定義 Claude-Workspace 的目錄結構（prompts/、notes/、machines/、rules/、scripts/、outputs/）、命名規則（電腦目錄、Plan 檔名、Commit 前綴）、工作規則（Plan 僅在本機執行、跨電腦共用放 notes/），以及 menu 快捷行為與其他規範的關聯索引。

### 2. prompts-and-scripts.md — Prompts 與 Scripts 分工 + 錯誤處理
區分 scripts/（Python、跨平台、無需 AI、snake_case 命名）與 prompts/（Markdown、需 AI 判斷、kebab-case 命名）的使用情境；混合型工作原則為「Script 負責收集，Prompt 負責分析」，能腳本化就優先腳本化。Script 輸出已存在時預設不覆蓋，需確認或加 --force。

**錯誤處理**：Script 執行失敗需回報用戶；Prompt 裡的任務失敗需先問用戶，不要自行變通；環境變數缺失可重試但需告知。

### 3. menu.md — Menu 功能規格
規範輸入「menu」時的行為：優先執行 `python3 scripts/menu.py`；若 rules/ 內有比腳本更新的檔案則手動組合。Menu 顯示最新 3 個 Prompts（1–3）、Plans（4–6）、Scripts（7–9），時間一律 UTC ISO 格式，並附目錄瀏覽功能（最後一選項，可層層進入 Workspace 目錄但不得跳出）。

### 4. README.md — 索引
本 rules/ 目錄的入口文件，列出各規範檔案用途、AI 使用方式（新任務先讀此檔）、menu 行為摘要，以及更新原則（優先改 rules/*.md，繁體中文撰寫）。

### 5. idea-process.md — Idea 處理流程
任何 Idea 討論後，**絕對不可直接執行**。必須先提供：目標、步驟、複雜度（Low/Medium/High）、預估時間、所需工具、風險。等待用戶確認後才可實作。

### 6. multi-agent-workflow.md — Multi-Agent 協作流程
定義從需求到交付的標準階段順序：BA → SA → SD → Quoter → Dev → QA → DevOps。SA 階段才確定 Repos 與 Applications 的劃分。Coordinator 統一入口，先提案後執行。

### 7. skills/README.md — Skills 觸發規則（強制）
任務開始前必須對照觸發規則表，確認是否有對應 Skill。有對應 Skill 時，**必須先讀 `SKILL.md` 再執行**，不得跳過。觸發情境：QA/測試 → qa-engineer；需求分析 → business-analyst；架構設計 → system-architect；API/DB 設計 → system-designer；開發實作 → developer；部署 → devops。

### 8. qa-engineer/rules/qa-flow-gates.md — QA 強制關卡
QA 任務三個 Gate 不得跳關：Gate 1（建立 test_cases/description.md + 龍哥確認）→ Gate 2（腳本語法驗證）→ Gate 3（結果記錄 + description.md 更新）。**未建立 description.md 禁止寫腳本。**
