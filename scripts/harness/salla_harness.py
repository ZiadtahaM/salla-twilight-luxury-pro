#!/usr/bin/env python3
"""
Salla Twilight Unified Verification Harness
Orchestrates static analysis, asset compilation, environment inspection, and git synchronization.
Evaluates the 7-Tier Salla Readiness Matrix.
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, List

# Import local harness modules
from validate_theme import ThemeValidator
from inspect_env import EnvironmentInspector
from check_git import GitSyncChecker


class SallaHarness:
    def __init__(self, theme_root: Path):
        self.theme_root = theme_root.resolve()

    def run_validate(self) -> Dict[str, Any]:
        validator = ThemeValidator(self.theme_root)
        valid, summary = validator.run()
        return summary

    def run_build(self) -> Dict[str, Any]:
        public_dir = self.theme_root / "public"
        errors: List[str] = []
        checks_passed: List[str] = []

        try:
            res = subprocess.run(
                ["pnpm", "run", "production"],
                cwd=str(self.theme_root),
                capture_output=True,
                text=True,
                check=False,
                shell=True,
            )
            if res.returncode != 0:
                errors.append(f"Build command failed with code {res.returncode}:\n{res.stderr or res.stdout}")
            else:
                checks_passed.append("pnpm run production succeeded (exit code 0)")
        except Exception as exc:
            errors.append(f"Failed to execute build command: {exc}")

        # Check required compiled outputs
        required_assets = ["app.css", "app.js"]
        for asset in required_assets:
            p = public_dir / asset
            if not p.exists():
                errors.append(f"Required compiled asset missing: public/{asset}")
            elif p.stat().st_size == 0:
                errors.append(f"Required compiled asset is empty: public/{asset}")
            else:
                size_kb = round(p.stat().st_size / 1024, 1)
                checks_passed.append(f"Compiled asset public/{asset} present ({size_kb} KB)")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": [],
            "passed_checks": checks_passed,
        }

    def run_env(self) -> Dict[str, Any]:
        inspector = EnvironmentInspector(self.theme_root)
        valid, summary = inspector.run()
        return summary

    def run_git(self) -> Dict[str, Any]:
        checker = GitSyncChecker(self.theme_root)
        valid, summary = checker.run()
        return summary

    def evaluate_matrix(
        self,
        val_res: Dict[str, Any],
        build_res: Dict[str, Any],
        env_res: Dict[str, Any],
        git_res: Dict[str, Any],
    ) -> Dict[str, Any]:
        # Check human/browser verification evidence file if present
        evidence_file = self.theme_root / ".scratch" / "salla-harness" / "store_verified.json"
        store_verified = False
        evidence_meta = {}
        if evidence_file.exists():
            try:
                with open(evidence_file, "r", encoding="utf-8") as f:
                    evidence_meta = json.load(f)
                    store_verified = evidence_meta.get("verified", False)
            except Exception:
                pass

        registered_themes = env_res.get("details", {}).get("registered_themes", [])
        theme_registered = len(registered_themes) > 0
        preview_active = env_res.get("details", {}).get("preview_daemon_active", False)

        matrix = {
            "1_SYNTAX_VALID": {
                "status": "PASS" if val_res.get("valid") else "FAIL",
                "description": "twilight.json, component files, and Twig hooks pass static analysis",
            },
            "2_ASSETS_BUILT": {
                "status": "PASS" if build_res.get("valid") else "FAIL",
                "description": "Production assets compiled into public/app.css and public/app.js",
            },
            "3_GIT_SYNCED": {
                "status": "PASS" if git_res.get("valid") and not git_res.get("warnings") else "WARN" if git_res.get("valid") else "FAIL",
                "description": "Local main branch is clean and synchronized with origin/main",
            },
            "4_CLI_AUTHENTICATED": {
                "status": "PASS" if env_res.get("details", {}).get("authenticated") else "FAIL",
                "description": "Salla CLI authenticated via OAuth config",
            },
            "5_THEME_REGISTERED": {
                "status": "PASS" if theme_registered else "FAIL",
                "description": "Theme ID recognized in Salla Partners Portal",
            },
            "6_PREVIEW_READY": {
                "status": "PASS" if not env_res.get("errors") else "FAIL",
                "description": "Streaming preview environment ports and prerequisites ready",
            },
            "7_STORE_VERIFIED": {
                "status": "PASS" if store_verified else "PENDING_CONFIRMATION",
                "description": "Custom components verified rendering in active demo store visual editor",
                "evidence": evidence_meta,
            },
        }

        # Calculate overall verdict
        core_pass = (
            matrix["1_SYNTAX_VALID"]["status"] == "PASS"
            and matrix["2_ASSETS_BUILT"]["status"] == "PASS"
            and matrix["4_CLI_AUTHENTICATED"]["status"] == "PASS"
            and matrix["5_THEME_REGISTERED"]["status"] == "PASS"
        )

        overall_status = "READY_FOR_PREVIEW" if core_pass and not store_verified else "STORE_CONFIRMED" if core_pass and store_verified else "INCOMPLETE"

        return {
            "overall_status": overall_status,
            "matrix": matrix,
            "validation": val_res,
            "build": build_res,
            "env": env_res,
            "git": git_res,
        }


def format_text_report(report: Dict[str, Any]) -> str:
    lines = []
    lines.append("=" * 66)
    lines.append(" SALLA TWILIGHT SEVEN-TIER VERIFICATION MATRIX")
    lines.append("=" * 66)
    lines.append("")

    matrix = report.get("matrix", {})
    for tier, info in sorted(matrix.items()):
        status = info.get("status")
        desc = info.get("description")
        mark = "[PASS]" if status == "PASS" else "[WARN]" if status == "WARN" else "[PENDING]" if status == "PENDING_CONFIRMATION" else "[FAIL]"
        lines.append(f"{mark:<10} {tier:<20} {desc}")

    lines.append("")
    lines.append("-" * 66)
    overall = report.get("overall_status")
    lines.append(f"Overall Platform Status: {overall}")
    if overall == "READY_FOR_PREVIEW":
        lines.append("Next Step: Run 'salla theme preview -e' and confirm components in Salla Theme Editor.")
    elif overall == "STORE_CONFIRMED":
        lines.append("Next Step: Theme is ready for marketplace publication (salla theme publish).")
    lines.append("-" * 66)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Salla Twilight Verification Harness")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "validate", "build", "env", "git-sync"])
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    parser.add_argument("--skip-build", action="store_true", help="Skip running production build during status evaluation")
    args = parser.parse_args()

    harness = SallaHarness(Path.cwd())

    if args.command == "validate":
        res = harness.run_validate()
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            for check in res.get("passed_checks", []):
                print(f"[PASS] {check}")
            for err in res.get("errors", []):
                print(f"[FAIL] {err}")
        sys.exit(0 if res.get("valid") else 1)

    elif args.command == "build":
        res = harness.run_build()
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            for check in res.get("passed_checks", []):
                print(f"[PASS] {check}")
            for err in res.get("errors", []):
                print(f"[FAIL] {err}")
        sys.exit(0 if res.get("valid") else 1)

    elif args.command == "env":
        res = harness.run_env()
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            for check in res.get("passed_checks", []):
                print(f"[PASS] {check}")
            for err in res.get("errors", []):
                print(f"[FAIL] {err}")
        sys.exit(0 if res.get("valid") else 1)

    elif args.command == "git-sync":
        res = harness.run_git()
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            for check in res.get("passed_checks", []):
                print(f"[PASS] {check}")
            for err in res.get("errors", []):
                print(f"[FAIL] {err}")
        sys.exit(0 if res.get("valid") else 1)

    elif args.command == "status":
        val_res = harness.run_validate()
        if args.skip_build:
            # Check public assets without running full build
            public_dir = harness.theme_root / "public"
            has_css = (public_dir / "app.css").exists()
            has_js = (public_dir / "app.js").exists()
            build_res = {
                "valid": has_css and has_js,
                "errors": [] if has_css and has_js else ["Missing compiled assets in public/"],
                "warnings": ["Skipped active build via --skip-build flag"],
                "passed_checks": ["Existing public/app.css and public/app.js detected"],
            }
        else:
            build_res = harness.run_build()

        env_res = harness.run_env()
        git_res = harness.run_git()

        report = harness.evaluate_matrix(val_res, build_res, env_res, git_res)

        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(format_text_report(report))

        sys.exit(0 if report.get("overall_status") in ["READY_FOR_PREVIEW", "STORE_CONFIRMED"] else 1)


if __name__ == "__main__":
    main()
