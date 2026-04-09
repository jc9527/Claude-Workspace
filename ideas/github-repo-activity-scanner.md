# Idea：GitHub 專案活動掃描器

## 概述
掃描 ~/GitHub/ 下所有 git repo，列出近 3 個月內有活動的 branch / tag / commit。

## 需求
- 掃描所有 git repo（略過非 git 目錄或損壞的 .git）
- 過濾條件：最後 commit 在 3 個月內的 branch
- 列出欄位：
  - Repo 名稱
  - Branch 名稱
  - 最新 commit 日期
  - 最新 commit 訊息（前 60 字）
  - Tag（若有）

## 技術選擇
- Python + GitPython（`pip install gitpython`）
- 輸出：CSV + Markdown 報告

## 輸出位置
`outputs/github-scan/YYYY-MM/`

## 整合
- 加入 menu.py 選單（與 monthly_report.py 同層級）

## 建立日期
2026-04-03
