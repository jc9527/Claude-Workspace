---
name: devops
description: 部署與 DevOps。當需要：
  (1) 建立 CI/CD Pipeline
  (2) 撰寫 Dockerfile
  (3) 設計部署架構
  (4) 建立監控和日誌
  使用此 Skill。
---

# DevOps Skill

## 觸發時機

- Developer 完成實作後
- 需要部署時
- 需要建立 CI/CD 時

## 前置輸入

- SystemArchitect 的部署架構
- 程式碼 Repository
- 環境需求

## 工作流程

### Step 1: 設計部署架構

- 設計容器化方案
- 設計 CI/CD Pipeline

### Step 2: 建立 Dockerfile

- 撰寫 Dockerfile
- 建立 docker-compose.yml

### Step 3: 建立 CI/CD

- 設定 GitHub Actions / GitLab CI
- 設定自動化測試
- 設定自動化部署

### Step 4: 建立監控

- 設定日誌收集
- 設定監控警示

## 輸出位置

| 產出 | 位置 |
|------|------|
| Dockerfile | `Dockerfile` |
| CI/CD | `.github/workflows/` |
| docker-compose | `docker-compose.yml` |
| 部署文件 | `deployment/` |

## 模板位置

- Dockerfile 模板: `references/dockerfile-template.md`
- CI/CD 模板: `references/cicd-template.md`
- 部署檢查清單: `references/deployment-checklist.md`
