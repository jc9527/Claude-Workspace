---
name: qa-engineer
description: 測試規劃與執行。當需要：
  (1) 設計測試案例
  (2) 執行功能測試
  (3) 報告 Bug
  (4) 建立自動化測試
  使用此 Skill。
---

# QA Engineer Skill

## 觸發時機

- Developer 完成實作後
- 需要測試時
- 需要建立測試計畫時

## 前置輸入

- User Stories 和驗收標準
- Developer 產出的程式碼
- API 規格文件

## 工作流程

### Step 1: 分析需求

- 理解功能需求
- 理解驗收標準
- 識別測試範圍

### Step 2: 設計測試案例

- 正向測試
- 負向測試
- 邊界測試

### Step 3: 執行測試

- 執行測試案例
- 記錄結果
- 報告 Bug

### Step 4: 自動化測試

- 建立自動化測試腳本
- 整合到 CI/CD

## 輸出位置

| 產出 | 位置 |
|------|------|
| 測試計畫 | `tests/TEST_PLAN.md` |
| 測試案例 | `tests/cases/` |
| Bug 報告 | `tests/BUGS.md` |
| 自動化測試 | `tests/automation/` |

## 規則位置

- 測試案例產生規範: `rules/testing-case-standards.md`

## 模板位置

- 測試案例模板: `references/test-case-template.md`
- Bug 報告模板: `references/bug-report-template.md`
- 測試計畫模板: `references/test-plan-template.md`
