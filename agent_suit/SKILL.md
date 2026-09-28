---
name: agent-suit
version: 0.1.0
description: |
  The operating layer for any LLM agent. Encodes the philosophy that
  verification is the differentiator between knowledge and trusted work,
  and that expert judgment should be made eligible for everyone via skills.
priority: high
domain: agent-orchestration
tags: [verification, worklog, ralph-loop, factory, panel, learning, deterministic]
---

# Agent Suit — Skill

> "Verification is the core that differentiates knowledge from trusted work."

This skill teaches an agent — or a human building an agent — the **operating
discipline** that turns "an LLM with tools" into "an agent that ships work you
trust." It is the judgment of an expert, captured as executable rules.

---

## When to load this skill

Load when the user is:

- Designing, building, or operating any LLM-driven agent.
- Asking how to make an agent reliable, testable, or auditable.
- Tired of agents that "look right" but aren't.
- Wiring up multi-agent systems, panels, or loops.
- Building anything mission-critical with LLMs.

Do **not** load for:

- Single-shot prompts with no consequences.
- Pure creative writing.
- Casual chat.

---

## The 7 disciplines (in priority order)

### 1. **Define success as a boolean predicate**
Before starting a mission, write the check. No check, no mission.

```
✓ file_exists("out/report.md")
✓ state["answer"] is in {"yes", "no"}
✓ regex(state["sql"], r"^SELECT .* FROM users WHERE active = true")
```

If you can't write it, the mission isn't ready.

### 2. **Loop with Ralph discipline**
observe → act → verify → repeat. Never trust in-flight memory; re-read state.
Always bound by `max_iters` AND `max_seconds`. Always log decisions.

### 3. **Worklog > compact, always**
Keep the full trace. Inject a compact summary at the top for orientation.
The worklog is the source of truth; summaries are projections.

### 4. **Factory, not bespoke**
Define `AgentSpec`s. Spawn with `factory.build(name, ...)`. Swap models
without touching logic. A/B test blueprints like config.

### 5. **Route by intent**
Cheap model for cheap questions. Big model for hard signals. Confidence
gates escalation. Log every routing decision.

### 6. **Panel for hard decisions**
For architecture / ethics / product calls, run 2–4 opposing personas in
parallel. Synthesize with a judge. Surface agreements and irreconcilable
conflicts explicitly.

### 7. **Learn from every mistake**
Every error → `memory.record(error, lesson)`. Before acting, query memory.
Never burn the same mistake twice. Track repeat count; escalate after N.

---

## The operating checklist (run this for every mission)

```
[ ] 1. Write the verification predicate FIRST.
[ ] 2. Define the worklog path and skill registry.
[ ] 3. Spawn the agent via factory (don't handcraft).
[ ] 4. Run inside RalphLoop with max_iters + max_seconds.
[ ] 5. Inject worklog compact summary each iteration for orientation.
[ ] 6. After each failed step: record lesson, query prior lessons, retry.
[ ] 7. On 2x repeat failure: escalate to human / bigger model.
[ ] 8. On verification pass: snapshot state, seal worklog, done.
[ ] 9. If decision is architectural/ethical: panel it.
```

---

## Anti-patterns (when the agent is doing it wrong)

- ❌ "I think it's done" → ✅ run the verifier, paste the result.
- ❌ Pasting the full worklog into every prompt → ✅ inject compact summary + tail.
- ❌ Same tool call 5 times in a row → ✅ check memory, change approach.
- ❌ Spawning an agent without a verification predicate → ✅ write check first.
- ❌ One mega-prompt for everything → ✅ factory + routing + panels.
- ❌ "Temperature=0.7 by default" → ✅ pin randomness for reproducibility.
- ❌ Treating panel personas as flavor text → ✅ give them real priors, real conflicts.

---

## When to escalate

Escalate when:
- Same failure signature repeats 2+ times.
- A verification predicate is impossible to write (mission under-specified).
- Two panel personas produce irreconcilable answers on a high-stakes call.
- The worklog shows the agent is generating context, not consuming it.

Escalation options:
- Bigger model.
- Human review.
- Re-scope the mission.

---

## Files in this skill

- `suit/__init__.py` — public surface
- `suit/worklog.py` — append-only trace
- `suit/verifier.py` — boolean predicate harness
- `suit/ralph.py` — observe→act→verify loop
- `suit/factory.py` — agent blueprints
- `suit/router.py` — LLM routing
- `suit/panel.py` — opposing philosophy panel
- `suit/learning.py` — error memory
- `suit/deferred.py` — pointer-based context
- `suit/cache.py` — tool result cache
- `suit/deterministic.py` — seed/snapshot/cache helpers
- `suit/skill_registry.py` — judgment-as-code

---

## Minimal invocation

```python
from agent_suit import (
    AgentFactory, Worklog, Verifier, Check,
    RalphLoop, SkillRegistry, ErrorMemory,
    seed_everything,
)

seed_everything(42)
memory = ErrorMemory()
registry = SkillRegistry.starter_pack()
worklog = Worklog(mission_id="M-001")
verifier = Verifier([Check("answer_present", lambda s: bool(s.get("answer")))])

# step_fn(state, worklog) -> state
def step(state, wl):
    state["answer"] = state.get("answer") or "computed-answer"
    return state

loop = RalphLoop(verifier=verifier, step_fn=step, max_iters=10)
result = loop.run({}, worklog)
print(result.success, result.final_state)
print(worklog.compact_summary())
```
