# Skills 索引

每個 Skill 代表一個專業角色。遇到對應情境時，**必須先讀該 Skill 的 `SKILL.md`**，依其流程執行，不得跳過。

---

## 觸發規則

| 情境關鍵字 | 必讀 Skill | 路徑 |
|-----------|------------|------|
| 測試、QA、test cases、腳本驗證、Bug 回報 | qa-engineer | `skills/qa-engineer/SKILL.md` |
| 需求分析、User Story、驗收標準、功能規格 | business-analyst | `skills/business-analyst/SKILL.md` |
| 系統架構、Repo 規劃、技術選型、模組拆分 | system-architect | `skills/system-architect/SKILL.md` |
| API 設計、DB Schema、UI 設計、SD 文件 | system-designer | `skills/system-designer/SKILL.md` |
| 開發、實作、寫程式、修 Bug | developer | `skills/developer/SKILL.md` |
| 部署、CI/CD、Docker、環境設定 | devops | `skills/devops/SKILL.md` |
| 報價、工時估算、成本分析 | quoter | `skills/quoter/SKILL.md` |
| 專案進度、風險管理、任務追蹤 | project-manager | `skills/project-manager/SKILL.md` |
| 網路搜尋、資料蒐集、外部資訊查詢 | web-searcher | `skills/web-searcher/SKILL.md` |
| Multi-Agent 協作、派工、流程協調 | cli-agent-orchestration | `skills/cli-agent-orchestration/SKILL.md` |

---

## 使用原則

1. **任務開始前先對照上表**，確認是否有對應 Skill
2. **讀完 SKILL.md 再執行**，特別注意 `rules/` 下的強制規範
3. **一個任務可能跨多個 Skill**（例如：新功能 = system-designer + developer + qa-engineer）
4. **Skill 有明確禁止行為時，絕對不得違反**（例如：qa-engineer Gate 1 未過不能寫腳本）

---

## 各 Skill 強制規範位置

| Skill | 規範檔案 |
|-------|---------|
| qa-engineer | `skills/qa-engineer/rules/qa-flow-gates.md`（Gate 1/2/3） |
| qa-engineer | `skills/qa-engineer/rules/testing-case-standards.md` |
| system-designer | `skills/system-designer/rules/debug-trace-standards.md` |

---

*最後更新：2026-04-18*
