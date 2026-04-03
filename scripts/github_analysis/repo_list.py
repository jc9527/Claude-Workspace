#!/usr/bin/env python3
"""產生 GitHub org 的 repo 清單（CSV + JSON）"""
import argparse, csv, json, os, subprocess, sys
from datetime import datetime
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="GitHub org repo list")
    parser.add_argument("--org", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent.parent
    out = root / "outputs" / "github-analysis" / "repo-list"
    today = datetime.now().strftime("%Y%m%d")
    csv_file = out / f"repos_{args.org}_{today}.csv"
    json_file = out / f"repos_{args.org}_{today}.json"

    if csv_file.exists() and not args.force:
        print(f"檔案已存在：{csv_file}，如需重新產生請加 --force")
        sys.exit(0)

    out.mkdir(parents=True, exist_ok=True)

    gh = "/opt/homebrew/bin/gh"
    if not os.path.exists(gh):
        gh = "gh"

    fields = "name,description,isPrivate,defaultBranchRef,primaryLanguage,updatedAt,stargazerCount,forkCount,issues"
    cmd = [gh, "repo", "list", args.org, "--limit", "200", "--json", fields]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)

    repos = json.loads(result.stdout)
    rows = []
    for r in repos:
        rows.append({
            "name": r.get("name", ""),
            "description": (r.get("description") or ""),
            "private": r.get("isPrivate", False),
            "default_branch": (r.get("defaultBranchRef") or {}).get("name", ""),
            "language": (r.get("primaryLanguage") or {}).get("name", ""),
            "updated_at": r.get("updatedAt", ""),
            "stars": r.get("stargazerCount", 0),
            "forks": r.get("forkCount", 0),
            "open_issues": (r.get("issues") or {}).get("totalCount", 0),
        })

    rows.sort(key=lambda x: x["updated_at"], reverse=True)

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"共 {len(rows)} 個 repos")
    print(f"CSV: {csv_file}")
    print(f"JSON: {json_file}")

if __name__ == "__main__":
    main()
