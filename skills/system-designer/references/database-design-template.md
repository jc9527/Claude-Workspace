# 資料庫設計模板

---

## 基本格式

```markdown
# [系統名稱] 資料庫設計

**資料庫類型**：[SQL Server / PostgreSQL / MySQL / MongoDB]
**版本**：v1.0
**說明**：[資料庫設計描述]

---

## Naming Conventions

| 類型 | 命名規則 | 範例 |
|------|----------|------|
| Table | PascalCase, 單數名詞 | Member, OrderDetail |
| Column | PascalCase | MemberName, CreatedAt |
| Primary Key | {TableName}Id | MemberId, OrderId |
| Foreign Key | {ReferencedTableName}Id | MemberId |
| Index | IX_{TableName}_{ColumnName} | IX_Member_Email |
| Unique Index | UX_{TableName}_{ColumnName} | UX_Member_Email |

---

## 資料表設計

### Table: [表格名稱]

| # | 欄位名稱 | 資料類型 | 主鍵 | 外鍵 | 必填 | 預設值 | 說明 |
|---|----------|----------|------|------|------|--------|------|
| 1 | | | PK | | 是 | | |
| 2 | | | | FK | 是 | | |
| 3 | | | | | 是 | | |
| 4 | | | | | 否 | | |

### 欄位類型對照

| C# 類型 | SQL Server | PostgreSQL | MySQL |
|----------|------------|------------|-------|
| int | INT | INTEGER | INT |
| long | BIGINT | BIGINT | BIGINT |
| string | NVARCHAR(MAX) | TEXT | VARCHAR(255) |
| string(50) | NVARCHAR(50) | VARCHAR(50) | VARCHAR(50) |
| decimal | DECIMAL(18,2) | DECIMAL(18,2) | DECIMAL(18,2) |
| DateTime | DATETIME2 | TIMESTAMP | DATETIME |
| bool | BIT | BOOLEAN | TINYINT(1) |
| Guid | UNIQUEIDENTIFIER | UUID | CHAR(36) |

---

## 關聯圖

```
┌─────────────┐       ┌─────────────┐
│   Member    │       │    Order    │
├─────────────┤       ├─────────────┤
│ MemberId (PK)│──┐   │ OrderId (PK)│
│ MemberName  │  │   │ MemberId(FK)│←─┘
│ Email       │      │ TotalAmount │
└─────────────┘      └─────────────┘
```

---

## 索引設計

### Table: [表格名稱]

| # | 索引名稱 | 類型 | 欄位 | 唯一 | 說明 |
|---|----------|------|------|------|------|
| 1 | PK_[TableName] | Clustered | Id | 是 | 主鍵索引 |
| 2 | IX_[TableName]_[Column] | Non-Clustered | Column | 否 | 一般索引 |
| 3 | UX_[TableName]_[Column] | Non-Clustered | Column | 是 | 唯一索引 |

---

## 約束條件

| # | 約束名稱 | 類型 | 欄位 | 條件 |
|---|----------|------|------|------|
| 1 | CK_[TableName]_[Column] | Check | Status | IN ('Active', 'Inactive') |
| 2 | DF_[TableName]_[Column] | Default | CreatedAt | GETDATE() |

---

## 範例：會員管理系統

### Table: Members

| # | 欄位名稱 | 資料類型 | 主鍵 | 外鍵 | 必填 | 預設值 | 說明 |
|---|----------|----------|------|------|------|--------|------|
| 1 | MemberId | UNIQUEIDENTIFIER | PK | | 是 | NEWID() | 會員 ID |
| 2 | MemberName | NVARCHAR(100) | | | 是 | | 會員名稱 |
| 3 | Email | NVARCHAR(255) | | | 是 | | Email |
| 4 | PasswordHash | NVARCHAR(MAX) | | | 是 | | 密碼雜湊 |
| 5 | Phone | NVARCHAR(20) | | | 否 | | 電話 |
| 6 | Status | NVARCHAR(20) | | | 是 | 'Active' | 狀態 |
| 7 | CreatedAt | DATETIME2 | | | 是 | GETDATE() | 建立時間 |
| 8 | UpdatedAt | DATETIME2 | | | 是 | GETDATE() | 更新時間 |

### Table: Orders

| # | 欄位名稱 | 資料類型 | 主鍵 | 外鍵 | 必填 | 預設值 | 說明 |
|---|----------|----------|------|------|------|--------|------|
| 1 | OrderId | UNIQUEIDENTIFIER | PK | | 是 | NEWID() | 訂單 ID |
| 2 | MemberId | UNIQUEIDENTIFIER | | FK(Members) | 是 | | 會員 ID |
| 3 | OrderDate | DATETIME2 | | | 是 | GETDATE() | 訂單日期 |
| 4 | TotalAmount | DECIMAL(18,2) | | | 是 | 0 | 總金額 |
| 5 | Status | NVARCHAR(20) | | | 是 | 'Pending' | 狀態 |
| 6 | CreatedAt | DATETIME2 | | | 是 | GETDATE() | 建立時間 |

### 關聯圖

```
┌─────────────┐       ┌─────────────┐
│   Members   │       │   Orders    │
├─────────────┤       ├─────────────┤
│ MemberId (PK)│──┐   │ OrderId (PK)│
│ MemberName  │  │   │ MemberId(FK)│←─┘
│ Email       │      │ TotalAmount │
└─────────────┘      └─────────────┘
```

---

## 設計檢查清單

- [ ] Table 命名符合規範？
- [ ] Column 命名符合規範？
- [ ] 主鍵都有設定？
- [ ] 外鍵關聯正確？
- [ ] 必填欄位都有標記？
- [ ] 適合的資料類型？
- [ ] 索引設計合理？
- [ ] 估計資料筆數和成長率？
