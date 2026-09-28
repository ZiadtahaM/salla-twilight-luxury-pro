# Agent Suit

> Verification is the core that differentiates knowledge from trusted work.
> Skills are expert judgment made eligible for everyone.

A small, opinionated Python toolkit that turns "an LLM with tools" into "an agent that ships work you trust." Drop-in. Zero external deps. ~600 LOC total.

---

## What's inside

| Module | What it does |
|---|---|
| `Worklog` | Append-only trace of every step. Lossless audit. Hybrid summary view. |
| `Verifier` + `Check` | Boolean predicates over observable state. No vibes — yes/no. |
| `RalphLoop` | observe → act → verify → repeat, with iter + time budgets. |
| `AgentFactory` + `AgentSpec` | Spawn configured agents from blueprints. Swap models cleanly. |
| `LLMRouter` | Route by capability / cost / signal. Audit every decision. |
| `Panel` + `Persona` | Run opposing philosophies in parallel, judge synthesizes. |
| `ErrorMemory` + `Lesson` | Never burn the same mistake twice. Queryable, weighted. |
| `DeferredContext` + `Pointer` | Pointers now, fetch on demand. Manifest fits any window. |
| `ToolCache` | Memoize deterministic tool calls by (tool, args), TTL'd. |
| `deterministic` helpers | seed, snapshot, cache pure functions. |
| `SkillRegistry` + `Skill` | Judgment-as-code. `when`/`action`/`verify` triples. |

Plus:
- `SKILL.md` — the meta-skill that captures this philosophy for any agent.
- `examples/end_to_end.py` — full Ralph loop with verification, learning, and persistence.
- `examples/panel_and_factory.py` — opposing panel + factory spawn, offline-runnable.

---

## Install / use

```bash
# drop the agent_suit/ folder next to your project
cd your-project
ln -s /path/to/agent_suit ./agent_suit
export PYTHONPATH=.
```

Or just `pip install -e .` if you turn it into a proper package.

---

## The 7 disciplines (priority order)

```
1. Define success as a boolean predicate          (Verifier + Check)
2. Loop with Ralph discipline                     (RalphLoop)
3. Worklog > compact, always                      (Worklog)
4. Factory, not bespoke                           (AgentFactory)
5. Route by intent                                (LLMRouter)
6. Panel for hard decisions                       (Panel)
7. Learn from every mistake                       (ErrorMemory + SkillRegistry)
```

---

## Minimal invocation

```python
from agent_suit import (
    Worklog, Verifier, Check, RalphLoop, seed_everything,
)

seed_everything(42)
worklog  = Worklog(mission_id="M-001", persist_to="runs/M-001/worklog.jsonl")
verifier = Verifier([Check("answer_present", lambda s: bool(s.get("answer")))])

def step(state, wl):
    wl.thought("doing the thing")
    state["answer"] = state.get("answer") or "computed"
    return state

result = RalphLoop(verifier=verifier, step_fn=step, max_iters=10).run({}, worklog)
print(result.success, result.iterations)
print(worklog.compact_summary())  # cheap orientation for the next prompt
```

---

## End-to-end (real)

```bash
python examples/end_to_end.py
```

You'll see:
- 3 iterations of the Ralph loop
- 5 checks all pass on iter 3
- 2 lessons learned from the failures on iter 1 and 2
- a JSONL worklog persisted to disk

```
SUCCESS: True  iterations: 3  reason: verified
final state snapshot: state:2c7484ee66ba82b5
--- compact worklog summary ---
mission=build-config  steps=28
  [s-0020] tool_call: write_file ...
  [s-0022..s-0026] verify: all passed
  [s-0027] decision: verification passed; loop done
```

---

## Patterns you can lift into your own agent

### "Verify before you celebrate"
```python
verifier = Verifier([
    Check("file_written",  lambda s: Path(s["out"]).exists()),
    Check("schema_valid",  lambda s: validate(s["artifact"], schema)),
    Check("no_secrets",    lambda s: not contains_secret(s.get("text",""))),
])
```

### "Loop with discipline"
```python
RalphLoop(verifier=v, step_fn=agent.step, max_iters=15, max_seconds=90)
```
Always set BOTH bounds. Always log every iteration.

### "Spawn many of the same blueprint"
```python
factory = AgentFactory(build_fn)
factory.register(AgentFactory.default_blueprints()["coder"])
agents  = factory.build_many("coder", count=8, model="sonnet")
```

### "Route by intent"
```python
router = LLMRouter.cost_escalation(cheap="haiku", big="opus", hard_signal_keys={"code", "math"})
route  = router.pick({"code": "yes", "question": "..."})
print(route.model)  # "opus"
```

### "Panel a hard decision"
```python
panel    = Panel(personas=Panel.opposing_philosophies(), runner=my_llm_call)
opinions = panel.ask("Should we ship feature X?")
synthesis = judge_synthesize(opinions)
```

### "Never repeat a mistake"
```python
memory = ErrorMemory()
memory.record(err_msg, lesson="never pass None to render()")
# later, before acting:
ctx_prompt += "\n" + memory.format_for_prompt(current_situation)
```

### "Package judgment as a skill"
```python
def skill_check_secrets(situation, ctx):
    text = situation.get("text", "")
    if "sk-" in text or "AKIA" in text:
        ctx.worklog.error("secret leak suspected")
        return "ABORT"
    return "OK"

registry.register(Skill(
    name="guard-secrets",
    when=lambda s: "text" in s,
    action=skill_check_secrets,
    description="Abort if a probable secret is in the output.",
    tags=["safety", "always"],
))
```

---

## What the suit is NOT

- Not a framework that wraps your LLM. Use your own client.
- Not a state machine DSL. Plain Python.
- Not opinionated about which model. Bring your own.
- Not a UI. CLI / library only.

---

## How to extend

Add a new module under `suit/`, expose it in `suit/__init__.py`, register any skill in `SkillRegistry.starter_pack()`.

Add a new blueprint to `AgentFactory.default_blueprints()`.

Add a new check type to `Verifier` (`@staticmethod file_exists(...)`, etc.).

That's it. No magic. No DSL.

---

## Tests / smoke check

```bash
python examples/end_to_end.py        # full ralph loop, expects SUCCESS
python examples/panel_and_factory.py # panel + factory, expects all 4 personas
```

Both exit 0 on success.

---

## License

MIT. Take it, fork it, ship it.
