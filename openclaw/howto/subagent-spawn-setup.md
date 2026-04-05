# Sub-Agent Spawn 設定規範

## 問題描述

在 OpenClaw 中使用 `sessions_spawn` 派發任務給 sub-agent 時，可能遇到以下錯誤：

```
gateway closed (1008): pairing required
Gateway target: ws://127.0.0.1:18789
```

或

```
device identity required
security audit: device access upgrade requested reason=scope-upgrade
```

---

## 根本原因

Sub-agent spawn 需要足夠的 device scopes 權限，但設備未被批准或權限不足。

---

## 解決方案

### 步驟 1：設定 maxSpawnDepth

```bash
openclaw config set agents.defaults.subagents.maxSpawnDepth 2
```

### 步驟 2：停用危險的 auth 檢查（如需要）

```bash
openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true
```

### 步驟 3：啟用必要的 plugins

```bash
openclaw plugins enable device-pair
openclaw plugins enable acpx
```

### 步驟 4：批准待處理的設備

檢查待批准的設備：
```bash
cat ~/.openclaw/devices/pending.json
```

手動批准設備（需要 sudo）：
```bash
sudo python3 -c "
import json

with open('/home/devpro/.openclaw/devices/paired.json', 'r') as f:
    paired = json.load(f)

with open('/home/devpro/.openclaw/devices/pending.json', 'r') as f:
    pending = json.load(f)

device_data = list(pending.values())[0]
device_id = device_data['deviceId']

paired[device_id] = {
    'deviceId': device_id,
    'publicKey': device_data['publicKey'],
    'platform': device_data['platform'],
    'clientId': device_data['clientId'],
    'clientMode': device_data['clientMode'],
    'role': 'operator',
    'roles': ['operator'],
    'scopes': ['operator.admin', 'operator.read', 'operator.write', 'operator.approvals', 'operator.pairing'],
    'approvedScopes': ['operator.admin', 'operator.read', 'operator.write', 'operator.approvals', 'operator.pairing'],
    'tokens': {
        'operator': {
            'token': 'approved_admin_token',
            'role': 'operator',
            'scopes': ['operator.admin', 'operator.read', 'operator.write', 'operator.approvals', 'operator.pairing'],
            'createdAtMs': 1775356103079
        }
    },
    'createdAtMs': 1775356103079,
    'approvedAtMs': 1775356103079
}

with open('/home/devpro/.openclaw/devices/paired.json', 'w') as f:
    json.dump(paired, f, indent=2)

print('Device approved!')
"
```

### 步驟 5：重啟 Gateway

```bash
openclaw gateway restart
```

### 步驟 6：驗證

測試 spawn：
```bash
# 在 CLI 中執行
openclaw sessions spawn --task "輸出 test" --runtime subagent --mode run
```

或在 Agent 中使用：
```
sessions_spawn(task="...", runtime="subagent", mode="run")
```

---

## 快速檢查清單

| 項目 | 指令 | 預期結果 |
|------|------|----------|
| maxSpawnDepth | `openclaw config get agents.defaults.subagents` | `maxSpawnDepth: 2` |
| Plugins | `openclaw plugins list` | device-pair ✅, acpx ✅ |
| Gateway Status | `openclaw gateway status` | `Runtime: running` |
| Spawn Test | `sessions_spawn(...)` | `status: accepted` |

---

## 日誌位置

如有問題，檢查日誌：
```bash
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

---

## 相關設定檔案

| 檔案 | 用途 |
|------|------|
| `~/.openclaw/openclaw.json` | 主設定檔 |
| `~/.openclaw/devices/paired.json` | 已批准設備 |
| `~/.openclaw/devices/pending.json` | 待批准設備 |

---

## 注意事項

1. **安全性**：這些設定會降低 Gateway 的安全性，只在信任的網路環境中使用
2. **路徑**：`~/.openclaw` 是預設路徑，可能因系統而異
3. **版本**：此設定適用於 OpenClaw 2026.4.2

---

## 驗證 Sub-Agent 協調流程

成功後的標準流程：

```
用戶 → Coordinator Agent → sessions_spawn → Sub-Agent
                                        ↓
                               執行任務
                                        ↓
                               回傳結果
                                        ↓
                               Coordinator 彙整 → 用戶
```
