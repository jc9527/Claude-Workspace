#!/usr/bin/env python3
"""
GitHub 月報：commits（近似 push 活動）+ merged PRs，雙層 JSON + CSV + Markdown。
依賴：gh CLI（已登入）、Python 標準庫。
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, tzinfo
from pathlib import Path
from typing import Any


def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _local_tzinfo() -> tzinfo:
    """系統本地時區（用於曆月邊界）。"""
    return datetime.now().astimezone().tzinfo  # type: ignore[return-value]


def default_last_month_local() -> tuple[int, int]:
    """上一個曆月（本地時區），供未指定 --year/--month 時使用。"""
    now = datetime.now().astimezone()
    if now.month == 1:
        return now.year - 1, 12
    return now.year, now.month - 1


def month_range_local(year: int, month: int) -> tuple[str, str, str]:
    """
    該曆月在本地時區的 [月初 00:00, 下月月初 00:00)，回傳 ISO8601（含偏移）供 GitHub API。
    """
    tz = _local_tzinfo()
    start = datetime(year, month, 1, 0, 0, 0, tzinfo=tz)
    if month == 12:
        end = datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=tz)
    else:
        end = datetime(year, month + 1, 1, 0, 0, 0, tzinfo=tz)
    tag = f"{year:04d}-{month:02d}"
    # 使用 isoformat 讓 since/until 帶本地偏移，與曆月邊界一致
    since_iso = start.isoformat(timespec="seconds")
    until_iso = end.isoformat(timespec="seconds")
    return since_iso, until_iso, tag


def discover_repos_fixed(org: str | None, max_repos: int) -> list[str]:
    """Paginate org repos via gh api, collect full_name."""
    if not org:
        return []
    all_names: list[str] = []
    page = 1
    while len(all_names) < max_repos:
        r = run_gh(
            [
                "api",
                "-H",
                "Accept: application/vnd.github+json",
                f"orgs/{org}/repos?per_page=100&sort=pushed&page={page}",
            ]
        )
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip() or "list repos failed")
        chunk = json.loads(r.stdout or "[]")
        if not chunk:
            break
        for item in chunk:
            fn = item.get("full_name")
            if fn:
                all_names.append(fn)
                if len(all_names) >= max_repos:
                    return all_names
        if len(chunk) < 100:
            break
        page += 1
    return all_names


def fetch_commits_for_repo(
    full_name: str, since_iso: str, until_iso: str
) -> list[dict[str, Any]]:
    owner, repo = full_name.split("/", 1)
    commits: list[dict[str, Any]] = []
    page = 1
    while True:
        r = run_gh(
            [
                "api",
                f"repos/{owner}/{repo}/commits"
                f"?per_page=100&page={page}&since={since_iso}&until={until_iso}",
            ]
        )
        if r.returncode != 0:
            return commits
        batch = json.loads(r.stdout or "[]")
        if not batch:
            break
        for c in batch:
            sha = c.get("sha", "")
            commit = c.get("commit") or {}
            git_author = commit.get("author") or {}
            gh_author = c.get("author") if isinstance(c.get("author"), dict) else None
            login = ""
            if gh_author and gh_author.get("login"):
                login = gh_author["login"]
            else:
                login = str(git_author.get("name") or "unknown")
            date = str(git_author.get("date") or "")
            commits.append(
                {
                    "type": "commit",
                    "repo": full_name,
                    "author": login,
                    "sha": sha,
                    "date": date,
                }
            )
        if len(batch) < 100:
            break
        page += 1
    return commits


def fetch_merged_prs(
    org: str | None,
    repos: list[str],
    since_date: str,
    until_date: str,
) -> list[dict[str, Any]]:
    q_parts: list[str] = [
        f"merged:{since_date}..{until_date}",
        "is:pr",
        "is:merged",
    ]
    if org and not repos:
        q_parts.append(f"org:{org}")
    elif repos:
        q_parts.append("(" + " OR ".join(f"repo:{r}" for r in repos) + ")")
    query = " ".join(q_parts)
    r = run_gh(
        [
            "search",
            "prs",
            query,
            "--json",
            "repository,author,number,closedAt,title",
            "--limit",
            "1000",
        ]
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "search prs failed")
    data = json.loads(r.stdout or "[]")
    flat: list[dict[str, Any]] = []
    for row in data:
        repo_obj = row.get("repository") or {}
        repo = str(repo_obj.get("nameWithOwner") or "")
        author_obj = row.get("author") if isinstance(row.get("author"), dict) else None
        author = str(author_obj.get("login") if author_obj else "") or "unknown"
        flat.append(
            {
                "type": "pr_merged",
                "repo": repo,
                "author": author,
                "number": row.get("number"),
                "closedAt": row.get("closedAt"),
                "title": row.get("title"),
            }
        )
    return flat


def build_nested(flat: list[dict[str, Any]]) -> dict[str, Any]:
    by_repo: dict[str, dict[str, dict[str, int]]] = defaultdict(
        lambda: defaultdict(lambda: {"commits": 0, "prs_merged": 0})
    )
    for row in flat:
        repo = row.get("repo", "")
        author = row.get("author", "unknown")
        t = row.get("type")
        if t == "commit":
            by_repo[repo][author]["commits"] += 1
        elif t == "pr_merged":
            by_repo[repo][author]["prs_merged"] += 1
    return {"repos": {k: {"authors": dict(v)} for k, v in by_repo.items()}}


def author_summary(flat: list[dict[str, Any]]) -> list[dict[str, Any]]:
    commits_by: dict[str, int] = defaultdict(int)
    prs_by: dict[str, int] = defaultdict(int)
    repos_by: dict[str, set[str]] = defaultdict(set)
    for row in flat:
        a = str(row.get("author") or "unknown")
        r = str(row.get("repo") or "")
        if row.get("type") == "commit":
            commits_by[a] += 1
            if r:
                repos_by[a].add(r)
        elif row.get("type") == "pr_merged":
            prs_by[a] += 1
            if r:
                repos_by[a].add(r)
    authors = sorted(set(commits_by.keys()) | set(prs_by.keys()))
    return [
        {
            "author": a,
            "commits": commits_by[a],
            "merged_prs": prs_by[a],
            "active_repos": len(repos_by[a]),
        }
        for a in authors
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def write_md_summary(path: Path, rows: list[dict[str, Any]], label: str) -> None:
    lines = [
        f"# GitHub 月報 — {label}",
        "",
        "| 作者 | Commits | Merged PRs | 活躍 Repo 數 |",
        "| --- | ---:| ---:| ---:|",
    ]
    for row in sorted(
        rows, key=lambda x: (-x["commits"], -x["merged_prs"], x["author"])
    ):
        lines.append(
            f"| {row['author']} | {row['commits']} | {row['merged_prs']} | "
            f"{row['active_repos']} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description="GitHub monthly activity report (gh CLI)")
    p.add_argument("--org", help="GitHub org login")
    p.add_argument(
        "--repos",
        help="Comma-separated owner/repo list (skips org discovery)",
    )
    p.add_argument(
        "--year",
        type=int,
        default=None,
        help="報表年（本地曆月）；與 --month 皆省略則為上一曆月（本地）",
    )
    p.add_argument(
        "--month",
        type=int,
        default=None,
        choices=range(1, 13),
        help="報表月 1–12；與 --year 皆省略則為上一曆月（本地）",
    )
    p.add_argument(
        "--out-dir",
        help="Output directory (default: outputs/github-analysis/<YYYY-MM> under cwd)",
    )
    p.add_argument("--max-repos", type=int, default=50)
    p.add_argument(
        "--no-wait",
        action="store_true",
        help="略過執行前 5 秒等待（排程／自動化用）",
    )
    args = p.parse_args()

    try:
        _scripts_dir = Path(__file__).resolve().parent.parent
        if str(_scripts_dir) not in sys.path:
            sys.path.insert(0, str(_scripts_dir))
        import menu_state  # noqa: PLC0415

        menu_state.record_run(__file__)
    except Exception:
        pass

    if not args.org and not args.repos:
        print("必須指定 --org 或 --repos", file=sys.stderr)
        return 2

    if args.year is None and args.month is None:
        year, month = default_last_month_local()
    elif args.year is not None and args.month is not None:
        year, month = args.year, args.month
    else:
        print(
            "請同時提供 --year 與 --month，或兩者皆省略以使用上一曆月（本地時區）。",
            file=sys.stderr,
        )
        return 2

    if args.repos:
        scope = f"repos={args.repos}"
    else:
        scope = f"org={args.org!r}（最多 {args.max_repos} 個 repo）"
    wait_msg = (
        "立即開始（已指定 --no-wait）。"
        if args.no_wait
        else "5 秒後開始…（可 Ctrl+C 取消）"
    )
    print(
        f"即將查詢 GitHub 活動：{year}-{month:02d}（本地月初 00:00～下月月初 00:00）\n"
        f"範圍：{scope}\n"
        f"{wait_msg}",
        file=sys.stderr,
    )
    if not args.no_wait:
        time.sleep(5)

    since_iso, until_iso, tag = month_range_local(year, month)
    since_day = since_iso[:10]
    until_day = until_iso[:10]

    repos: list[str] = []
    if args.repos:
        repos = [x.strip() for x in args.repos.split(",") if x.strip()]
    else:
        repos = discover_repos_fixed(args.org, args.max_repos)

    flat: list[dict[str, Any]] = []
    for full in repos:
        flat.extend(fetch_commits_for_repo(full, since_iso, until_iso))

    try:
        flat.extend(
            fetch_merged_prs(
                args.org if args.org else None, repos, since_day, until_day
            )
        )
    except RuntimeError as e:
        print(f"警告：PR 搜尋失敗（仍輸出 commits）：{e}", file=sys.stderr)

    out = (
        Path(args.out_dir)
        if args.out_dir
        else Path("outputs") / "github-analysis" / tag
    )
    out.mkdir(parents=True, exist_ok=True)

    (out / "flat.json").write_text(
        json.dumps(flat, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    nested = build_nested(flat)
    (out / "nested.json").write_text(
        json.dumps(nested, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    summary = author_summary(flat)
    write_csv(out / "summary.csv", summary)
    write_md_summary(out / "summary.md", summary, tag)

    print(f"已寫入 {out.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
