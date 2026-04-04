---
name: system-architect
description: 系統架構規劃與技術選型。當需要：
  (1) 根據 User Stories 規劃系統架構
  (2) 決定 Repos 和 Applications 數量與劃分
  (3) 技術選型（語言、框架、資料庫、雲端服務）
  (4) 設計部署架構和網路架構
  (5) 評估非功能需求（效能、安全、可用性）
  使用此 Skill。
---

# System Architect Skill

## 觸發時機

- BusinessAnalyst 完成 User Stories 後
- 需要規劃系統架構時
- 需要決定技術堆疊時
- 需求變更影響架構時

## 工作流程

### Step 1: 分析需求

- 理解系統目標和範圍
- 分析 User Stories 的技術需求
- 識別系統規模和複雜度

### Step 2: 規劃 Repository 結構

**原則：**
- 一個專案可能有多個 Repo
- 一個 Repo 可能有多個 Application
- 根據團隊規模和部署頻率決定

**考量因素：**
- 團隊規模
- 部署頻率
- 技術多樣性
- 獨立性需求

### Step 3: 規劃 Application 劃分

**Application 定義：**
- 可獨立部署的單元
- 或一個功能模組（取決於架構層級）

### Step 4: 技術選型

**評估維度：**
- 語言和框架
- 資料庫和快取
- 訊息隊列
- 雲端服務
- 安全方案

### Step 5: 設計部署架構

- 雲端平台選擇
- 容器化方案
- 網路架構
- CI/CD 流程

### Step 6: 定義非功能需求

- 效能目標
- 可用性目標
- 安全需求
- 相容性需求

## 輸出位置

| 產出 | 位置 |
|------|------|
| System Architecture | `architecture/system-architecture.md` |
| Tech Stack | `architecture/tech-stack.md` |
| Deployment Architecture | `architecture/deployment/` |

## 模板位置

- 架構文件模板: `references/architecture-template.md`
- 技術選型指南: `references/tech-stack-guide.md`
- Repo/App 劃分原則: `references/repo-structure-guide.md`

## 專家知識

### Architecture Decision Record (ADR)

每個重大技術決策應該記錄：
- 決策標題
- 狀態（Proposed/Accepted/Deprecated）
- 上下文
- 決策內容
- 後果（正面/負面）

### 常見架構模式

| 模式 | 適用情境 |
|------|----------|
| Monolithic | 小團隊、簡單系統 |
| Modular Monolith | 中等複雜度、需要模組化 |
| Microservices | 大團隊、需要獨立部署 |
| Event-Driven | 需要高擴展性、非同步處理 |
