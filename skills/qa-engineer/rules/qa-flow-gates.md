# QA Flow Gates（強制關卡）

每個 Gate 必須通過才能進入下一階段。**禁止跳關。**

---

## Gate 1：test_cases 建立完成 → 才能寫腳本

### 通過條件
- [ ] `QA/test_cases/{功能ID}/description.md` 已建立
- [ ] description.md 包含：功能說明、測試案例清單（含正向/負向/邊界）、預期結果
- [ ] 已取得龍哥確認（口頭或文字）

### 禁止行為
- ❌ 未建立 description.md 就直接寫測試腳本
- ❌ 未列測試案例就開始執行

---

## Gate 2：腳本驗證完成 → 才能執行

### 通過條件
- [ ] 腳本命名符合規則：`p003_test_v{版本}_{功能}.py`
- [ ] `python3 -m py_compile {腳本}` 無語法錯誤
- [ ] 腳本內的測試案例 ID 與 description.md 對應一致

### 禁止行為
- ❌ 腳本有語法錯誤就執行
- ❌ 腳本測試案例與 description.md 不一致

---

## Gate 3：結果記錄完成 → 才算結案

### 通過條件
- [ ] 執行結果寫入 `QA/TestV{版本}-{功能}-{日期}-R{輪次}/results.json`
- [ ] description.md 的「實際結果」與「狀態判定」已更新
- [ ] FAIL 案例已開立 Bug 回報（含錯誤描述、判斷原因、期望結果、Trace ID）

### 禁止行為
- ❌ 有 FAIL 未開 Bug 就關閉測試
- ❌ description.md 未更新實際結果就回報完成

---

## 執行順序總覽

```
[需求/新功能]
      ↓
[Gate 1] 建立 test_cases/{ID}/description.md → 龍哥確認
      ↓
[Gate 2] 撰寫腳本 → 語法驗證 → 案例 ID 對應
      ↓
[Gate 3] 執行腳本 → 寫入結果 → 更新 description.md
      ↓
[完成]
```

---

*最後更新：2026-04-18*
