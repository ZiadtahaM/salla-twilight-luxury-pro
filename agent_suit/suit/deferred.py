"""
DeferredContext — pointers now, fetch when needed.

Agents can't keep everything in head. This gives them a way to say
"this exists, here's how to load it" without paying the context cost upfront.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
from pathlib import Path


@dataclass
class Pointer:
    key: str
    source: str                # file path, doc id, url, etc.
    summary: str               # 1-line orientation
    loader: Callable[[], Any] | None = None
    estimated_tokens: int = 0


class DeferredContext:
    def __init__(self):
        self.pointers: dict[str, Pointer] = {}

    def add(self, p: Pointer) -> None:
        self.pointers[p.key] = p

    def from_file(self, key: str, path: str, summary: str = "") -> "DeferredContext":
        p = Path(path)
        if not summary:
            summary = f"file @ {path}"
        self.add(Pointer(
            key=key, source=path, summary=summary,
            loader=lambda: p.read_text() if p.exists() else "",
            estimated_tokens=p.stat().st_size // 4 if p.exists() else 0,
        ))
        return self

    def resolve(self, key: str) -> Any:
        p = self.pointers[key]
        if p.loader is None:
            raise ValueError(f"no loader for pointer {key}")
        return p.loader()

    def resolve_into(self, target: dict, *keys: str) -> dict:
        for k in keys:
            if k in self.pointers:
                target[k] = self.resolve(k)
        return target

    def manifest(self) -> str:
        """Tiny manifest: pointers + summaries, fits in any context window."""
        lines = ["Deferred context (use resolve(key) to load):"]
        for p in self.pointers.values():
            lines.append(f"  - {p.key}  ({p.estimated_tokens} tok)  {p.summary}")
        return "\n".join(lines)
