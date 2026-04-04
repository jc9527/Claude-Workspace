---
name: business-analyst
description: 需求分析與 User Story 撰寫。當需要：
  (1) 分析客戶需求並轉化為 User Story
  (2) 訂定驗收標準（Acceptance Criteria）
  (3) 評估需求優先順序（Must/Should/Could）
  (4) 識別風險與假設
  使用此 Skill。
---

# Business Analyst Skill

## 觸發時機

- 用戶說「分析需求」、「建立 User Story」
- 用戶提供需求描述，請求轉化為規格文件
- 需求範圍不明確，需要訪談問題澄清

## 工作流程

### Step 1: 理解需求

如果需求描述不明確，先提出訪談問題：
- 誰是主要使用者？
- 主要的使用情境是什麼？
- 期望的輸出/結果是什麼？
- 有哪些限制條件？

### Step 2: 拆解 User Story

依照 **INVEST 原則** 拆解：
- **I**ndependent（獨立）
- **N**egotiable（可協商）
- **V**aluable（有价值）
- **E**stimable（可估算）
- **S**mall（足够小）
- **T**estable（可測試）

### Step 3: 訂定驗收標準

每個 User Story 需要：
- 明確的 Given-When-Then 格式
- 可測試的標準
- 客觀的完成定義

### Step 4: 評估優先順序

使用 MoSCoW 原則：
- **M**ust Have（必須有）
- **S**hould Have（應該有）
- **C**ould Have（可以有）
- **W**on't Have（這次不會有）

### Step 5: 識別風險與假設

- 技術風險
- 業務風險
- 依賴關係
- 假設條件

## 輸出位置

| 產出 | 位置 |
|------|------|
| User Stories | `requirements/user-stories/` |
| 驗收標準 | `requirements/acceptance-criteria/` |
| 訪談問題 | `requirements/interview-notes/` |

## 模板位置

- User Story 模板: `references/user-story-template.md`
- INVEST 原則: `references/invest-principles.md`
- 驗收標準範例: `references/acceptance-criteria.md`

## 專家知識

### INVEST 檢查清單

- [ ] 每個 Story 是否獨立？（避免依賴）
- [ ] 是否可以協商？（非固定規格）
- [ ] 是否對用戶有價值？
- [ ] 是否可以估算？（足够資訊）
- [ ] 是否足够小？（1-3 天工作量）
- [ ] 是否可以測試？

### Good User Story 範例

```
作為 [線上購物會員]
我希望 [在結帳時查看訂單摘要]
以便 [確認商品、數量、價格無誤後再付款]
```

### Bad User Story 範例

```
身為管理員，我想要一個管理介面，可以做很多事情（太模糊、太大）
```
