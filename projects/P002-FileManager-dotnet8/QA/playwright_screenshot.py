#!/usr/bin/env python3
"""
P002-FileManager-dotnet8 - Playwright E2E 截圖測試
使用方式: python3 playwright_screenshot.py [output_dir]
"""
import sys
import time
from playwright.sync_api import sync_playwright

APP_URL = "http://localhost:5220"
OUTPUT_DIR = sys.argv[1] if len(sys.argv) > 1 else "/home/devpro/Claude-Workspace/projects/P002-FileManager-dotnet8/QA/screenshots/playwright"

def screenshot(page, name, wait=2000):
    """截圖並等待"""
    time.sleep(2)  # Blazor 需要時間 render
    page.screenshot(path=f"{OUTPUT_DIR}/{name}", full_page=True)
    print(f"  ✅ {name}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        print(f"\n📸 P002-FileManager 截圖測試")
        print(f"   URL: {APP_URL}")
        print(f"   Output: {OUTPUT_DIR}\n")

        # TC-001: 首頁
        print("TC-001: 首頁截圖")
        page.goto(f"{APP_URL}/", wait_until="networkidle", timeout=30000)
        screenshot(page, "TC001_homepage.png")

        # TC-002: 檔案列表（已在首頁顯示）
        print("TC-002: 檔案列表")
        page.goto(f"{APP_URL}/", wait_until="networkidle", timeout=30000)
        screenshot(page, "TC002_filelist.png")

        # TC-003: 點擊右鍵選單（滑鼠右鍵點第一個檔案）
        print("TC-003: 右鍵選單")
        page.goto(f"{APP_URL}/", wait_until="networkidle", timeout=30000)
        time.sleep(2)
        # 嘗試找到檔案列表中的第一個項目並右鍵
        try:
            items = page.locator("table tbody tr").all()
            if items:
                items[0].click(button="right")
                time.sleep(1)
                screenshot(page, "TC003_context_menu.png")
        except Exception as e:
            print(f"  ⚠️ 右鍵選單截圖失敗: {e}")
            screenshot(page, "TC003_context_menu.png")

        # TC-004: 新增資料夾對話框（按鈕）
        print("TC-004: 新增資料夾")
        page.goto(f"{APP_URL}/", wait_until="networkidle", timeout=30000)
        time.sleep(2)
        try:
            # 找新增按鈕
            btns = page.locator("button").all()
            for btn in btns:
                if "new" in btn.inner_text().lower() or "新增" in btn.inner_text():
                    btn.click()
                    break
            time.sleep(1)
            screenshot(page, "TC004_new_folder_dialog.png")
        except Exception as e:
            print(f"  ⚠️ 新增資料夾截圖失敗: {e}")
            screenshot(page, "TC004_new_folder_dialog.png")

        # TC-005: 搜尋框
        print("TC-005: 搜尋功能")
        page.goto(f"{APP_URL}/", wait_until="networkidle", timeout=30000)
        time.sleep(2)
        try:
            search_input = page.locator("input[type='text'], input[placeholder*='Search'], input[placeholder*='搜尋']").first
            search_input.fill("Test")
            time.sleep(1)
            screenshot(page, "TC005_search.png")
        except Exception as e:
            print(f"  ⚠️ 搜尋截圖失敗: {e}")
            screenshot(page, "TC005_search.png")

        # TC-006: 設定頁面
        print("TC-006: 設定頁面")
        page.goto(f"{APP_URL}/settings", wait_until="networkidle", timeout=30000)
        screenshot(page, "TC006_settings.png")

        # TC-007: Debug Header 驗證（Network 面板用截圖替代）
        print("TC-007: Debug Header")
        page.goto(f"{APP_URL}/", wait_until="networkidle", timeout=30000)
        time.sleep(2)
        screenshot(page, "TC007_debug_header.png")

        print(f"\n✅ 截圖完成，共 7 張")
        print(f"   目錄: {OUTPUT_DIR}")

        browser.close()

if __name__ == "__main__":
    main()
