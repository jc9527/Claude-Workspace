# P002 - FileManager .NET 8 重建計畫

## 專案目標

從現有 FileManager (.NET Framework 4.7 + DevExpress) 遷移到 .NET 8 + Blazor，在 Ubuntu 上運行。

## 現況分析

| 項目 | 現況 |
|------|------|
| 原始程式 | `/home/devpro/github/devpro-tw/FileManager` |
| Framework | .NET Framework 4.7 |
| UI | DevExpress v18.2（Windows only）|
| 目標 | .NET 8 + Blazor |

## 專案目錄

```
P002-FileManager-dotnet8/
├── SD/           # 系統設計文件
├── Dev/          # 開發產出
├── DevOps/       # 環境準備、UT
├── QA/           # 測試報告
└── outputs/      # 最終產出
```

## 執行階段

| Phase | 負責 | 工作 |
|-------|------|------|
| 1 | 龍哥（分析）| 分析現有程式，產出功能需求規格 |
| 2 | SD | 系統設計 |
| 3 | DevOps | .NET 8 環境準備 |
| 4 | Developer | 實作新系統 |
| 5 | QA | 測試驗證 |

## 預估時程

- Phase 1（分析）：1-2 天
- Phase 2（SD）：0.5 天
- Phase 3（DevOps）：0.5 天
- Phase 4（實作）：3-5 天
- Phase 5（測試）：1-2 天

**總計：約 6-10 天**

## 預估成本

（待 Business Analyst / Quoter 估算）

## 風險

| 風險 | 等級 | 對策 |
|------|------|------|
| DevExpress 功能替代 | 🟡 中 | 使用 Blazor 原生元件 |
| 效能議題 | 🟢 低 | Blazor Server 即可 |
| 遷移複雜度 | 🟡 中 | 採 Greenfield 方式 |

## 關聯資源

- 原始 Repo：`/home/devpro/github/devpro-tw/FileManager`
- Claude-Workspace 規範：`/home/devpro/Claude-Workspace/rules/`

---

*最後更新：2026-04-05 21:54 GMT+8*
*Owner：龍哥 🐉*