"""
E2E Test Script for Contact Manager vB
Takes screenshots of List Page, Add Form, and Edit Form
"""

import asyncio
import os
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, 'screenshots')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 720})
        page = await context.new_page()
        
        base_url = 'http://localhost:5001'
        
        # EC-01: List Page Screenshot
        print("Taking screenshot: List Page...")
        await page.goto(f'{base_url}/')
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, 'list_page.png'), full_page=True)
        print(f"  -> Saved: {SCREENSHOT_DIR}/list_page.png")
        
        # EC-02: Add Form Screenshot
        print("Taking screenshot: Add Form...")
        await page.goto(f'{base_url}/add')
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, 'add_form.png'), full_page=True)
        print(f"  -> Saved: {SCREENSHOT_DIR}/add_form.png")
        
        # EC-03: Edit Form Screenshot
        print("Taking screenshot: Edit Form...")
        # First create a contact to edit
        await page.goto(f'{base_url}/')
        await page.wait_for_load_state('networkidle')
        
        # Get contact ID from page if exists
        contact_id = await page.evaluate('''() => {
            const firstRow = document.querySelector("tr[data-contact-id]");
            return firstRow ? firstRow.dataset.contactId : null;
        }''')
        
        if contact_id:
            await page.goto(f'{base_url}/edit/{contact_id}')
        else:
            # Create a contact first
            await page.goto(f'{base_url}/add')
            await page.fill('#name', 'Test User for Edit')
            await page.fill('#email', 'edit.test@example.com')
            await page.fill('#phone', '0999-888-777')
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(1000)
            
            # Go back to list and get the ID
            await page.goto(f'{base_url}/')
            await page.wait_for_load_state('networkidle')
            contact_id = await page.evaluate('''() => {
                const firstRow = document.querySelector("tr[data-contact-id]");
                return firstRow ? firstRow.dataset.contactId : null;
            }''')
            await page.goto(f'{base_url}/edit/{contact_id}')
        
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path=os.path.join(SCREENSHOT_DIR, 'edit_form.png'), full_page=True)
        print(f"  -> Saved: {SCREENSHOT_DIR}/edit_form.png")
        
        await browser.close()
        print("\nE2E Test completed successfully!")

if __name__ == '__main__':
    asyncio.run(main())
