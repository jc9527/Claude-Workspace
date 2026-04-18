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

## ⚠️ 強制執行順序（不得跳關）

```
Step 1 建立 test_cases
    ↓ [Gate 1：龍哥確認]
Step 2 撰寫腳本
    ↓ [Gate 2：語法驗證]
Step 3 執行測試
    ↓ [Gate 3：結果記錄]
Step 4 結案
```

**Gate 細節見 `rules/qa-flow-gates.md`。每個 Gate 的 checklist 全部打勾才能繼續。**

---

## 觸發時機

- Developer 完成實作後
- 需要測試時
- 需要建立測試計畫時

## 前置輸入

- User Stories 和驗收標準
- Developer 產出的程式碼
- API 規格文件

---

## 工作流程

### Step 1: 建立測試案例文件 → [Gate 1]

1. 理解功能需求與驗收標準
2. 識別測試範圍（正向、負向、邊界）
3. 建立 `QA/test_cases/{功能ID}/description.md`（依模板）
4. **等龍哥確認後才能進入 Step 2**

### Step 2: 撰寫測試腳本 → [Gate 2]

1. 依 description.md 的案例清單撰寫腳本
2. 腳本命名：`QA/p003_test_v{版本}_{功能}.py`
3. 執行 `python3 -m py_compile {腳本}` 確認無語法錯誤
4. 確認腳本案例 ID 與 description.md 一致

### Step 3: 執行測試 → [Gate 3]

1. 確認 Server 為最新版本（重啟後再測）
2. 執行腳本
3. 結果寫入 `QA/TestV{版本}-{功能}-{日期}-R{輪次}/results.json`
4. FAIL 案例開立 Bug 回報

### Step 4: 結案

1. 更新 description.md 的「實際結果」與「狀態判定」
2. 回報 PASS/FAIL 統計

---

## P003 專案路徑規範

| 產出 | 路徑 |
|------|------|
| 測試案例 | `QA/test_cases/{功能ID}/description.md` |
| 測試腳本 | `QA/p003_test_v{版本}_{功能}.py` |
| 執行結果 | `QA/TestV{版本}-{功能}-{日期}-R{輪次}/` |
| Bug 報告 | `QA/BUGS.md` |
| 截圖 | `QA/test_cases/{功能ID}/screenshots/` |

---

## E2E 截圖流程（必須遵守）

### 使用 Playwright 截圖（標準方式）

```python
from playwright.sync_api import sync_playwright
import datetime

def take_screenshot(url, filename):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        response = page.goto(url, wait_until='networkidle')
        if response.status != 200:
            print(f"HTTP {response.status} - FAIL")
            browser.close()
            return False
        page.screenshot(path=filename, full_page=True)
        browser.close()
        return True
```

### 截圖前檢查（用 curl）
```bash
curl -I http://localhost:5001/
# 若非 200，等 3 秒後重試，最多 3 次
```

### 截圖命名規則
```
{專案編號}-E2E-{TC編號}-{時間戳}.png
範例：P003-E2E-FA001-20260418_1200.png
```

---

## 規則與模板

- 強制關卡：`rules/qa-flow-gates.md`
- 測試案例規範：`rules/testing-case-standards.md`
- 測試案例模板：`references/test-case-template.md`
- Bug 報告模板：`references/bug-report-template.md`

---

## 重要提醒

1. **未建立 description.md 禁止寫腳本**
2. **未取得龍哥確認禁止執行**
3. **E2E 測試必須截圖並驗證內容**
4. **所有 FAIL 項目必須開 Bug**
5. **結案前必須更新 description.md 實際結果**
