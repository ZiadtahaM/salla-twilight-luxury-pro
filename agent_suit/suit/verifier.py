"""
Verifier — boolean predicates over observable state.

The core differentiator: every mission ends here. No vibes. No "looks good."
If you can't write a Check, the mission isn't ready.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Any
from .worklog import Worklog


@dataclass
class Check:
    name: str
    predicate: Callable[[dict], bool]
    detail_on_fail: str = ""

    def run(self, state: dict) -> "CheckResult":
        try:
            passed = bool(self.predicate(state))
        except Exception as e:
            return CheckResult(self.name, False, f"check raised {type(e).__name__}: {e}")
        return CheckResult(self.name, passed, "" if passed else self.detail_on_fail)


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


class Verifier:
    """Runs a battery of checks against a state dict. Returns all-or-nothing verdict."""

    def __init__(self, checks: list[Check]):
        self.checks = checks

    def run(self, state: dict, worklog: Worklog | None = None) -> tuple[bool, list[CheckResult]]:
        results = [c.run(state) for c in self.checks]
        all_passed = all(r.passed for r in results)
        if worklog:
            for r in results:
                worklog.verify(r.passed, f"{r.name}: {r.detail}" if not r.passed else f"{r.name}: ok")
        return all_passed, results

    # ---- factories for common checks ----
    @staticmethod
    def file_exists(path: str, label: str | None = None) -> Check:
        from pathlib import Path
        return Check(
            name=label or f"file_exists:{path}",
            predicate=lambda s: Path(s.get(path, "")).exists(),
            detail_on_fail=f"{path} must exist on disk",
        )

    @staticmethod
    def key_equals(key: str, expected: Any) -> Check:
        return Check(
            name=f"{key}=={expected!r}",
            predicate=lambda s: s.get(key) == expected,
            detail_on_fail=f"state[{key!r}] must equal {expected!r}",
        )

    @staticmethod
    def key_in(key: str, choices: list) -> Check:
        return Check(
            name=f"{key}∈{choices}",
            predicate=lambda s: s.get(key) in choices,
            detail_on_fail=f"state[{key!r}] must be one of {choices}",
        )

    @staticmethod
    def regex_in(key: str, pattern: str) -> Check:
        import re
        rx = re.compile(pattern)
        return Check(
            name=f"regex({key})~/{pattern}/",
            predicate=lambda s: bool(rx.search(str(s.get(key, "")))),
            detail_on_fail=f"state[{key!r}] must match /{pattern}/",
        )

    @staticmethod
    def callable_(name: str, fn: Callable[[dict], bool], fail_msg: str = "") -> Check:
        return Check(name=name, predicate=fn, detail_on_fail=fail_msg)
