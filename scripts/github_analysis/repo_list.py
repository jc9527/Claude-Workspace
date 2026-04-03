#!/usr/bin/env python3
"""
GitHub Org Repo 清單：輸出 CSV + JSON。
依賴：gh CLI（已登入）、Python 標準庫。
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 確保 /opt/homebrew/bin（gh 在 Mac 上的位置）在 PATH 中
_HOMEBREW_BIN = "/opt/homebrew/bin"
if _HOMEBREW_BIN not in os.environ.get("PATH", "").split(os.pathsep):
    os.environ["PATH"] = _HOMEBREW_BIN + os.pathsep + os.environ.get("PATH", "")


def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def fetch_repos(org: str) -> list[dict]:
    """用 gh api --paginate 取得 org 所有 repos。"""
    result = run_gh([
        "api",
        f"orgs/{org}/repos?type=all&per_page=100",
        "--paginate",
        "--slurp",
    ])
    if result.returncode != 0:
        print(f"gh api 失敗：{result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    # --slurp 將所有頁合併為一個 JSON 陣列的陣列，需展平
    pages = json.loads(result.stdout)
    repos: list[dict] = []
    for page in pages:
        if isinstance(page, list):
            repos.extend(page)
    return repos


def extract_fields(raw: dict) -> dict:
    return {
        "name": raw.get("name", ""),
        "description": raw.get("description") or "",
        "private": raw.get("private", False),
        "default_branch": raw.get("default_branch", ""),
        "language": raw.get("language") or "",
        "updated_at": raw.get("updated_at", ""),
        "stars": raw.get("stargazers_count", 0),
        "forks": raw.get("forks_count", 0),
        "open_issues": raw.get("open_issues_count", 0),
    }


CSV_HEADERS = [
    "name", "description", "private", "default_branch",
    "language", "updated_at", "stars", "forks", "open_issues",
]


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def check_existing(path: Path, force: bool, label: str) -> bool:
    """若檔案已存在且無 --force，印提示後回傳 False；否則回傳 True。"""
    if path.exists():
        if not force:
            print(
                f"{label} 已存在：{path}，如需覆蓋請加 --force 參數",
                file=sys.stderr,
            )
            return False
        print(f"--force 指定，覆蓋已存在的檔案：{path}", file=sys.stderr)
    return True


def main() -> int:
    p = argparse.ArgumentParser(
        description="取得 GitHub org 的 repo 清單，輸出 CSV + JSON。"
    )
    p.add_argument("--org", required=True, help="GitHub 組織名稱")
    p.add_argument(
        "--force",
        action="store_true",
        help="若輸出檔案已存在，強制覆蓋",
    )
    args = p.parse_args()

    today = datetime.now().strftime("%Y%m%d")
    out_dir = Path("outputs") / "github-analysis" / "repo-list"
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / f"repos_{args.org}_{today}.csv"
    json_path = out_dir / f"repos_{args.org}_{today}.json"

    # 兩個檔案只要有一個存在就先檢查
    csv_ok = check_existing(csv_path, args.force, "CSV")
    json_ok = check_existing(json_path, args.force, "JSON")
    if not csv_ok or not json_ok:
        return 1

    print(f"正在查詢 {args.org} 的 repo 清單...", file=sys.stderr)
    raw_repos = fetch_repos(args.org)
    rows = [extract_fields(r) for r in raw_repos]

    write_csv(csv_path, rows)
    write_json(json_path, rows)

    print(f"共 {len(rows)} 個 repos")
    print(f"CSV  → {csv_path}")
    print(f"JSON → {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
