"""
ToolCache — memoize tool calls by (tool, args).

Cache only deterministic tools. Tag with TTL.
"""

from __future__ import annotations
import time
import hashlib
import json
from typing import Any, Callable
from dataclasses import dataclass, field


@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class ToolCache:
    def __init__(self, default_ttl: float = 300.0):
        self.store: dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def key_for(self, tool: str, args: Any) -> str:
        raw = json.dumps({"t": tool, "a": args}, default=str, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, tool: str, args: Any) -> Any | None:
        k = self.key_for(tool, args)
        e = self.store.get(k)
        if e is None:
            self.misses += 1
            return None
        if e.expires_at < time.time():
            del self.store[k]
            self.misses += 1
            return None
        self.hits += 1
        return e.value

    def put(self, tool: str, args: Any, value: Any, ttl: float | None = None) -> None:
        k = self.key_for(tool, args)
        self.store[k] = CacheEntry(value=value, expires_at=time.time() + (ttl or self.default_ttl))

    def wrap(self, tool: str, fn: Callable[..., Any], ttl: float | None = None) -> Callable[..., Any]:
        def wrapper(*args, **kwargs):
            cached = self.get(tool, args)
            if cached is not None:
                return cached
            v = fn(*args, **kwargs)
            self.put(tool, args, v, ttl)
            return v
        wrapper.cache = self  # type: ignore
        return wrapper

    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hits / total, 3) if total else 0.0,
            "entries": len(self.store),
        }
