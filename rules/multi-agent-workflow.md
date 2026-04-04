# Multi-Agent 協作流程與架構規範

## 概述

本規範定義多 Agent 協作時的標準流程，確保從需求到交付的每個階段都有明確的責任歸屬和產出標準。

---

## 核心原則

1. **Coordinator（協調者）統一入口** — 用戶只與 Coordinator 溝通，Coordinator 協調其他 Agent
2. **先提案、後執行** — 任何任務執行前，需先提案並獲得確認
3. **階段性交付** — 每個階段產出需確認才往下
4. **標準化輸出** — 所有產出有固定目錄結構

---

## 階段順序（嚴格遵守）

```
需求輸入
    │
    ▼
┌─────────────────────────┐
│  BA（需求分析）           │
│  BusinessAnalyst        │
└───────────┬─────────────┘
            │ 產出：User Stories、功能範圍
            ▼
┌─────────────────────────┐
│  SA（系統分析）           │  ← 這時候才確定 Repos & Applications
│  SystemArchitect        │
└───────────┬─────────────┘
            │ 產出：System Architecture（Repos 數量、Application 劃分、技術選型）
            ▼
┌─────────────────────────┐
│  SD（系統設計）           │
│  SystemDesigner         │
└───────────┬─────────────┘
            │ 產出：API 規格、資料結構、類圖
            ▼
┌─────────────────────────┐
│  Quoter（報價）          │
└───────────┬─────────────┘
            │ 產出：報價單（人力、產品、時程）
            ▼
┌─────────────────────────┐
│  Dev（開發）              │
│  Developer              │
└───────────┬─────────────┘
            │ 產出：原始碼、单元测试
            ▼
┌─────────────────────────┐
│  QA（測試）              │
│  QAEngineer             │
└───────────┬─────────────┘
            │ 產出：測試報告、Bug 清單
            ▼
┌─────────────────────────┐
│  DevOps（部署）           │
└───────────┬─────────────┘
            │ 產出：部署腳本、Dockerfile
            ▼
[Coordinator] 彙整交付
```

---

## 層級關係

```
Project（專案）
│
├── Repo 1
│   │
│   └── Application A
│       ├── requirements/
│       ├── architecture/
│       ├── src/
│       ├── tests/
│       └── outputs/
│
├── Repo 2
│   │
│   ├── Application B
│   └── Application C
│
└── Repo N
    └── ...
```

### 對應表

| 層級 | 一個 Project 有 | 一個 Repo 有 | 一個 Application 有 |
|------|----------------|--------------|-------------------|
| **數量** | 多個 Repo | 多個 Application | — |
| **範例** | ProjectAlpha | Repo: backend-api<br>Repo: frontend-web | App: UserService<br>App: AuthService |

---

## Repo 標準結構

每個 Repo 統一格式：

```
{RepoName}/
│
├── applications/              # 這個 Repo 裡的多個 Application
│   │
│   ├── {ApplicationName}/     # 例如：UserService
│   │   ├── requirements/      # 需求文件（BA 維護）
│   │   │   ├── user-stories/
│   │   │   ├── acceptance-criteria/
│   │   │   └── SPEC.md
│   │   ├── architecture/     # 架構文件（SA/SD 維護）
│   │   │   ├── tech-stack.md
│   │   │   ├── system-design.md
│   │   │   ├── api-design.md
│   │   │   └── deployment/
│   │   ├── src/              # 原始碼（Dev 維護）
│   │   ├── tests/             # 測試（QA 維護）
│   │   └── outputs/           # Agent 產出
│   │       ├── quotes/        # 報價（Quoter）
│   │       ├── reports/       # 報告
│   │       └── logs/          # 日誌
│   │
│   └── {ApplicationName}/     # 其他 Application
│       └── ...
│
├── shared/                    # 跨 Application 共用
│   ├── contracts/
│   └── utilities/
│
├── CLAUDE.md                  # AI 工作規範
├── AGENTS.md                  # Agent 角色定義
└── README.md
```

---

## Agent 角色定義

| Agent | 職責 | 主要產出 |
|-------|------|----------|
| **Coordinator** | 協調統籌、統一入口 | 任務分配、回報彙整 |
| **BusinessAnalyst** | 需求分析、User Story | `requirements/user-stories/` |
| **SystemArchitect** | 系統分析、架構規劃 | System Architecture（確定 Repos/Apps） |
| **SystemDesigner** | 詳細設計、API 規格 | `architecture/api-design.md` |
| **Quoter** | 報價估算 | `outputs/quotes/` |
| **Developer** | 程式開發 | `src/`、`tests/` |
| **QAEngineer** | 測試驗證 | 測試報告、Bug 清單 |
| **DevOps** | 部署自動化 | 部署腳本、Dockerfile |

---

## 提案格式

每個任務執行前，Coordinator 需提供：

```
## 任務提案

**目標**：[用戶想要達成什麼]

**分配**：
- 由 [Agent] 負責
- 其他支援：[Agent list]

**流程**：
1. [步驟一]
2. [步驟二]
...

**複雜度**：Low / Medium / High
**預估時間**：[時間]
**風險**：[可能的問題]

**請確認後我才執行。**
```

---

## 錯誤處理

- Agent 執行失敗 → 立即回報 Coordinator → Coordinator 通知用戶
- 用戶可選擇：修改提案、跳過、終止

---

## 與其他規範的關係

- 本規範補充 idea-process.md 的執行階段
- 與 prompts-and-scripts.md 搭配使用（Script/Prompt 分工）
- 與 workspace.md 搭配使用（目錄結構規範）
