#!/usr/bin/env python3
"""
掃描 ~/GitHub/ 下所有 git repo，列出近 N 個月內有活動的 branch/tag。
輸出 MD + CSV 到 machines/<電腦>/github-scan/<repo>/<日期>/

用法：
  python3 scripts/github_scan/scan_repos.py
  python3 scripts/github_scan/scan_repos.py --months 3 --machine Johnny-MBP-M2
"""
from __future__ import annotations

import argparse
import csv
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from git import Repo, InvalidGitRepositoryError, GitCommandNotFound
except ImportError:
    sys.exit("請先安裝 gitpython：pip3 install gitpython")


# ── 路徑設定 ──────────────────────────────────────────────────────────────────

GITHUB_DIR = Path.home() / "GitHub"
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent


def resolve_machine(machine_arg: str | None) -> str:
    if machine_arg:
        return machine_arg.strip()
    env = os.environ.get("CLAUDE_WORKSPACE_MACHINE")
    if env:
        return env.strip()
    if platform.system() == "Darwin":
        r = subprocess.run(["scutil", "--get", "ComputerName"],
                           capture_output=True, text=True, check=False)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip().replace(" ", "-")
    sys.exit("無法決定電腦目錄名，請用 --machine 指定。")


# ── 掃描 ──────────────────────────────────────────────────────────────────────

def find_repos(base: Path) -> list[Path]:
    repos = []
    for p in sorted(base.iterdir()):
        if not p.is_dir() or p.name.startswith("."):
            continue
        if (p / ".git").exists():
            repos.append(p)
        else:
            # 往下再一層找
            for sub in sorted(p.iterdir()):
                if sub.is_dir() and not sub.name.startswith(".") and (sub / ".git").exists():
                    repos.append(sub)
    return repos


def branch_activity(repo: Repo) -> list[dict]:
    rows = []
    for ref in repo.references:
        try:
            commit = ref.commit
            dt = datetime.fromtimestamp(commit.committed_date, tz=timezone.utc)
            is_tag = ref.path.startswith("refs/tags/")
            rows.append({
                "branch": ref.name,
                "type": "tag" if is_tag else "branch",
                "last_commit_date": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "last_commit_msg": commit.message.strip().splitlines()[0][:80],
                "author": commit.author.name,
            })
        except Exception:
            continue
    rows.sort(key=lambda r: r["last_commit_date"], reverse=True)
    return rows


# ── 輸出 ──────────────────────────────────────────────────────────────────────

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, repo_name: str, rows: list[dict]) -> None:
    lines = [
        f"# {repo_name} — 最新 {len(rows)} 筆活動報告",
        f"\n產出時間：{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n",
        "| 類型 | Branch / Tag | 最後 commit | 作者 | 訊息 |",
        "|------|-------------|-------------|------|------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['type']} | `{r['branch']}` | {r['last_commit_date']} "
            f"| {r['author']} | {r['last_commit_msg']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── 互動選 repo ───────────────────────────────────────────────────────────────

def pick_repos(repos: list[Path]) -> list[Path]:
    print("\n掃描到以下 git repo：\n")
    for i, p in enumerate(repos, 1):
        print(f"  {i:>2}. {p.name}")
    print("\n請輸入編號（空白分隔），或輸入 all 全選：")
    raw = input("> ").strip()
    if raw.lower() == "all" or raw == "":
        return repos
    selected = []
    for token in raw.split():
        try:
            idx = int(token) - 1
            if 0 <= idx < len(repos):
                selected.append(repos[idx])
        except ValueError:
            pass
    return selected or repos


# ── 主程式 ────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="掃描 GitHub repos 近期活動")
    ap.add_argument("--machine", default=None, help="machines/ 子目錄名稱")
    ap.add_argument("--all", dest="select_all", action="store_true", help="不互動，直接全選")
    ap.add_argument("--limit", type=int, default=10, help="每個 repo 最多顯示幾筆活動（預設 10）")
    args = ap.parse_args()

    machine = resolve_machine(args.machine)
    date_str = datetime.now().strftime("%Y%m%d")
    scan_base = WORKSPACE_ROOT / "machines" / machine / "github-scan"

    all_repos = find_repos(GITHUB_DIR)
    if not all_repos:
        print(f"在 {GITHUB_DIR} 找不到任何 git repo。")
        return 1

    chosen = all_repos if args.select_all else pick_repos(all_repos)
    if not chosen:
        print("未選擇任何 repo，結束。")
        return 0

    print(f"\n開始掃描 {len(chosen)} 個 repo（每個最新 {args.limit} 筆活動）…\n")
    total = 0

    for repo_path in chosen:
        try:
            repo = Repo(repo_path)
        except (InvalidGitRepositoryError, GitCommandNotFound):
            print(f"  ⚠ 跳過（無法開啟）：{repo_path.name}")
            continue

        rows = branch_activity(repo)[:args.limit]
        if not rows:
            print(f"  — 無活動：{repo_path.name}")
            continue

        out_dir = scan_base / repo_path.name / date_str
        out_dir.mkdir(parents=True, exist_ok=True)

        write_csv(out_dir / "activity.csv", rows)
        write_md(out_dir / "activity.md", repo_path.name, rows)

        print(f"  ✅ {repo_path.name}（最新 {len(rows)} 筆）→ {out_dir.relative_to(WORKSPACE_ROOT)}")
        total += len(rows)

    print(f"\n完成！共 {total} 筆活動，輸出至 machines/{machine}/github-scan/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
