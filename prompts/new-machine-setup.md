# 新電腦加入 Claude Workspace 指南

## 使用方式
在新電腦的 Claude Code 中貼上下方提示詞，Claude 會自動完成所有設定。

---

## 提示詞

請幫我在這台新電腦上初始化 Claude Workspace 環境。按照以下步驟執行：

Step 1：Clone Claude-Workspace
git clone https://github.com/jc9527/Claude-Workspace.git ~/GitHub/Claude-Workspace

Step 2：讀取偏好設定
讀取 ~/GitHub/Claude-Workspace/notes/johnny-preferences.md

Step 3：查詢這台電腦名稱
執行 scutil --get ComputerName

Step 4：建立這台電腦的目錄
在 ~/GitHub/Claude-Workspace/machines/[電腦名稱]/ 下建立 info.md 和 plans/

Step 5：收集電腦資訊寫入 info.md
格式參考 machines/Johnny-MBP-M2/info.md

Step 6：設定 ~/.claude/CLAUDE.md 全域偏好

Step 7：安裝 Agent Skills（sa-agent, sd-agent, pg-agent, qa-agent）

Step 8：安裝 GStack

Step 9：安裝 GitHub CLI

Step 10：Clone devpro-agent-rules

Step 11：Commit 並 Push

Step 12：確認環境

---

## 目錄結構說明
- prompts/ 提示詞模板
- notes/ 跨電腦共用筆記
- machines/[電腦名稱]/ 每台電腦一個目錄（info.md + plans/）
- scripts/ 自動化腳本
- outputs/ 產出檔案

## 規範
- 電腦目錄名用 scutil --get ComputerName，空格用 - 取代
- Plan 編號 plan-XXX-描述.md
- Commit 規範 feat/refactor/docs/fix
- 所有文件使用繁體中文

### 工作規則
- 每台電腦的 Plan 只在該台電腦上執行
- Claude 預設只讀取和操作 machines/[當前電腦名稱]/plans/ 下的計劃
- 跨電腦共用的內容放在 notes/ 目錄

### Prompts 與 Scripts 分工原則

**Scripts（scripts/ 目錄）— 機器可直接執行的工作：**
- 用 Python (.py) 撰寫，確保跨平台（Mac/Windows/Linux）
- 適用場景：收集電腦資訊、安裝工具、建立目錄結構、抓取資料、產生報表、檔案操作
- 不需要 AI 介入，任何電腦都能直接跑
- 命名規則：snake_case，如 setup_machine.py、monthly_report.py

**Prompts（prompts/ 目錄）— 需要 AI 判斷的工作：**
- 用 Markdown (.md) 撰寫
- 適用場景：需求分析、系統設計、Code Review、文件撰寫、決策建議
- 需要 AI 理解上下文和做判斷
- 命名規則：kebab-case，如 new-machine-setup.md、code-review.md

**混合型工作的處理方式：**
- 資料收集用 Script，分析摘要用 Prompt
- 例如：Script 抓取 GitHub commits 資料（JSON/CSV） → Prompt 讓 AI 分析趨勢並產出月報
- 優先腳本化：能寫成 Script 的部分就寫成 Script，只留真正需要 AI 的部分在 Prompt

### Menu 快捷指令
- 用戶輸入「menu」時，列出以下內容讓用戶選：
  - Prompts：~/GitHub/Claude-Workspace/prompts/ 下最新 3 個 .md 檔案
  - Plans：~/GitHub/Claude-Workspace/machines/[當前電腦名稱]/plans/ 下最新 3 個 .md 檔案
- 按檔案修改日期排序，最新在前
- 用數字選項（1/2/3...）讓用戶選擇
- 用戶選擇後，讀取該檔案並執行對應的操作
