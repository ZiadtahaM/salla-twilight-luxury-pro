import sys
import time
from playwright.sync_api import sync_playwright

def capture_preview(url, output_path):
    print(f"Navigating to: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception as e:
            print(f"Navigation warning: {e}")

        time.sleep(3)
        page.screenshot(path=output_path, full_page=True)
        print(f"Screenshot saved to: {output_path}")
        browser.close()

if __name__ == "__main__":
    url = sys.argv[1]
    out = sys.argv[2]
    capture_preview(url, out)
