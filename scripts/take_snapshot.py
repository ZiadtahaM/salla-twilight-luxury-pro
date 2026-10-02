import subprocess
import os
from pathlib import Path
import shutil

repo_root = Path(__file__).resolve().parent.parent
html_path = repo_root / "screenshots" / "rendered_preview.html"
out_path = repo_root / "screenshots" / "luxury_storefront_snapshot.png"

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--window-size=1440,3200",
    f"--screenshot={out_path}",
    f"file:///{str(html_path.resolve()).replace('\\', '/')}"
]

print("Executing:", " ".join(cmd))
res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)

if out_path.exists():
    print(f"Success! Snapshot generated at {out_path} ({out_path.stat().st_size} bytes)")
    # Also copy to artifact directory for the assistant
    artifact_dir = Path(r"C:\Users\DevUser\.gemini\antigravity-cli\brain\1fdd556b-d842-496b-a55d-0f5b8dacc716")
    if artifact_dir.exists():
        dest = artifact_dir / "luxury_storefront_snapshot.png"
        shutil.copyfile(out_path, dest)
        print(f"Copied to artifact dir: {dest}")
else:
    print("Snapshot file was not created. Stdout/Stderr:")
    print("Stdout:", res.stdout)
    print("Stderr:", res.stderr)
