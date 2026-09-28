"""
agent_suit — a practical operating layer for any LLM agent.

Philosophy (embedded as code, not docs):
    1. Verification is the core that differentiates knowledge from trusted work.
    2. Skills are expert judgment made eligible for everyone.
    3. Learn from every error; never burn the same mistake twice.
    4. Worklog > compact: keep the full trace, summarize on demand.
    5. LLM calls are non-deterministic. Everything around them should be.
    6. Every mission must end in a boolean predicate, not a feeling.

Drop this folder next to your agent. Import and use.
"""

from .factory import AgentFactory, AgentSpec
from .worklog import Worklog, WorklogEntry
from .verifier import Verifier, Check, CheckResult
from .router import LLMRouter, Route
from .panel import Panel, Persona
from .ralph import RalphLoop, LoopResult
from .learning import ErrorMemory, Lesson
from .deferred import DeferredContext, Pointer
from .deterministic import deterministic, seed_everything, snapshot
from .cache import ToolCache
from .skill_registry import SkillRegistry, Skill, SkillContext

__version__ = "0.1.0"

__all__ = [
    "AgentFactory", "AgentSpec",
    "Worklog", "WorklogEntry",
    "Verifier", "Check", "CheckResult",
    "LLMRouter", "Route",
    "Panel", "Persona",
    "RalphLoop", "LoopResult",
    "ErrorMemory", "Lesson",
    "DeferredContext", "Pointer",
    "deterministic", "seed_everything", "snapshot",
    "ToolCache",
    "SkillRegistry", "Skill", "SkillContext",
]
