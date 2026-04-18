# Idea：P003 站台服務部署慣例 — FileStorage RootPath 設計

建立日期：2026-04-18

## 背景

`FileStorage:RootPath` 目前在 `appsettings.json` 寫死 `/home/devpro/data`。
已改為可設定，但預設值不適用於 Windows，且不符合站台服務部署慣例。

## Idea 內容

採用 ASP.NET Core 站台服務標準做法：

1. 預設值改為相對 `ContentRootPath` 的 `data` 子目錄（開發零設定可跑）
2. Production 透過環境變數 `FileStorage__RootPath` 覆蓋（不進 source code）
3. Linux systemd unit 設定 `Environment=FileStorage__RootPath=/var/lib/filemanager`
4. Windows IIS `web.config` 設定 `environmentVariable`

## 狀態

待 Plan 確認後實作
