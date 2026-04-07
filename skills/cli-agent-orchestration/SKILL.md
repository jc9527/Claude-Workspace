# Claude Code CLI 交互技能

## 功能
透過 Python subprocess/pexpect 與 Claude Code CLI 互動，實現多輪對話與任務執行。

## 使用時機
- 需要 Claude Code 分析專案、給建議
- 需要 Claude Code 執行 scripts/menu.py 等腳本
- 需要將 Claude Code 的來回對話記錄存檔

## 已知限制
- VM 上 Claude CLI 需要登入（`claude auth login`）
- `--print --permission-mode=bypassPermissions` 在某些 VM 上會 hang，改用 `--print --dangerously-skip-permissions` 繞過
- menu.py 需要 `CLAUDE_WORKSPACE_MACHINE=Johnny-MBP-M2` 環境變數

## 腳本範例

### 單次往返（推薦）
```bash
cd /path/to/project && timeout 50 claude --print "你的任務" 2>&1
```

### 多輪往返
```python
import subprocess

questions = [
    "第一題...",
    "第二題...",
    "第三題...",
]

for q in questions:
    result = subprocess.run(
        ["claude", "--print"],
        input=q,
        capture_output=True,
        text=True,
        timeout=120,
    )
    print(result.stdout)
```

### 執行需要環境變數的腳本
```bash
CLAUDE_WORKSPACE_MACHINE=Johnny-MBP-M2 claude --print --dangerously-skip-permissions "執行 python3 scripts/menu.py" 2>&1
```

### 有來回記錄的腳本
```python
import subprocess
from datetime import datetime

TASK = "你的任務"
LOG_FILE = f"/tmp/claude_session_{datetime.now().strftime('%H%M%S')}.md"

with open(LOG_FILE, "w") as f:
    f.write(f"# Claude CLI 互動\n\n**任務：** {TASK}\n\n---\n\n")

result = subprocess.run(
    ["claude", "--print"],
    input=TASK,
    capture_output=True,
    text=True,
    timeout=120,
)

with open(LOG_FILE, "a") as f:
    f.write("## Claude 回應\n\n")
    f.write(result.stdout)
    f.write(f"\n\n**時間：** {datetime.now()}")

print(f"記錄：{LOG_FILE}")
```

## 參數說明

| 參數 | 說明 |
|------|------|
| `--print` | 單次輸出模式（非互動 REPL）|
| `--dangerously-skip-permissions` | 跳過工具執行授權（危險但可用）|
| `--permission-mode=bypassPermissions` | 繞過授權（某些 VM 上會 hang）|
| `CLAUDE_WORKSPACE_MACHINE` | menu.py 需要，設為主機名（如 Johnny-MBP-M2）|

## 授權處理
Claude Code 在 --agent 模式下執行工具時會詢問授權。選項：
1. 用 `--dangerously-skip-permissions` 跳過（推薦純讀取任務）
2. 用 pexpect 偵測 `[y/N]` 並自動回覆 `y`

## 疑難排解

| 問題 | 解法 |
|------|------|
| `Not logged in` | VM 上執行 `claude auth login` |
| 工具執行 hang | 去掉 `--permission-mode=bypassPermissions`，改用 `--dangerously-skip-permissions` |
| menu.py 失敗 | 加 `CLAUDE_WORKSPACE_MACHINE=Johnny-MBP-M2` 環境變數 |
| 輸出為空 | Claude CLI 仍在執行，增加 timeout 或檢查 stderr |

## 位置
- 技能目錄：`skills/cli-agent-orchestration/`
- 相關腳本：`scripts/claude_*`（可參考）
