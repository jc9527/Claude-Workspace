---
name: system-designer
description: 系統詳細設計。當需要：
  (1) 設計 API 規格（RESTful / GraphQL）
  (2) 設計資料庫 Schema
  (3) 設計 UI 頁面（欄位、按鍵功能）
  (4) 繪製類圖或時序圖
  (5) 定義介面規格
  使用此 Skill。
---

# System Designer Skill

## 觸發時機

- SystemArchitect 完成 System Architecture 後
- 需要實作詳細設計時
- 需要定義 API 介面時
- 需要設計 UI 畫面時

## 前置輸入

- SystemArchitect 產出的 System Architecture Document
- Application 清單（每個 Application 的類型：Web/WinForm/Console/API）
- User Stories 和 Use Cases

## 工作流程

### Step 1: 分析需求

- 理解 System Architecture
- 理解每個 Application 的目標
- 理解 User Stories 和 Use Cases

### Step 2: API 設計（針對 API Service）

- 定義 Endpoint
- 設計 Request/Response 格式
- 定義錯誤碼
- 設計驗證規則

### Step 3: UI 設計（針對 Web/WinForm）

- 設計頁面結構
- 定義欄位
- 定義按鍵功能
- 定義狀態（正常、錯誤、loading）

### Step 4: 資料庫設計

- 設計 Table Schema
- 定義欄位和類型
- 設計索引
- 定義關聯

### Step 5: 類圖 / 時序圖

- 繪製類圖
- 繪製時序圖

## 輸出位置

| 產出 | 位置 |
|------|------|
| API 規格 | `architecture/api-design/` |
| UI 設計 | `architecture/ui-design/` |
| 資料庫設計 | `architecture/database/` |

## 模板位置

- API 設計模板: `references/api-design-template.md`
- UI 設計模板: `references/ui-design-template.md`
- 資料庫設計模板: `references/database-design-template.md`
- 類圖指南: `references/class-diagram-guide.md`
- 時序圖指南: `references/sequence-diagram-guide.md`
