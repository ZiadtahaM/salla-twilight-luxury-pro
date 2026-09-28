"""
ErrorMemory — never burn the same mistake twice.

Every error/lesson logged into the worklog gets promoted into a queryable memory.
Before the agent acts on a similar shape of problem, it consults memory first.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from collections import Counter
import re
import time


@dataclass
class Lesson:
    id: str
    signature: str   # extracted signature from the error / situation
    lesson: str
    count: int = 1
    last_seen: float = field(default_factory=time.time)
    examples: list[str] = field(default_factory=list)


class ErrorMemory:
    def __init__(self):
        self.lessons: dict[str, Lesson] = []

    def record(self, error_or_observation: str, lesson: str, signature: str | None = None) -> Lesson:
        sig = signature or self._extract_signature(error_or_observation)
        for ls in self.lessons:
            if ls.signature == sig:
                ls.count += 1
                ls.last_seen = time.time()
                ls.examples.append(error_or_observation[:200])
                return ls
        new = Lesson(id=f"L{len(self.lessons)+1:04d}", signature=sig, lesson=lesson)
        new.examples.append(error_or_observation[:200])
        self.lessons.append(new)
        return new

    def recall(self, situation: str, top_k: int = 3) -> list[Lesson]:
        """Return lessons whose signature matches tokens in the situation."""
        toks = set(re.findall(r"\w+", situation.lower()))
        scored = []
        for ls in self.lessons:
            sig_toks = set(re.findall(r"\w+", ls.signature.lower()))
            overlap = len(toks & sig_toks)
            if overlap:
                scored.append((overlap * ls.count, ls))
        scored.sort(reverse=True)
        return [ls for _, ls in scored[:top_k]]

    def format_for_prompt(self, situation: str, top_k: int = 3) -> str:
        hits = self.recall(situation, top_k)
        if not hits:
            return "(no prior lessons)"
        lines = ["Lessons learned (apply before acting):"]
        for ls in hits:
            lines.append(f"- [{ls.id}] (seen {ls.count}x) {ls.lesson}")
        return "\n".join(lines)

    @staticmethod
    def _extract_signature(text: str) -> str:
        """Cheap signature: error type + first few content words."""
        # look for "XxxError" or "XxxException"
        m = re.search(r"\b(\w+(?:Error|Exception|Failure))\b", text)
        kind = m.group(1) if m else "issue"
        # first 6 alphanumeric words
        words = re.findall(r"\w+", text)[:6]
        return f"{kind}:{' '.join(words)}"

    def stats(self) -> dict:
        return {
            "total_lessons": len(self.lessons),
            "top_repeated": sorted(
                ({"sig": l.signature, "count": l.count, "lesson": l.lesson} for l in self.lessons),
                key=lambda x: -x["count"],
            )[:5],
        }
