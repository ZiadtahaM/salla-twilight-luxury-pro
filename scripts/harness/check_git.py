#!/usr/bin/env python3
"""
Salla Twilight Git Synchronization Checker
Verifies local working tree status, active branch, and parity with remote origin.
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Tuple


class GitSyncChecker:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.checks_passed: List[str] = []
        self.details: Dict[str, Any] = {}

    def run_git(self, args: List[str]) -> Tuple[int, str]:
        res = subprocess.run(
            ["git"] + args,
            cwd=str(self.repo_root),
            capture_output=True,
            text=True,
            check=False,
        )
        return res.returncode, (res.stdout + res.stderr).strip()

    def check_branch(self) -> None:
        code, out = self.run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        if code != 0:
            self.errors.append(f"Failed to determine current git branch: {out}")
            self.details["branch"] = None
        else:
            self.details["branch"] = out
            self.checks_passed.append(f"Current git branch is '{out}'")

    def check_remote_url(self) -> None:
        code, out = self.run_git(["config", "--get", "remote.origin.url"])
        if code != 0 or not out:
            self.errors.append("Git remote 'origin' is not configured")
            self.details["remote_url"] = None
        else:
            self.details["remote_url"] = out
            self.checks_passed.append(f"Git remote origin: {out}")

    def check_clean_working_tree(self) -> None:
        code, out = self.run_git(["status", "--porcelain"])
        if code != 0:
            self.errors.append(f"Failed to check git status: {out}")
            return

        lines = [l for l in out.splitlines() if l.strip()]
        # Separate tracked modified vs untracked
        modified_tracked = [l for l in lines if not l.startswith("??")]
        untracked = [l for l in lines if l.startswith("??")]

        self.details["modified_tracked"] = modified_tracked
        self.details["untracked_count"] = len(untracked)

        if modified_tracked:
            self.warnings.append(
                f"Working tree has {len(modified_tracked)} modified tracked files not committed"
            )
        else:
            self.checks_passed.append("Working tree has zero uncommitted modifications to tracked files")

    def check_remote_parity(self) -> None:
        # Check if remote tracking exists
        code, upstream = self.run_git(["rev-parse", "--abbrev-ref", "@{u}"])
        if code != 0:
            self.warnings.append("No upstream branch configured for active branch")
            return

        # Check commits ahead
        code_ahead, out_ahead = self.run_git(["rev-list", "--count", f"{upstream}..HEAD"])
        ahead_count = int(out_ahead) if code_ahead == 0 and out_ahead.isdigit() else 0

        # Check commits behind
        code_behind, out_behind = self.run_git(["rev-list", "--count", f"HEAD..{upstream}"])
        behind_count = int(out_behind) if code_behind == 0 and out_behind.isdigit() else 0

        self.details["ahead"] = ahead_count
        self.details["behind"] = behind_count

        if ahead_count > 0:
            self.warnings.append(
                f"Local branch is ahead of {upstream} by {ahead_count} commit(s). Remember to run 'git push' so Salla Partners receives updates."
            )
        else:
            self.checks_passed.append(f"Local branch is in sync with {upstream} (0 commits ahead)")

        if behind_count > 0:
            self.warnings.append(
                f"Local branch is behind {upstream} by {behind_count} commit(s). Pull remote changes."
            )

    def run(self) -> Tuple[bool, Dict[str, Any]]:
        self.check_branch()
        self.check_remote_url()
        self.check_clean_working_tree()
        self.check_remote_parity()

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

    checker = GitSyncChecker(root)
    valid, summary = checker.run()

    print("=" * 60)
    print(" SALLA TWILIGHT GIT SYNCHRONIZATION CHECKER")
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
        print("Verdict: REJECTED (Git sync failed)")
        sys.exit(1)
    else:
        print("Verdict: PASSED (Git sync succeeded)")
        sys.exit(0)


if __name__ == "__main__":
    main()
