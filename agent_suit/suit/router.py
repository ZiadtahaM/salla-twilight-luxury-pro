"""
LLMRouter — send different queries to different models.

Strategies you can compose:
    - by capability (coding, vision, reasoning)
    - by cost (cheap-first, escalate on failure)
    - by latency (fast-first for interactive)
    - by confidence (small model first, judge gates escalation)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Any


@dataclass
class Route:
    name: str
    model: str
    when: Callable[[dict], bool]   # returns True if this route applies
    cost_hint: float = 1.0         # relative cost, for budgeting
    latency_hint_ms: int = 1000


class LLMRouter:
    def __init__(self, routes: list[Route], default: str | None = None):
        self.routes = routes
        self.default = default or (routes[0].name if routes else None)
        self.audit: list[dict] = []

    def pick(self, query: dict) -> Route:
        for r in self.routes:
            try:
                if r.when(query):
                    self.audit.append({"route": r.name, "model": r.model, "query_keys": list(query.keys())})
                    return r
            except Exception:
                continue
        fallback = next(x for x in self.routes if x.name == self.default)
        self.audit.append({"route": fallback.name, "model": fallback.model, "fallback": True})
        return fallback

    # ---- preset factories ----
    @staticmethod
    def cost_escalation(cheap: str, big: str, hard_signal_keys: set[str]) -> "LLMRouter":
        """Cheap model unless query mentions hard-signal keys."""
        return LLMRouter(
            routes=[
                Route(name="cheap", model=cheap, when=lambda q: not (hard_signal_keys & set(q.keys()))),
                Route(name="big",   model=big,   when=lambda q: bool(hard_signal_keys & set(q.keys()))),
            ],
            default="cheap",
        )

    @staticmethod
    def by_capability(map_: dict[str, str], default: str) -> "LLMRouter":
        """capability -> model. {'coding': 'opus', 'vision': 'gpt-4o'}"""
        return LLMRouter(
            routes=[
                Route(name=cap, model=mdl, when=lambda q, cap=cap: q.get("capability") == cap)
                for cap, mdl in map_.items()
            ],
            default=default,
        )
