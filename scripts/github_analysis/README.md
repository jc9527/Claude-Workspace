# GitHub Analysis（月報／多格式輸出）

對應 `machines/Johnny-MBP-M2/plans/plan-001-github-analysis-upgrade.md`。

## 需求

- 本機已安裝並登入 [GitHub CLI](https://cli.github.com/)（`gh auth login`）。
- Python 3.10+（僅用標準庫）。

## Menu／執行紀錄

- 本腳本在 `main()` 內會呼叫 `menu_state.record_run(__file__)`，供「menu」列出最近執行的 scripts（見 `rules/workspace.md` §4）。
- 其他新建之 `scripts/**/*.py` 建議在 `main()` 開始處同樣記錄，或執行後由 AI 呼叫 `python3 scripts/menu_state.py record <該腳本路徑>`。
- Menu 若需顯示「最近執行」與「檔案 mtime」欄位，見同層上一級 `menu_state.suggest_scripts_for_menu_rows`。

## 用法

```bash
cd /path/to/Claude-Workspace
# 未指定 --org/--repos 時：會先**互動詢問**查詢範圍（o=組織 / r=逗號分隔 repos）；無終端機時須自行傳入 --org 或 --repos。
# 未指定 --year/--month 時：會再互動詢問年、月（同樣優先 /dev/tty）；兩欄皆 Enter = 上一曆月；完全無終端時年月才預設上一曆月。
python3 scripts/github_analysis/monthly_report.py

# 或明確指定組織／月份，或略過等待（排程用）
python3 scripts/github_analysis/monthly_report.py \
  --org YOUR_ORG \
  --year 2026 --month 3 \
  --no-wait
```

私有組織／Repo 需已授權目前 `gh` 帳號。

### 常用參數

| 參數 | 說明 |
|------|------|
| `--org` | 組織登入名（與 `--repos` 擇一；**皆省略**時互動詢問範圍，無終端則錯誤退出） |
| `--repos` | 逗號分隔的 `owner/repo` 清單；同上 |
| `--year` / `--month` | 報表曆月（**本地**月初 00:00～下月月初）；**兩者皆省略**：優先 `/dev/tty` 詢問（IDE 內亦常可用），否則 stdin 為 TTY 時詢問；皆不可時用上一曆月；只給其中一個會報錯 |
| `--no-wait` | 略過執行前 5 秒等待 |
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
