import os
import sys
from playwright.sync_api import sync_playwright

url = "https://s.salla.sa/auth/auto?access_token=eyJpdiI6ImJ4bmdQS1NrMU9sTTRtN1lIOE9iK0E9PSIsInZhbHVlIjoiYW9HQ2I0U3pvVmFTa0pKUlREOXMydG0xRDVGbVhFY2lHSE5OMldyYXpFU0dhNXFYM0dnL3JkSmpvR05IVG9CRklnalUzWUl6YlN0RnM5MndiajNnNkE9PSIsIm1hYyI6ImU0MzliNjI3OTQ5ODVhYjM4MWMyMGQzNDgzYWNkYWY3NmU0ZjI4NzkyYzQ0MWQyNDM2Y2UwZmMyYzdlNzk1OTIiLCJ0YWciOiIifQ==&source=partners&url=https%3A%2F%2Fs.salla.sa%2Fdesign%2Fdraft-226958633%3Flegacy=0%26assets_url=http://localhost:8000%26ws_port=8001%26with_editor=false"
output_path = r"C:\Users\DevUser\salla-twilight-luxury-pro\screenshots\salla-live-preview.png"
artifact_path = r"C:\Users\DevUser\.gemini\antigravity-cli\brain\1fdd556b-d842-496b-a55d-0f5b8dacc716\salla-live-preview.png"

print("Navigating to Salla Live Preview Session...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    try:
        response = page.goto(url, wait_until="load", timeout=20000)
        page.wait_for_timeout(4000)
        print("Final URL:", page.url)
        print("Status:", response.status if response else "No response")
        print("Title:", page.title())
        page.screenshot(path=output_path, full_page=False)
        page.screenshot(path=artifact_path, full_page=False)
        print("Saved screenshot to:", output_path)
    except Exception as e:
        print("Error during navigation:", e)
        page.screenshot(path=output_path, full_page=False)
        page.screenshot(path=artifact_path, full_page=False)
    finally:
        browser.close()
