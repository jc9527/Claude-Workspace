# Plan #001 — Github Analysis 改造計劃

## 目標

改造 GitHub Analysis 工具，新增以下功能：

- JSON 雙格式輸出（扁平 + 巢狀）
- 月報分析（人員統計 / Repo 活躍度 / PR vs Push）
- 月報三格式輸出（CSV + JSON + Markdown）

## 實作狀態（Claude-Workspace）

- 初版工具：`scripts/github_analysis/monthly_report.py`（見同目錄 `README.md`）。
- 產出：`flat.json`、`nested.json`、`summary.csv`、`summary.md`（預設於 `outputs/github-analysis/<YYYY-MM>/`）。
- 依賴：`gh` 已登入；PR 欄位使用 `gh search prs` 之 `closedAt`（merged 篩選仍由 search query 負責）。
- 未指定 `--year`/`--month` 時之年月互動：優先 `/dev/tty`，含 Cursor 等「stdin 非 TTY」情境；無終端機時退回上一曆月。

## 技術

- Python 3（標準庫）
