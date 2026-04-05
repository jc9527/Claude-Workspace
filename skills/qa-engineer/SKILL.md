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
- **截圖驗證（E2E）**
- 記錄結果
- 報告 Bug

### Step 4: 自動化測試

- 建立自動化測試腳本
- 整合到 CI/CD

## E2E 截圖流程（必須遵守）

### 截圖前檢查
```bash
# 1. 先確認 HTTP 200
curl -I http://localhost:5000/
# 若非 200，等 3 秒後重試，最多 3 次

# 2. 截圖
curl -s http://localhost:5000/ > page.html

# 3. 驗證頁面內容
grep -i "關鍵文字" page.html
# 若找不到，判定 Fail
```

### 截圖命令
```bash
# 使用 curl 截圖 HTML
curl -s http://localhost:5000/ > outputs/圖片名稱.html

# 使用 cutycapt 或 wkhtmltopdf 轉 PNG（如果有安裝）
```

### 截圖命名規則
```
{專案編號}-E2E-{TC編號}-{時間戳}.png
範例：P002-E2E-001-20260406_002200.png
```

## 輸出位置

| 產出 | 位置 |
|------|------|
| 測試計畫 | `tests/TEST_PLAN.md` |
| 測試案例 | `tests/cases/` |
| Bug 報告 | `tests/BUGS.md` |
| 自動化測試 | `tests/automation/` |
| E2E 截圖 | `tests/screenshots/` |

## 規則位置

- 測試案例產生規範: `rules/testing-case-standards.md`

## 模板位置

- 測試案例模板: `references/test-case-template.md`
- Bug 報告模板: `references/bug-report-template.md`
- 測試計畫模板: `references/test-plan-template.md`

## 重要提醒

1. **E2E 測試必須截圖**
2. **截圖前必須檢查 HTTP 200**
3. **截圖後必須驗證內容**
4. **截圖命名必須符合規範**
5. **所有 Fail 的項目要附上截圖**
