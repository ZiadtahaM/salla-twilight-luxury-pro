"""
RalphLoop — observe → act → verify, until done or budget exhausted.

The key discipline: don't trust in-flight memory. Re-read state every iteration.
The worklog holds context; the loop holds discipline.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Any
import time

from .worklog import Worklog
from .verifier import Verifier


@dataclass
class LoopResult:
    success: bool
    iterations: int
    final_state: dict
    reason: str = ""


class RalphLoop:
    def __init__(
        self,
        *,
        verifier: Verifier,
        step_fn: Callable[[dict, Worklog], dict],
        max_iters: int = 20,
        max_seconds: float = 120.0,
        on_iteration: Callable[[int, dict], None] | None = None,
    ):
        """
        step_fn(state, worklog) -> new_state
        Each iteration, you get the full state and the worklog, you return an updated state.
        """
        self.verifier = verifier
        self.step_fn = step_fn
        self.max_iters = max_iters
        self.max_seconds = max_seconds
        self.on_iteration = on_iteration

    def run(self, initial_state: dict, worklog: Worklog | None = None) -> LoopResult:
        wl = worklog or Worklog()
        state = dict(initial_state)
        deadline = time.time() + self.max_seconds

        for i in range(self.max_iters):
            if time.time() > deadline:
                wl.append("decision", f"aborting: time budget exceeded ({self.max_seconds}s)")
                return LoopResult(False, i, state, "timeout")

            wl.thought(f"--- iteration {i} ---")
            try:
                state = self.step_fn(state, wl) or state
            except Exception as e:
                wl.error(e, iter=i)
                return LoopResult(False, i + 1, state, f"step raised {type(e).__name__}: {e}")

            passed, results = self.verifier.run(state, wl)
            if self.on_iteration:
                self.on_iteration(i, state)

            if passed:
                wl.decision("verification passed; loop done")
                return LoopResult(True, i + 1, state, "verified")

            failing = [r for r in results if not r.passed]
            wl.decision(f"verification failed; failing checks: {[r.name for r in failing]}")

        return LoopResult(False, self.max_iters, state, "max iters reached")
