#!/usr/bin/env python3
"""
AI News Fetcher - 抓取 AI 大廠新聞並彙整摘要

使用方式：
    cd /home/devpro/Claude-Workspace
    /usr/bin/python3 scripts/ai_news_fetcher.py

輸出：
    - 主程式產出 Markdown 格式的新聞摘要到 stdout
    - 另存一份到 outputs/ai-news/YYYY-MM-DD.md
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict

try:
    from ddgs import DDGS
except ImportError:
    print("請先安裝：pip install ddgs", file=sys.stderr)
    sys.exit(1)

# 設定
SCRIPT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "ai-news"
SEARCH_KEYWORDS = {
    "OpenAI": "OpenAI ChatGPT GPT artificial intelligence",
    "Anthropic": "Anthropic Claude AI model news",
    "Google": "Google Gemini AI Bard",
    "Microsoft": "Microsoft Copilot AI",
    "Meta": "Meta AI Llama",
}
MAX_RESULTS_PER_SOURCE = 3
SEARCH_DELAY = 3  # 每次搜尋後延遲秒數，避免 Rate Limit


def get_news(keyword: str, max_results: int = MAX_RESULTS_PER_SOURCE) -> List[Dict]:
    """使用 DuckDuckGo 搜尋新聞"""
    news_results = []
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(keyword, max_results=max_results))
            for r in results:
                news_results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "source": r.get("source", ""),
                    "date": r.get("date", ""),
                    "snippet": r.get("body", "")[:200],
                })
    except Exception as e:
        print(f"搜尋「{keyword}」時發生錯誤: {e}", file=sys.stderr)
    return news_results


def format_news(category: str, news_list: List[Dict]) -> str:
    """格式化新聞為 Markdown"""
    if not news_list:
        return f"• **{category}**: 暂无最新消息\n"

    lines = []
    for i, news in enumerate(news_list[:3], 1):
        title = news.get("title", "無標題")
        source = news.get("source", "")
        date = news.get("date", "")
        url = news.get("url", "")

        # 清理標題
        title = " ".join(title.split())

        lines.append(f"  {i}. [{title}]({url})")
        if source:
            lines.append(f"     📰 {source} | {date}")

    return "\n".join(lines)


def generate_report(news_by_category: Dict[str, List[Dict]]) -> str:
    """產生完整的新聞報告"""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    time_str = today.strftime("%H:%M")
    weekday = today.strftime("%A")

    # 中文星期
    weekday_cn = {
        "Monday": "週一",
        "Tuesday": "週二",
        "Wednesday": "週三",
        "Thursday": "週四",
        "Friday": "週五",
        "Saturday": "週六",
        "Sunday": "週日",
    }.get(weekday, weekday)

    report = f"""📰 **AI 晨報** {weekday_cn} {date_str}

━━━━━━━━━━━━━━━━━━━━

## 🔥 本週亮點

"""

    # 找出所有新聞中的前 3 條當作亮點
    highlight_count = 0
    for category, news_list in news_by_category.items():
        if news_list and highlight_count < 3:
            top_news = news_list[0]
            title = " ".join(top_news.get("title", "").split())
            url = top_news.get("url", "")
            report += f"- [{title}]({url})\n"
            highlight_count += 1

    report += """
## 🏭 大廠動態

"""

    for category in ["OpenAI", "Anthropic", "Google", "Microsoft", "Meta"]:
        news_list = news_by_category.get(category, [])
        report += f"### {category}\n\n"
        report += format_news(category, news_list)
        report += "\n\n"

    report += """## 💡 小結

AI 產業持續快速發展，各大廠積極推出新模型和功能。建議關注：
- 多模態模型的最新進展
- AI 安全性 和 監管政策
- 企業級 AI 應用落地情況

━━━━━━━━━━━━━━━━━━━━

⏰ 抓取時間：{time_str} (GMT+8)
🤖 訊息來源：AI News Scraper (DuckDuckGo)
""".format(time_str=time_str)

    return report


def save_to_file(content: str, date_str: str):
    """儲存報告到檔案"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"{date_str}.md"

    if output_file.exists():
        output_file = OUTPUT_DIR / f"{date_str}_{datetime.now().strftime('%H%M%S')}.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    return output_file


def main():
    print("🔍 開始抓取 AI 新聞...", file=sys.stderr)

    news_by_category = {}

    for category, keyword in SEARCH_KEYWORDS.items():
        print(f"   抓取 {category}...", file=sys.stderr)
        news = get_news(keyword)
        news_by_category[category] = news
        print(f"   → 取得 {len(news)} 條新聞", file=sys.stderr)
        time.sleep(SEARCH_DELAY)  # 避免 Rate Limit

    # 產生報告
    report = generate_report(news_by_category)

    # 儲存到檔案
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = save_to_file(report, date_str)
    print(f"📁 報告已儲存至：{output_file}", file=sys.stderr)

    # 輸出報告
    print("\n" + "=" * 50)
    print(report)

    print("\n✅ 新聞抓取完成！", file=sys.stderr)


if __name__ == "__main__":
    main()
