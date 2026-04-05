# DevOps Skill

## 觸發時機

- SystemArchitect 完成 System Architecture 後
- 需要準備開發環境時
- 需要執行單元測試時

## 前置輸入

- SystemDesigner 的系統設計文件
- 環境需求（Python/Node 版本、套件清單）
- 測試需求

## 工作流程

### Step 1: 環境準備（Develop + UT Phase 1）

- 分析環境需求
- 安裝必要的 SDK（Python/Node等）
- 建立虛擬環境（venv/virtualenv）
- 安裝專案依賴（requirements.txt / package.json）

### Step 2: 測試框架架設（Develop + UT Phase 1）

- 安裝測試框架（pytest / unittest / jest）
- 設定測試配置
- 建立測試目錄結構

### Step 3: UT 執行（Develop + UT Phase 1）

- 執行單元測試
- 收集測試結果
- 產出 UT 報告

---

## DevOps Agent 分工（v2）

| 方向 | 職責 | 目前優先 |
|------|------|----------|
| **Develop + UT** | 環境準備、套件管理、測試框架、UT 執行 | ✅ 目前專注 |
| **Publish + Deploy** | 部署、發布、CI/CD | ⏸ 以後再做 |

### Develop + UT 職責細項

| 項目 | 說明 |
|------|------|
| 環境準備 | 安裝 SDK、建立虛擬環境 |
| 套件管理 | requirements.txt / package.json |
| 測試框架 | 安裝並設定 pytest/unittest/jest |
| UT 執行 | 執行單元測試、產出報告 |
| 開發工具 | linter、formatter 設定 |

---

## 輸出位置

| 產出 | 位置 |
|------|------|
| 環境配置 | `.env` / `venv/` |
| 依賴清單 | `requirements.txt` / `package.json` |
| UT 報告 | `tests/report/` |
| 測試配置 | `pytest.ini` / `jest.config.js` |

## 模板位置

- Dockerfile 模板: `references/dockerfile-template.md`（Publish + Deploy 用）
- CI/CD 模板: `references/cicd-template.md`（Publish + Deploy 用）
- 環境設定模板: `references/dev-env-template.md`（新建）

## 規則位置

- 任務派工規範: `rules/task-dispatch-standards.md`