import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import shutil
import sys

# Force UTF-8 stdout on Windows
sys.stdout.reconfigure(encoding='utf-8')

auth_url = "https://s.salla.sa/auth/auto?access_token=eyJpdiI6Ii9YWG9UZnBVZmlYeDZscDN5aEpCN3c9PSIsInZhbHVlIjoieStFdXFSUnMzMVg5eTFwd0U2dEhjL3FwUlc5RTJIcExSbExxV21VWHJIcjg1RjNjcFZ1Ymg1amVDL3J4eU8yT2RaRnF5L0V6M3pINXZWQWVhWHBLOFE9PSIsIm1hYyI6Ijg4MDQzZmQ0YjZjOWFmYjM2MjZmMTk1MGQ0MTgyZjBkMWNhMTMxOGNlYjI4NTVkMTIxMWQyMGEzZGVlY2E4ODEiLCJ0YWciOiIifQ==&source=partners&url=https%3A%2F%2Fs.salla.sa%2Fdesign%2Fdraft-863961203%3Flegacy=0%26assets_url=http://localhost:8000%26ws_port=8001%26with_editor=false"

out_path = Path(r"C:\Users\DevUser\salla-twilight-luxury-pro\screenshots\live_salla_verified_preview.png")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 2800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        page.on("console", lambda msg: print(f"[Browser Console] {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"[Browser PageError]: {err}"))

        print("Navigating to auth URL...")
        try:
            response = await page.goto(auth_url, wait_until="domcontentloaded", timeout=30000)
            print(f"Initial Status: {response.status if response else 'No response'}")
        except Exception as e:
            print(f"Navigation warning: {e}")

        # Wait for page transitions, auth redirects, and iframe/storefront loading
        for i in range(12):
            await asyncio.sleep(1)
            print(f"[{i+1}s] Current URL: {page.url}")

        title = await page.title()
        print(f"Page Title: {title}")

        # If there are iframes (e.g. Salla editor embedding draft preview), check frames
        for idx, frame in enumerate(page.frames):
            print(f"Frame {idx}: name='{frame.name}', url='{frame.url}'")

        await page.screenshot(path=str(out_path), full_page=True)
        print(f"Screenshot saved to {out_path} ({out_path.stat().st_size} bytes)")

        # Copy to artifact directory
        artifact_dir = Path(r"C:\Users\DevUser\.gemini\antigravity-cli\brain\1fdd556b-d842-496b-a55d-0f5b8dacc716")
        if artifact_dir.exists():
            dest = artifact_dir / "live_salla_verified_preview.png"
            shutil.copyfile(out_path, dest)
            print(f"Copied to artifact dir: {dest}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
