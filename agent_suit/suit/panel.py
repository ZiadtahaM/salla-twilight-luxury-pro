"""
Panel — run a question through N personas with opposing philosophies,
then synthesize via a judge.

Use cases:
    - product/architecture decisions
    - red-teaming
    - ethics checks
    - debugging hypothesis selection
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
import asyncio


@dataclass
class Persona:
    name: str
    system_prompt: str
    priors: list[str] = field(default_factory=list)   # worldview commitments


@dataclass
class PanelOpinion:
    persona: Persona
    response: str


class Panel:
    def __init__(self, personas: list[Persona], runner: Callable[[Persona, str], str]):
        """
        runner(persona, question) -> str
        Plug in your LLM call. Must be callable per persona.
        """
        self.personas = personas
        self.runner = runner

    def ask(self, question: str) -> list[PanelOpinion]:
        opinions = []
        for p in self.personas:
            full = f"You are {p.name}.\n{p.system_prompt}\nPriors: {'; '.join(p.priors)}\n\nQuestion: {question}"
            response = self.runner(p, full)
            opinions.append(PanelOpinion(persona=p, response=response))
        return opinions

    async def ask_async(self, question: str, async_runner) -> list[PanelOpinion]:
        tasks = [async_runner(p, f"{p.system_prompt}\nPriors: {'; '.join(p.priors)}\n\nQuestion: {question}")
                 for p in self.personas]
        responses = await asyncio.gather(*tasks)
        return [PanelOpinion(persona=p, response=r) for p, r in zip(self.personas, responses)]

    @staticmethod
    def opposing_philosophies() -> list[Persona]:
        """A starter panel with genuinely conflicting priors."""
        return [
            Persona(
                name="Ship-Fast Founder",
                system_prompt="You ship MVPs. Speed beats perfection. Bias to action.",
                priors=["time-to-market > completeness", "iterate based on feedback"],
            ),
            Persona(
                name="Security-Paranoid Architect",
                system_prompt="You assume every input is hostile. You think in attack surfaces.",
                priors=["deny-by-default", "least-privilege", "audit-trail-or-it-didn't-happen"],
            ),
            Persona(
                name="User-Empathy Researcher",
                system_prompt="You center the user's lived experience. You look for frictions and delights.",
                priors=["observe first", "speak to real workflows", "delight beats features"],
            ),
            Persona(
                name="Pragmatic Operator",
                system_prompt="You optimize for what works in production. Maintenance is a feature.",
                priors=["boring tech wins", "if it can't be paged, it can't ship"],
            ),
        ]
