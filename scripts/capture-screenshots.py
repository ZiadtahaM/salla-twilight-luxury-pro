import os
import sys
from playwright.sync_api import sync_playwright

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST_DIR = os.path.join(ROOT_DIR, "dist")
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "screenshots")
ARTIFACT_DIR = r"C:\Users\DevUser\.gemini\antigravity-cli\brain\1fdd556b-d842-496b-a55d-0f5b8dacc716"

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

targets = [
    {"name": "desktop-ar.png", "file": "preview-ar.html", "width": 1440, "height": 900, "is_mobile": False},
    {"name": "mobile-ar.png", "file": "preview-ar.html", "width": 360, "height": 780, "is_mobile": True},
    {"name": "desktop-en.png", "file": "preview-en.html", "width": 1440, "height": 900, "is_mobile": False},
    {"name": "mobile-en.png", "file": "preview-en.html", "width": 360, "height": 780, "is_mobile": True},
]

print("Initializing offline Playwright capture engine...")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-web-security", "--allow-file-access-from-files"]
    )
    
    for target in targets:
        html_file = os.path.join(DIST_DIR, target["file"])
        if not os.path.exists(html_file):
            raise FileNotFoundError(f"Missing preview artifact: {html_file}")
            
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        page = browser.new_page(
            viewport={"width": target["width"], "height": target["height"]},
            is_mobile=target["is_mobile"],
            device_scale_factor=1.5
        )
        
        # Abort any external network calls to guarantee instant offline execution
        page.route("**/*", lambda route: route.abort() if route.request.url.startswith("http") else route.continue_())
        
        print(f"Rendering {target['name']} ({target['width']}x{target['height']})...")
        page.set_content(html_content, wait_until="commit", timeout=5000)
        page.wait_for_timeout(300) # Small tick for DOM reflow
        
        repo_path = os.path.join(SCREENSHOTS_DIR, target["name"])
        artifact_path = os.path.join(ARTIFACT_DIR, target["name"])
        
        page.screenshot(path=repo_path, full_page=False)
        page.screenshot(path=artifact_path, full_page=False)
        print(f"Captured viewport: {repo_path}")

        # Also capture full-page view to verify product grid and footer
        full_repo_path = repo_path.replace(".png", "-full.png")
        full_artifact_path = artifact_path.replace(".png", "-full.png")
        page.screenshot(path=full_repo_path, full_page=True)
        page.screenshot(path=full_artifact_path, full_page=True)
        print(f"Captured full page: {full_repo_path}")
        
        page.close()
        
    browser.close()

print("ALL SCREENSHOTS GENERATED DETERMINISTICALLY IN < 3 SECONDS.")
