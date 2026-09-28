"""
Worklog — append-only trace of every step an agent takes.

Why worklog over compact:
    - Lossless: nothing is forgotten unless we explicitly trim.
    - Auditable: replay, debug, defend.
    - Hybrid-ready: top of worklog can carry a compact summary for orientation.

Pattern: agent.step() logs here. Verifier reads from here. Memory writes here.
"""

from __future__ import annotations
import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional


@dataclass
class WorklogEntry:
    step_id: str
    kind: str           # "thought" | "tool_call" | "tool_result" | "decision" | "verify" | "error" | "lesson"
    content: Any
    ts: float = field(default_factory=time.time)
    meta: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


class Worklog:
    """Append-only trace. Cheap to write, free to read."""

    def __init__(self, mission_id: Optional[str] = None, persist_to: Optional[Path] = None):
        self.mission_id = mission_id or f"mission-{uuid.uuid4().hex[:8]}"
        self.persist_to = persist_to
        self.entries: list[WorklogEntry] = []
        self._opened = time.time()

    def append(self, kind: str, content: Any, **meta) -> WorklogEntry:
        entry = WorklogEntry(
            step_id=f"s-{len(self.entries):04d}",
            kind=kind,
            content=content,
            meta=meta,
        )
        self.entries.append(entry)
        if self.persist_to:
            self._flush(entry)
        return entry

    # ---- shorthands ----
    def thought(self, content: str, **m): return self.append("thought", content, **m)
    def tool_call(self, name: str, args: Any, **m): return self.append("tool_call", {"name": name, "args": args}, **m)
    def tool_result(self, name: str, result: Any, **m): return self.append("tool_result", {"name": name, "result": result}, **m)
    def decision(self, content: str, **m): return self.append("decision", content, **m)
    def verify(self, passed: bool, detail: str, **m): return self.append("verify", {"passed": passed, "detail": detail}, **m)
    def error(self, exc: Exception, **m): return self.append("error", {"type": type(exc).__name__, "msg": str(exc)}, **m)
    def lesson(self, lesson: str, **m): return self.append("lesson", lesson, **m)

    # ---- views ----
    def tail(self, n: int = 20) -> list[WorklogEntry]:
        return self.entries[-n:]

    def compact_summary(self, max_entries: int = 8) -> str:
        """Top-of-window orientation: what happened, what's pending, what's the next move."""
        recent = self.entries[-max_entries:]
        lines = [f"mission={self.mission_id}  steps={len(self.entries)}"]
        for e in recent:
            content_str = str(e.content)[:160].replace("\n", " ")
            lines.append(f"  [{e.step_id}] {e.kind}: {content_str}")
        return "\n".join(lines)

    def full_text(self) -> str:
        return "\n".join(f"[{e.step_id}] {e.kind}: {e.content}" for e in self.entries)

    def errors(self) -> list[WorklogEntry]:
        return [e for e in self.entries if e.kind == "error"]

    def _flush(self, entry: WorklogEntry) -> None:
        assert self.persist_to is not None
        self.persist_to.parent.mkdir(parents=True, exist_ok=True)
        with self.persist_to.open("a") as f:
            f.write(json.dumps(entry.to_dict()) + "\n")

    def __len__(self) -> int:
        return len(self.entries)

    def __bool__(self) -> bool:
        # Always truthy — an empty worklog is still a valid worklog.
        # Without this, `wl or Worklog()` would replace empty worklogs.
        return True
