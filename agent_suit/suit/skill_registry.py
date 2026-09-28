"""
SkillRegistry — expert judgment made eligible for everyone.

A skill is a packaged heuristic that says:
    "When the situation looks like X, do Y, verify with Z."

It's not a doc. It's executable judgment. Loaded into the agent when relevant.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Any


@dataclass
class Skill:
    name: str
    when: Callable[[dict], bool]               # situation -> True if relevant
    action: Callable[[dict, "SkillContext"], Any]  # what to do
    verify: Callable[[dict], bool] | None = None  # how to know it worked
    description: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class SkillContext:
    worklog: Any
    verifier: Any
    memory: Any
    cache: Any
    deferred: Any


class SkillRegistry:
    def __init__(self):
        self.skills: list[Skill] = []

    def register(self, skill: Skill) -> None:
        self.skills.append(skill)

    def applicable(self, situation: dict) -> list[Skill]:
        return [s for s in self.skills if s.when(situation)]

    def run_applicable(self, situation: dict, ctx: SkillContext) -> list[tuple[Skill, Any]]:
        results = []
        for s in self.applicable(situation):
            try:
                r = s.action(situation, ctx)
                results.append((s, r))
            except Exception as e:
                results.append((s, f"failed: {e}"))
        return results

    @staticmethod
    def starter_pack() -> "SkillRegistry":
        """A small set of universal skills. Add your own."""
        reg = SkillRegistry()

        def has_error(situation: dict) -> bool:
            return bool(situation.get("last_error"))

        def record_lesson(situation: dict, ctx: SkillContext):
            err = situation["last_error"]
            lesson = situation.get("lesson") or f"avoid: {err[:120]}"
            return ctx.memory.record(err, lesson)

        reg.register(Skill(
            name="remember-the-mistake",
            when=has_error,
            action=record_lesson,
            description="When something failed, log it as a lesson before retrying.",
            tags=["learning", "always"],
        ))

        def is_wide_context(situation: dict) -> bool:
            return situation.get("context_chars", 0) > 20_000

        def compress_context(situation: dict, ctx: SkillContext):
            wl = ctx.worklog
            return wl.compact_summary(max_entries=8)

        reg.register(Skill(
            name="summarize-when-wide",
            when=is_wide_context,
            action=compress_context,
            description="When context is bloated, prefer the compact summary view.",
            tags=["context", "efficiency"],
        ))

        def is_repeat_failure(situation: dict) -> bool:
            return situation.get("consecutive_failures", 0) >= 2

        def escalate(situation: dict, ctx: SkillContext):
            return ("escalate", situation.get("last_error"))

        reg.register(Skill(
            name="escalate-after-repeat-failure",
            when=is_repeat_failure,
            action=escalate,
            verify=lambda s: s.get("consecutive_failures", 0) == 0,
            description="If the same shape of failure recurs, escalate instead of looping.",
            tags=["safety", "loop-guard"],
        ))

        return reg
