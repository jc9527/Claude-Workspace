# CI/CD Pipeline 模板

---

## GitHub Actions - .NET 專案

```yaml
name: .NET CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  DOTNET_VERSION: '8.0.x'

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: ${{ env.DOTNET_VERSION }}
    
    - name: Restore dependencies
      run: dotnet restore
    
    - name: Build
      run: dotnet build --no-restore --configuration Release
    
    - name: Run tests
      run: dotnet test --no-build --configuration Release --verbosity normal
    
    - name: Publish
      run: dotnet publish -c Release -o ./publish
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: publish
        path: ./publish

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Download artifacts
      uses: actions/download-artifact@v4
      with:
        name: publish
    
    - name: Deploy to server
      # 這裡替換為實際的部署指令
      run: |
        echo "Deploying to server..."
        # rsync or scp or docker commands

```

---

## GitHub Actions - Node.js 專案

```yaml
name: Node.js CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
    - name: Build
      run: npm run build
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: dist
        path: dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
```

---

## 部署檢查清單

### 部署前

- [ ] 所有測試通過
- [ ] Code Review 完成
- [ ] 文件已更新
- [ ] 資料庫 Migration 已準備
- [ ] 環境變數已設定
- [ ] Rollback 計畫已準備

### 部署中

- [ ] 監控部署過程
- [ ] 檢查 logs
- [ ] 驗證功能正常

### 部署後

- [ ] Smoke test 通過
- [ ] 確認效能正常
- [ ] 通知相關人員
- [ ] 更新專案狀態
