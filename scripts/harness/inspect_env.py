#!/usr/bin/env python3
"""
Salla Twilight Environment and CLI Inspector
Probes Salla CLI binary, OAuth configuration, registered theme IDs, and preview ports.
"""

import sys
import os
import re
import json
import socket
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


def check_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        result = s.connect_ex((host, port))
        return result == 0


class EnvironmentInspector:
    def __init__(self, theme_root: Path):
        self.theme_root = theme_root.resolve()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.checks_passed: List[str] = []
        self.details: Dict[str, Any] = {}

    def inspect_cli(self) -> None:
        try:
            res = subprocess.run(
                ["salla", "--version"],
                capture_output=True,
                text=True,
                check=False,
                shell=True,
            )
            output = (res.stdout + res.stderr).strip()
            # Match version like 3.2.56
            v_match = re.search(r"(\d+\.\d+\.\d+)", output)
            if v_match:
                version = v_match.group(1)
                self.checks_passed.append(f"Salla CLI installed: version {version}")
                self.details["cli_version"] = version
            else:
                self.warnings.append("Salla CLI executed but version number could not be parsed")
                self.details["cli_version"] = "unknown"
        except FileNotFoundError:
            self.errors.append("Salla CLI executable 'salla' not found in PATH")
            self.details["cli_version"] = None

    def inspect_oauth_config(self) -> None:
        config_path = Path.home() / ".salla" / "config.json"
        if not config_path.exists():
            self.errors.append(f"Salla CLI config file not found at {config_path}")
            self.details["authenticated"] = False
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            salla_data = data.get("salla", {})
            has_token = bool(salla_data.get("access_token"))
            user_data = salla_data.get("user", {})
            user_email = user_data.get("email") or "unknown"

            if has_token:
                self.checks_passed.append(f"Salla CLI authenticated as user: {user_email}")
                self.details["authenticated"] = True
                self.details["user_email"] = user_email
            else:
                self.errors.append("Salla CLI config exists but access_token is missing. Run 'salla login'.")
                self.details["authenticated"] = False
        except Exception as exc:
            self.errors.append(f"Failed to read Salla config file: {exc}")
            self.details["authenticated"] = False

    def inspect_theme_list(self) -> None:
        try:
            res = subprocess.run(
                ["salla", "theme", "list"],
                capture_output=True,
                text=True,
                check=False,
                shell=True,
            )
            raw_output = res.stdout + res.stderr
            # Strip ANSI escape sequences
            clean_output = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", raw_output)

            # Match lines with theme data: digit ID, name, status
            # Example: │ 1252059893  │ Luxury Pro Bespoke           │ development   │
            theme_matches = re.findall(
                r"[│|]\s*(\d{5,})\s*[│|]\s*([^│|]+?)\s*[│|]\s*([^│|]+?)\s*[│|]", clean_output
            )
            themes: List[Dict[str, str]] = []
            for tid, tname, tstatus in theme_matches:
                themes.append({
                    "id": tid.strip(),
                    "name": tname.strip(),
                    "status": tstatus.strip(),
                })

            self.details["registered_themes"] = themes
            if themes:
                self.checks_passed.append(f"Found {len(themes)} registered theme(s) in Partners account")
                for t in themes:
                    self.checks_passed.append(f"  Theme ID: {t['id']} | Name: {t['name']} | Status: {t['status']}")
            else:
                self.warnings.append("No themes detected from 'salla theme list' output")
        except Exception as exc:
            self.errors.append(f"Error querying 'salla theme list': {exc}")

    def inspect_preview_ports(self) -> None:
        p8000 = check_port_in_use(8000)
        p8001 = check_port_in_use(8001)

        self.details["ports"] = {
            "8000_in_use": p8000,
            "8001_in_use": p8001,
        }

        if p8000 and p8001:
            self.checks_passed.append("Ports 8000 (asset server) and 8001 (ws) are ACTIVE (Preview daemon running)")
            self.details["preview_daemon_active"] = True
        elif not p8000 and not p8001:
            self.checks_passed.append("Ports 8000 and 8001 are free (Ready to start preview daemon)")
            self.details["preview_daemon_active"] = False
        else:
            self.warnings.append(
                f"Partial port conflict: Port 8000 in_use={p8000}, Port 8001 in_use={p8001}"
            )
            self.details["preview_daemon_active"] = False

    def run(self) -> Tuple[bool, Dict[str, Any]]:
        self.inspect_cli()
        self.inspect_oauth_config()
        self.inspect_theme_list()
        self.inspect_preview_ports()

        is_valid = len(self.errors) == 0
        summary = {
            "valid": is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "passed_checks": self.checks_passed,
            "details": self.details,
        }
        return is_valid, summary


def main():
    root = Path.cwd()
    if len(sys.argv) > 1:
        root = Path(sys.argv[1])

    inspector = EnvironmentInspector(root)
    valid, summary = inspector.run()

    print("=" * 60)
    print(" SALLA TWILIGHT ENVIRONMENT AND CLI INSPECTOR")
    print("=" * 60)

    if summary["passed_checks"]:
        print(f"Passed Checks ({len(summary['passed_checks'])}):")
        for check in summary["passed_checks"]:
            print(f"  [PASS] {check}")
        print()

    if summary["warnings"]:
        print(f"Warnings ({len(summary['warnings'])}):")
        for w in summary["warnings"]:
            print(f"  [WARN] {w}")
        print()

    if summary["errors"]:
        print(f"Errors ({len(summary['errors'])}):")
        for err in summary["errors"]:
            print(f"  [FAIL] {err}")
        print()
        print("Verdict: REJECTED (Environment inspection failed)")
        sys.exit(1)
    else:
        print("Verdict: PASSED (Environment inspection succeeded)")
        sys.exit(0)


if __name__ == "__main__":
    main()
