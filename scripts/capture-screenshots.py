import os
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST_DIR = os.path.join(ROOT_DIR, "dist")
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "screenshots")
ARTIFACT_DIR = r"C:\Users\DevUser\.gemini\antigravity-cli\brain\1fdd556b-d842-496b-a55d-0f5b8dacc716"

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

class StaticHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)

    def log_message(self, format, *args):
        pass # Silence logging

PORT = 8999
httpd = HTTPServer(("127.0.0.1", PORT), StaticHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"Local static server listening at http://127.0.0.1:{PORT}")

targets = [
    {"name": "desktop-ar.png", "path": "preview-ar.html", "width": 1440, "height": 900, "is_mobile": False},
    {"name": "mobile-ar.png", "path": "preview-ar.html", "width": 360, "height": 780, "is_mobile": True},
    {"name": "desktop-en.png", "path": "preview-en.html", "width": 1440, "height": 900, "is_mobile": False},
    {"name": "mobile-en.png", "path": "preview-en.html", "width": 360, "height": 780, "is_mobile": True},
]

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for target in targets:
            page = browser.new_page(
                viewport={"width": target["width"], "height": target["height"]},
                is_mobile=target["is_mobile"],
                device_scale_factor=1.5
            )
            url = f"http://127.0.0.1:{PORT}/{target['path']}"
            print(f"Capturing {target['name']} from {url}...")
            page.goto(url, wait_until="domcontentloaded", timeout=10000)
            page.wait_for_timeout(1500) # Give Tailwind and fonts time to paint
            
            repo_path = os.path.join(SCREENSHOTS_DIR, target["name"])
            artifact_path = os.path.join(ARTIFACT_DIR, target["name"])
            
            page.screenshot(path=repo_path, full_page=False)
            page.screenshot(path=artifact_path, full_page=False)
            print(f"Saved: {repo_path}")
            page.close()
        browser.close()
finally:
    httpd.shutdown()

print("ALL SCREENSHOTS CAPTURED SUCCESSFULLY.")
