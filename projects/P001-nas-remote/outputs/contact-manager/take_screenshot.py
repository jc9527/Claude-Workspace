from playwright.sync_api import sync_playwright
import os

output_dir = "/home/devpro/Claude-Workspace/projects/P001-nas-remote/outputs/contact-manager"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    
    # Take screenshot of main page
    page.goto("http://localhost:5000/")
    page.wait_for_load_state("networkidle")
    page.screenshot(path=f"{output_dir}/test_screenshot_01_list.png")
    print("📸 Screenshot 01: List page")
    
    # Test adding contact page
    page.goto("http://localhost:5000/contacts/new")
    page.wait_for_load_state("networkidle")
    page.screenshot(path=f"{output_dir}/test_screenshot_02_add_form.png")
    print("📸 Screenshot 02: Add form page")
    
    browser.close()
    print("✅ Screenshots taken")