# GitHub Analysis（月報／多格式輸出）

對應 `machines/Johnny-MBP-M2/plans/plan-001-github-analysis-upgrade.md`。

## 需求

- 本機已安裝並登入 [GitHub CLI](https://cli.github.com/)（`gh auth login`）。
- Python 3.10+（僅用標準庫）。

## 用法

```bash
cd /path/to/Claude-Workspace
python3 scripts/github_analysis/monthly_report.py \
  --org YOUR_ORG \
  --year 2026 --month 3 \
  --out-dir outputs/github-analysis
```

私有組織／Repo 需已授權目前 `gh` 帳號。

### 常用參數

| 參數 | 說明 |
|------|------|
| `--org` | 組織登入名（與 `--repos` 擇一） |
| `--repos` | 逗號分隔的 `owner/repo` 清單，精簡 API 次數 |
| `--year` / `--month` | 報表月份（UTC 月初至下月月初） |
| `--out-dir` | 輸出目錄（預設 `outputs/github-analysis/<YYYY-MM>`） |
| `--max-repos` | 掃描 repo 上限（預設 50，避免大型組織過慢） |

## 產出

於輸出目錄寫入：

- `flat.json` — 事件列層級（每筆 commit / 一筆 PR）
- `nested.json` — 依 repo → 作者彙總
- `summary.csv` — 作者維度：commits、merged PRs、活躍 repo 數
- `summary.md` — 同上之 Markdown 表

## 指標說明

- **Commits**：該月在預設分支歷史上、`since`/`until` 範圍內的 commit（近似「push 活動」；非 Audit log 的嚴格 push 事件）。
- **Merged PRs**：以 `gh search prs` 搜尋在該曆日範圍內 **merged** 的 PR（組織模式用 `org:<name>`；`--repos` 模式改以 repo 條件組 query）。

GitHub Search API 有結果筆數上限；大量活動請縮小 repo 範圍或分批月份。
