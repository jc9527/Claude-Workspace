#!/usr/bin/env python3
"""Menu 用：記錄與讀取最近執行的 scripts（本機 JSON，見 rules/workspace.md §4）。"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MARKER = "rules/workspace.md"


def find_workspace_root(start: Path | None = None) -> Path | None:
    p = (start or Path.cwd()).resolve()
    if p.is_file():
        p = p.parent
    for d in [p, *p.parents]:
        if (d / MARKER).is_file():
            return d
    return None


def state_path(root: Path) -> Path:
    return root / "outputs" / ".menu-recent-scripts.json"


def _load_entries(root: Path) -> list[dict[str, Any]]:
    sp = state_path(root)
    if not sp.is_file():
        return []
    try:
        data = json.loads(sp.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [x for x in data if isinstance(x, dict) and "path" in x]
    except (json.JSONDecodeError, OSError):
        pass
    return []


def _save_entries(root: Path, entries: list[dict[str, Any]]) -> None:
    sp = state_path(root)
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def record_run(script_file: str | Path) -> bool:
    path = Path(script_file).resolve()
    root = find_workspace_root(path)
    if root is None:
        return False
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        return False
    norm = rel if not rel.endswith("/") else rel.rstrip("/")
    if not norm.startswith("scripts/"):
        return False
    if Path(norm).suffix.lower() != ".py":
        return False
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entries = _load_entries(root)
    found = False
    for e in entries:
        if e.get("path") == norm:
            e["last_run_at"] = now
            found = True
            break
    if not found:
        entries.append({"path": norm, "last_run_at": now})
    _save_entries(root, entries)
    return True


def get_recent_scripts(limit: int = 3, root: Path | None = None) -> list[str]:
    r = root or find_workspace_root()
    if r is None:
        return []
    entries = _load_entries(r)
    entries.sort(key=lambda x: str(x.get("last_run_at") or ""), reverse=True)
    seen: set[str] = set()
    out: list[str] = []
    for e in entries:
        p = str(e.get("path") or "")
        if p and p not in seen:
            seen.add(p)
            out.append(p)
            if len(out) >= limit:
                break
    return out


def _creation_timestamp(path: Path) -> float:
    """盡可能使用建立時間（birthtime）；不支援或無效時退回 mtime。"""
    try:
        st = path.stat()
        bt = getattr(st, "st_birthtime", None)
        if bt is not None and float(bt) > 0:
            return float(bt)
        return float(st.st_mtime)
    except OSError:
        return 0.0


def _iter_script_py_paths(root: Path, exclude: set[str]) -> list[tuple[Path, str]]:
    scripts_dir = root / "scripts"
    if not scripts_dir.is_dir():
        return []
    out: list[tuple[Path, str]] = []
    for p in scripts_dir.rglob("*.py"):
        if p.name == "__init__.py":
            continue
        try:
            rel = p.relative_to(root).as_posix()
        except ValueError:
            continue
        if rel in exclude:
            continue
        out.append((p, rel))
    return out


def _birthtime_sort_py_paths(root: Path, limit: int, exclude: set[str]) -> list[str]:
    """無執行紀錄時：依檔案建立時間（新→舊）。"""
    rows = _iter_script_py_paths(root, exclude)
    scored: list[tuple[float, str]] = []
    for p, rel in rows:
        t = _creation_timestamp(p)
        if t <= 0:
            continue
        scored.append((t, rel))
    scored.sort(key=lambda x: -x[0])
    return [rel for _, rel in scored[:limit]]


def _mtime_fallback_py_paths(root: Path, limit: int, exclude: set[str]) -> list[str]:
    """有執行紀錄但不足額時：缺額依 mtime 補滿（與 Prompts 一致）。"""
    rows = _iter_script_py_paths(root, exclude)
    paths: list[tuple[float, str]] = []
    for p, rel in rows:
        try:
            m = p.stat().st_mtime
        except OSError:
            continue
        paths.append((m, rel))
    paths.sort(key=lambda x: -x[0])
    return [rel for _, rel in paths[:limit]]


def suggest_scripts_for_menu(limit: int = 3, root: Path | None = None) -> list[str]:
    r = root or find_workspace_root()
    if r is None:
        return []
    if not _load_entries(r):
        return _birthtime_sort_py_paths(r, limit, set())
    recent = get_recent_scripts(limit=limit, root=r)
    if len(recent) >= limit:
        return recent[:limit]
    exclude = set(recent)
    need = limit - len(recent)
    fallback = _mtime_fallback_py_paths(r, need + 50, exclude)
    for rel in fallback:
        if rel in exclude:
            continue
        recent.append(rel)
        exclude.add(rel)
        need -= 1
        if need <= 0:
            break
    return recent[:limit]


def main() -> int:
    ap = argparse.ArgumentParser(description="Menu 腳本執行紀錄")
    sub = ap.add_subparsers(dest="cmd", required=False)
    rec = sub.add_parser("record", help="記錄一次執行")
    rec.add_argument("path", help="腳本路徑（絕對或相對）")
    args = ap.parse_args()
    if args.cmd == "record":
        return 0 if record_run(args.path) else 1
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
