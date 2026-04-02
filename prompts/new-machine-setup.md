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
