# 初始化 Claude Workspace 環境

## 使用方式
在新電腦的 Claude Code 終端機中，直接貼上以下提示詞即可。

## 提示詞

請幫我初始化 Claude 工作環境，執行以下步驟：

1. Clone Claude-Workspace：
git clone https://github.com/jc9527/Claude-Workspace.git ~/GitHub/Claude-Workspace

2. Clone devpro-agent-rules（公司 AI 規範）：
git clone https://github.com/devpro-tw/devpro-agent-rules.git ~/GitHub/devpro-tw/devpro-agent-rules

3. 安裝 Agent Skills 到 Claude Code：
mkdir -p ~/.claude/skills
如果 ~/Downloads/agent-skills/ 存在，複製 sa-agent、sd-agent、pg-agent、qa-agent 到 ~/.claude/skills/

4. 安裝 GStack：
claude install-skill https://github.com/garrytan/gstack

5. 安裝 GitHub CLI（如果沒有）：
brew install gh
然後提醒我執行 gh auth login

6. 確認環境：列出 claude --version、git config、ls ~/.claude/skills/、gh --version

## 備註
- Claude-Workspace 是私有 repo（jc9527），需要 GitHub 登入權限
- devpro-agent-rules 是公司 repo（devpro-tw），需要組織存取權限
- GStack 安裝需要 bun，會自動安裝
- 工作區共通規範（目錄、命名、menu 等）：clone 後見 repo 內 `rules/README.md`
