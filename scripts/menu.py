#!/usr/bin/env python3
"""
列印 workspace §4 格式之 menu（Prompts / Plans / Scripts、連續編號、UTC 時間）。
自 repo 根執行：python3 scripts/menu.py [--machine DIR]
"""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

import menu_state  # noqa: E402


def _die(msg: str, code: int = 2) -> NoReturn:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def _resolve_machine(machine_arg: str | None) -> str:
    if machine_arg and machine_arg.strip():
        return machine_arg.strip()
    env = os.environ.get("CLAUDE_WORKSPACE_MACHINE")
    if env and env.strip():
        return env.strip()
    if platform.system() == "Darwin":
        r = subprocess.run(
            ["scutil", "--get", "ComputerName"],
            capture_output=True,
            text=True,
            check=False,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip().replace(" ", "-")
    _die(
        "無法決定電腦目錄名。請設定環境變數 CLAUDE_WORKSPACE_MACHINE，"
        "或傳入 --machine（與 rules/workspace.md §2 一致，例如 Johnny-MBP-M2）。",
        2,
    )


def _top_md_by_mtime(glob_dir: Path, pattern: str, limit: int) -> list[Path]:
    if not glob_dir.is_dir():
        return []
    paths = sorted(
        glob_dir.glob(pattern),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )[:limit]
    return paths


def _print_table(headers: list[str], rows: list[list[str]]) -> None:
    line = "| " + " | ".join(headers) + " |"
    sep = "|" + "|".join("---" for _ in headers) + "|"
    print(line)
    print(sep)
    for row in rows:
        print("| " + " | ".join(row) + " |")


def main() -> int:
    ap = argparse.ArgumentParser(description="列印 Claude-Workspace menu（見 rules/menu.md）")
    ap.add_argument(
        "--machine",
        default=None,
        help="machines/<此目錄>/plans/；省略時用 CLAUDE_WORKSPACE_MACHINE 或 macOS scutil",
    )
    args = ap.parse_args()

    root = menu_state.find_workspace_root()
    if root is None:
        _die("找不到工作區根目錄（需含 rules/workspace.md）。請在 repo 根目錄或子目錄下執行。", 2)

    machine = _resolve_machine(args.machine)
    plans_dir = root / "machines" / machine / "plans"
    if not plans_dir.is_dir():
        _die(
            f"找不到 Plans 目錄：{plans_dir.relative_to(root)!s}\n"
            f"請確認電腦目錄名正確（--machine 或 CLAUDE_WORKSPACE_MACHINE）。",
            2,
        )

    prompts = _top_md_by_mtime(root / "prompts", "*.md", 3)
    plans = _top_md_by_mtime(plans_dir, "*.md", 3)
    script_rows = menu_state.suggest_scripts_for_menu_rows(3, root=root)

    n = 1
    print("### Prompts（`prompts/`）\n")
    if prompts:
        rows: list[list[str]] = []
        for p in prompts:
            mtime = menu_state.mtime_to_utc_iso(p.stat().st_mtime)
            rows.append([str(n), f"`{p.name}`", mtime])
            n += 1
        _print_table(["#", "檔案", "mtime (UTC)"], rows)
    else:
        print("（無 `.md` 檔）\n")

    print("\n### Plans（`machines/%s/plans/`）\n" % machine)
    if plans:
        rows_p: list[list[str]] = []
        for p in plans:
            mtime = menu_state.mtime_to_utc_iso(p.stat().st_mtime)
            rows_p.append([str(n), f"`{p.name}`", mtime])
            n += 1
        _print_table(["#", "檔案", "mtime (UTC)"], rows_p)
    else:
        print("（無 `.md` 檔）\n")

    print("\n### Scripts（`scripts/**/*.py`）\n")
    if script_rows:
        rows_s: list[list[str]] = []
        for r in script_rows:
            lr = r.get("last_run_at") or "—"
            m = r.get("file_mtime_utc") or "—"
            rows_s.append([str(n), f"`{r['path']}`", str(lr), str(m)])
            n += 1
        _print_table(["#", "路徑", "last_run_at", "mtime (UTC)"], rows_s)
    else:
        print("（無腳本）\n")

    n += 1
    print(f"\n{n}. 📁 瀏覽 Workspace 目錄")

    return 0


if __name__ == "__main__":
    sys.exit(main())
