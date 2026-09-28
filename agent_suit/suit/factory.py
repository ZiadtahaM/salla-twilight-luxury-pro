"""
AgentFactory — same blueprint, different inputs.

A factory lets you:
    - spawn many agents in parallel for many tasks
    - swap models without rewriting code
    - A/B test agent configurations
    - version-control agent blueprints
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
import uuid


@dataclass
class AgentSpec:
    name: str
    system_prompt: str
    tools: list[str] = field(default_factory=list)
    model: str = "sonnet"
    temperature: float = 0.0
    metadata: dict = field(default_factory=dict)


class AgentFactory:
    """Stamps out configured agents. Plug in your own `build_fn`."""

    def __init__(self, build_fn: Callable[[AgentSpec, str], Any]):
        """
        build_fn(spec, agent_id) -> agent
        e.g. build_fn could call openai/claude/your-framework.
        """
        self.build_fn = build_fn
        self.registry: dict[str, AgentSpec] = {}

    def register(self, spec: AgentSpec) -> None:
        self.registry[spec.name] = spec

    def build(self, name: str, **overrides) -> tuple[Any, str]:
        if name not in self.registry:
            raise KeyError(f"unknown agent {name!r}. known: {list(self.registry)}")
        spec = self.registry[name]
        # apply overrides
        for k, v in overrides.items():
            if hasattr(spec, k):
                setattr(spec, k, v)
        agent_id = f"{name}-{uuid.uuid4().hex[:6]}"
        agent = self.build_fn(spec, agent_id)
        return agent, agent_id

    def build_many(self, name: str, count: int, **overrides) -> list[tuple[Any, str]]:
        return [self.build(name, **overrides) for _ in range(count)]

    # ---- presets ----
    @staticmethod
    def default_blueprints() -> dict[str, AgentSpec]:
        return {
            "researcher": AgentSpec(
                name="researcher",
                system_prompt="You gather facts. Cite sources. No opinions.",
                tools=["web_search", "web_fetch"],
                model="sonnet",
            ),
            "coder": AgentSpec(
                name="coder",
                system_prompt="You write code that compiles, runs, and is tested.",
                tools=["read_file", "write_file", "bash"],
                model="opus",
            ),
            "critic": AgentSpec(
                name="critic",
                system_prompt="You are skeptical. Find what could go wrong. Steelman first, then attack.",
                tools=[],
                model="sonnet",
            ),
            "judge": AgentSpec(
                name="judge",
                system_prompt="You score outputs on a rubric. Be precise. Output only the score.",
                tools=[],
                model="sonnet",
                temperature=0.0,
            ),
        }
