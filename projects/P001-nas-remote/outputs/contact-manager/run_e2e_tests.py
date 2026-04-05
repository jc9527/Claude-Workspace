from playwright.sync_api import sync_playwright
import os

output_dir = "/home/devpro/Claude-Workspace/projects/P001-nas-remote/outputs/contact-manager"
timestamp = "20260405_1815"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    
    # TC-101: 列表頁載入
    page.goto("http://localhost:5000/")
    page.wait_for_load_state("networkidle")
    page.screenshot(path=f"{output_dir}/P001-E2E-101-list-{timestamp}.png")
    print("✅ P001-E2E-101: 列表頁截圖完成")
    
    # TC-102: 新增表單頁
    page.goto("http://localhost:5000/contacts/new")
    page.wait_for_load_state("networkidle")
    page.screenshot(path=f"{output_dir}/P001-E2E-102-new-{timestamp}.png")
    print("✅ P001-E2E-102: 新增表單截圖完成")
    
    # TC-103: 編輯表單頁
    page.goto("http://localhost:5000/contacts/new")
    page.wait_for_load_state("networkidle")
    page.fill("#nameInput", "測試")
    page.screenshot(path=f"{output_dir}/P001-E2E-103-edit-{timestamp}.png")
    print("✅ P001-E2E-103: 編輯表單截圖完成")
    
    browser.close()
    print("✅ 所有 E2E 截圖完成")