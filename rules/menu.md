# Menu 功能規格

menu 是 Claude-Workspace 的快速導航指令，讓用戶快速存取常用的 Prompts、Plans 和 Scripts。

## 「menu」快捷行為

當使用者輸入 **「menu」** 時：

**預設（可執行路徑）**：AI **優先**自專案根目錄執行 `python3 scripts/menu.py`（必要時加 `--machine <電腦目錄>` 或設定環境變數 `CLAUDE_WORKSPACE_MACHINE`，見該腳本 `--help`）。若退出碼為 **0**，以 **stdout 全文**作為本次 menu（可簡短引言後附上）。

**例外（規範可能領先腳本）**：若 `rules/` 目錄內**任一檔案**的 **mtime 晚於** `scripts/menu.py` 的 mtime，則**不得**僅信賴腳本輸出，須改依下列第 1–7 點**手動組合** menu，並可在合理時機提醒將 `menu.py` 對齊新規範。

**失敗時**：`menu.py` 非 0 退出、找不到工作區根目錄、無法解析電腦目錄等，則**完全依**下列第 1–7 點手動組 menu。

---

1. **Prompts**：列出專案根目錄 `prompts/` 下**最新 3 個** `.md` 檔（依修改時間，新→舊）。每一筆除檔名外，須附**該檔目前修改時間**（`mtime`），格式與下項一致。
2. **Plans**：列出 `machines/<當前電腦目錄>/plans/` 下**最新 3 個** `.md` 檔（同上）；每一筆除檔名外，須附**該檔目前 `mtime`**。
3. **Scripts**：列出**最近執行紀錄**優先的 **3 個** `scripts/` 下 `.py`（相對路徑）。每一筆須附：**最近執行時間**（來自 `outputs/.menu-recent-scripts.json` 的 `last_run_at`；從未執行過則標 **—**）與**該檔目前修改時間**（列表當下對檔案 `stat` 的 `mtime`，UTC）。紀錄檔另會於每次 `record_run` 寫入當下之 `file_mtime_utc`（快照，供稽核）。排序規則不變：若**完全沒有**執行紀錄，改依腳本**建立時間**（`st_birthtime`，無效則 **mtime**）新→舊；若已有紀錄但不足 3 筆，缺額**依 mtime** 補滿。略過 `__init__.py`。
4. **時間格式**：同一次 menu 回覆內，上述時間一律使用 **UTC ISO**（例如 `2026-04-03T10:00:00Z`），三區一致。
5. **選項編號**：三組**連續編號**——Prompts 佔 1–3、Plans 佔 4–6、Scripts 佔 7–9；若某一組不足 3 個檔案，後續組從緊接的數字接續（例如 Prompts 僅 2 個時，Plans 自 3 開始）。
6. 使用者選定後：若為 **Prompts／Plans**，**讀取該檔**並執行其對應操作；若為 **Script**，依該腳本用途執行（例如 `python3 <路徑>` 並傳入合理參數）。**AI 責任**：在**實際執行**該 script 後，須寫入執行紀錄——與腳本內建方式相同：優先呼叫 `scripts/menu_state.py record <腳本路徑>`，或在可 `import menu_state` 時呼叫 `menu_state.record_run(該腳本之 __file__ 或絕對路徑)`，以免僅手動／代理執行時沒有留痕。
7. 實作參考：完整輸出見 `scripts/menu.py`；Scripts 排序與時間欄見 `scripts/menu_state.py`（`suggest_scripts_for_menu` 僅路徑；**需附時間欄**時用 `suggest_scripts_for_menu_rows`）。

若無法取得本機電腦名稱，可請使用者提供，或依使用者目前開啟路徑推斷 `machines/` 下對應子目錄並先確認。

## 目錄瀏覽功能

menu 除了列出 Prompts、Plans、Scripts 外，最後一個選項為「目錄瀏覽」。

### 操作流程
1. 用戶輸入 menu → 顯示原有選項 + 最後一項「📁 瀏覽 Workspace 目錄」
2. 用戶選擇該項 → 列出 Claude-Workspace 的第一層目錄（有編號），例如：
   ```
   📁 Workspace 目錄
   1. prompts/
   2. notes/
   3. machines/
   4. rules/
   5. scripts/
   6. outputs/
   0. ← 返回 menu
   ```
3. 用戶選一個目錄編號 → 列出該目錄下的檔案和子目錄（有編號），例如：
   ```
   📁 rules/
   1. README.md (1.2 KB)
   2. workspace.md (3.5 KB)
   3. prompts-and-scripts.md (2.1 KB)
   4. menu.md (1.8 KB)
   0. ← 返回上層
   ```
4. 用戶選一個檔案編號 → 讀取該檔案內容或執行（依副檔名判斷）
5. 選 0 返回上層，可層層退回到 menu

### 規則
- 只瀏覽 Claude-Workspace 目錄，不允許跳出
- 隱藏 .git/ 和 .claude/ 目錄
- 子目錄用 / 結尾標示，檔案顯示大小
- 0 永遠代表返回上層/返回 menu
