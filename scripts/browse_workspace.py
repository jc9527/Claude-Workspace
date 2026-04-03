#!/usr/bin/env python3
"""瀏覽 Claude-Workspace 目錄結構"""
import argparse, os, sys
from pathlib import Path

HIDDEN = {'.git', '.claude', '__pycache__', '.DS_Store'}

def find_root():
    p = Path(__file__).resolve().parent.parent
    if (p / "rules").is_dir():
        return p
    sys.exit("找不到 workspace root")

def list_dir(path, level=0):
    items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    entries = []
    for item in items:
        if item.name in HIDDEN:
            continue
        if item.is_dir():
            entries.append({"name": item.name + "/", "path": str(item), "is_dir": True, "size": ""})
        else:
            size = item.stat().st_size
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1048576:
                size_str = f"{size/1024:.1f} KB"
            else:
                size_str = f"{size/1048576:.1f} MB"
            entries.append({"name": item.name, "path": str(item), "is_dir": False, "size": size_str})
    return entries

def main():
    parser = argparse.ArgumentParser(description="瀏覽 Claude-Workspace 目錄")
    parser.add_argument("subdir", nargs="?", default="", help="子目錄路徑（相對於 workspace root）")
    args = parser.parse_args()

    root = find_root()
    target = root / args.subdir if args.subdir else root

    if not target.is_dir():
        print(f"目錄不存在：{target}")
        sys.exit(1)

    # 安全檢查：不允許跳出 workspace
    try:
        target.resolve().relative_to(root.resolve())
    except ValueError:
        print("不允許跳出 Workspace 目錄")
        sys.exit(1)

    rel = target.relative_to(root)
    print(f"📁 {rel or 'Workspace root'}/\n")

    entries = list_dir(target)
    for i, e in enumerate(entries, 1):
        if e["is_dir"]:
            print(f"  {i}. {e['name']}")
        else:
            print(f"  {i}. {e['name']} ({e['size']})")

    print(f"\n  0. ← 返回上層")

if __name__ == "__main__":
    main()
