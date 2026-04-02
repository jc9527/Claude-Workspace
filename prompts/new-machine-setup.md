# 新電腦加入 Claude Workspace 指南

## 使用方式
在新電腦的 Claude Code 中貼上下方提示詞，Claude 會自動完成所有設定。

---

## 提示詞

請幫我在這台新電腦上初始化 Claude Workspace 環境。按照以下步驟執行：

Step 1：Clone Claude-Workspace
git clone https://github.com/jc9527/Claude-Workspace.git ~/GitHub/Claude-Workspace

Step 2：讀取偏好與工作區規範
1. 讀取 <repo>/notes/johnny-preferences.md
2. 讀取 <repo>/rules/README.md，並依索引載入 `rules/*.md`（工作區慣例以 `rules/` 為準）

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

## 目錄結構與共通規範

**完整說明（給人與多種 AI 共用）請讀：** `rules/README.md`，並視需要開啟：

- `rules/workspace.md` — 目錄結構、命名、Commit、工作規則、menu
- `rules/prompts-and-scripts.md` — `prompts/` 與 `scripts/` 分工

（以下不再重複條列，避免與 `rules/` 內容分叉。）
