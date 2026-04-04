# Repository 和 Application 劃分原則

## 核心概念

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

---

## Repository 劃分原則

### 決定因素

| 因素 | 說明 |
|------|------|
| **團隊邊界** | 不同團隊負責不同 Repo |
| **部署頻率** | 需要獨立部署的拆開 |
| **技術多樣性** | 不同技術堆疊拆開 |
| **安全需求** | 敏感程式碼獨立管理 |
| **存取權限** | 不同Repo 不同權限 |

### 劃分策略

#### 策略 1: 按團隊劃分
```
Org: devpro-tw
├── repo: frontend-team
├── repo: backend-team
├── repo: infra-team
```

#### 策略 2: 按應用程式劃分（推薦）
```
Org: devpro-tw
├── repo: user-service
├── repo: order-service
├── repo: payment-service
├── repo: admin-frontend
├── repo: customer-frontend
```

#### 策略 3: 按層級劃分
```
Org: devpro-tw
├── repo: microservices-core
├── repo: microservices-business
├── repo: web-frontend
├── repo: mobile-app
```

---

## Application 劃分原則

### 定義

**Application** 可以是：
1. **可獨立部署的服務**（微服務架構）
2. **一個功能模組**（模組化單體）

### 選擇準則

| 條件 | 建議 |
|------|------|
| 需要獨立部署 | 拆為獨立 Application |
| 需要獨立擴展 | 拆為獨立 Application |
| 團隊需要獨立開發 | 拆為獨立 Application |
| 共享程式碼 | 放在 `shared/` 目錄 |

---

## 實際範例

### 電子商務平台

```
Project: E-commerce Platform
│
├── Repo: user-management
│   │
│   ├── Application: UserService
│   │   ├── requirements/
│   │   ├── architecture/
│   │   └── src/
│   │
│   ├── Application: AuthService
│   │   └── ...
│   │
│   └── shared/
│       └── common-contracts/
│
├── Repo: order-management
│   │
│   ├── Application: OrderService
│   │   └── ...
│   │
│   ├── Application: InventoryService
│   │   └── ...
│   │
│   └── shared/
│       └── order-contracts/
│
├── Repo: frontend
│   │
│   ├── Application: AdminPortal
│   │   └── ...
│   │
│   └── Application: CustomerWeb
│       └── ...
│
└── Repo: infrastructure
    │
    ├── Application: APIGateway
    ├── Application: MessageBus
    └── Application: Monitoring
```

---

## 依賴管理

### 原則

1. **同 Repo 內**：直接引用
2. **跨 Repo**：使用 Package Registry
   - NuGet (.NET)
   - npm (Node.js)
   - PyPI (Python)

### 版本策略

| 策略 | 適用情境 | 範例 |
|------|----------|------|
| **固定版本** | 測試環境 | 1.0.0 |
| **範圍版本** | 開發環境 | >=1.0.0 <2.0.0 |
| **浮動版本** | 生產環境 | 1.0.\* |

---

## 決策檢查清單

規劃 Repo 結構前，先回答：

- [ ] 團隊規模多大？
- [ ] 需要支援多少 concurrent deployments？
- [ ] 不同 Repo 的技術堆疊差異大嗎？
- [ ] 有敏感程式碼需要特別權限嗎？
- [ ] 部署頻率差異大嗎？
- [ ] 未来可能的變化？

根據答案選擇最適合的劃分策略。
