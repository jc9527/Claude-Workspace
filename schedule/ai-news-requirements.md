# AI 新聞摘要需求文件

**建立日期**：2026-04-05
**狀態**：待實作
**提出者**：強哥

---

## 目標

每天早上自動抓取 AI 大廠新聞和產業動態，彙整後推播給使用者。

---

## 涵蓋範圍

| 公司/來源 | 關注內容 |
|-----------|----------|
| OpenAI | ChatGPT、GPT 模型更新、API 新功能、產品發布 |
| Anthropic | Claude 更新、Claude Code、商業化進展 |
| Google | Gemini、Bard、Vertex AI、DeepMind |
| Microsoft | Copilot 更新（Windows、Office、Bing） |
| Meta | Llama 模型、AI Studio、開放生態 |
| AI 產業 | 重要併購、政策、應用趨勢 |

---

## 推播格式

```
📰 AI 晨報 [星期幾] [日期]

🔥 本週亮點
- [標題] - [一句話說明]
- [標題] - [一句話說明]

🏭 大廠動態
• OpenAI: [重點摘要]
• Anthropic: [重點摘要]
• Google: [重點摘要]
• Microsoft: [重點摘要]
• Meta: [重點摘要]

💡 小結
[AI 產業趨勢一句話總結]

---
⏰ 抓取時間：[時間]
🤖 訊息來源：AI News Scraper
```

---

## 技術需求

### 1. 新聞來源
- 使用 DuckDuckGo Web Search（透過 `ddgs` 套件）
- 搜尋關鍵字：`OpenAI news`、`Anthropic Claude AI`、`Google Gemini AI`、`Microsoft Copilot AI`、`Meta AI Llama`
- 選擇近期（1-3 天內）的新聞

### 2. 執行頻率
- 每天早上 **8:00 AM**（GMT+8）
- 使用系統排程（cron）

### 3. 推播方式
- 直接輸出 Markdown 格式到 stdout
- 寫入檔案供後續處理

### 4. 輸出位置
- `outputs/ai-news/YYYY-MM-DD.md`

---

## 技術規格

### 執行者
- **Agent**：WebSearch Agent（負責對外搜尋的 Agent）
- **Skill**：`web-searcher`

### Python 版本
- Python 3.10+（已確認有 pip）

### 所需函式庫
- `ddgs`（DuckDuckGo Search）

### 腳本位置
- `scripts/ai_news_fetcher.py`

### 執行方式
```bash
cd /home/devpro/Claude-Workspace
/usr/bin/python3 scripts/ai_news_fetcher.py
```

### 注意事項
- 連續搜尋多個關鍵字時需加入延遲，避免 Rate Limit
- 建議每次搜尋後等待 2-3 秒

---

## 預計產出

| 項目 | 位置 |
|------|------|
| 主程式 | `scripts/ai_news_fetcher.py` |
| 歷史新聞 | `outputs/ai-news/YYYY-MM-DD.md` |

---

## 風險與限制

1. **DuckDuckGo Rate Limit** - 已加入延遲機制避免
2. **網站結構變更** - 搜尋方式較不易受影響
3. **執行時間** - 預估 1-2 分鐘

---

## 下一步

- [ ] 實作 Python 脚本
- [ ] 測試執行
- [ ] 設定 cron job
- [ ] 整合到 OpenClaw
