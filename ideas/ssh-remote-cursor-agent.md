# Idea: SSH 遠端執行 Cursor Agent

**建立日期**：2026-04-05
**狀態**：已提出，待評估
**提出者**：強哥

---

## 目標

透過 SSH 連線，在另一台機器上執行 Cursor Agent（`cursor-agent`），實現跨機器的 AI 工作指派。

---

## 預期效益

- 可以在 VM（龍哥）上指派任務給其他機器的 Cursor Agent
- 分散 AI 運算負載
- 支援不同作業環境（Windows、macOS、Linux）

---

## 技術需求

1. **SSH 連線**
   - SSH 金鑰認證
   - 目標機器的 IP/hostname + 帳號

2. **目標機器需求**
   - 安裝了 `cursor-agent`
   - 已設定 `cursor-agent login`（或 API Key）

3. **風險**
   - TTY 互動問題
   - 認證需要（cursor-agent 需要登入）
   - 網路延遲

---

## 下一步

1. 取得目標機器的 SSH 連線資訊
2. 設定 SSH 金鑰
3. 測試 SSH 連線
4. 測試遠端執行 `cursor-agent --version`
5. 處理 cursor-agent 認證問題

---

## 狀態追蹤

| 日期 | 狀態 | 說明 |
|------|--------|------|
| 2026-04-05 | 已提出 | 等待強哥提供目標機器資訊 |
