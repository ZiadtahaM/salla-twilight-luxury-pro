"""
end_to_end.py — full demo of the suit in one runnable script.

A fake "build a config file" mission:
    - Verifier says it must exist with required keys
    - RalphLoop iterates a step_fn that simulates tool calls
    - First iter: the file is missing -> error -> lesson learned
    - Second iter: file exists but wrong content -> still fails
    - Third iter: correct -> verification passes
    - Compact summary + learning stats printed at the end
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# Make the package importable when run from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from suit import (
    Worklog,
    Verifier,
    Check,
    RalphLoop,
    LoopResult,
    ErrorMemory,
    SkillRegistry,
    SkillContext,
    LLMRouter,
    Route,
    Panel,
    Persona,
    ToolCache,
    DeferredContext,
    Pointer,
    seed_everything,
    snapshot,
)


def main() -> int:
    seed_everything(42)

    tmpdir = Path(tempfile.mkdtemp(prefix="agent_suit_demo_"))
    target_file = tmpdir / "config.json"

    print(f"[demo] working dir: {tmpdir}")

    # ---- 1. Verifier: define success BEFORE starting ---------------------
    required_keys = {"host", "port", "ssl"}

    def has_all_keys(state: dict) -> bool:
        cfg = state.get("config", {})
        return isinstance(cfg, dict) and required_keys.issubset(cfg.keys())

    def port_in_range(state: dict) -> bool:
        cfg = state.get("config", {})
        p = cfg.get("port", 0)
        return isinstance(p, int) and 1 <= p <= 65535

    def ssl_is_bool(state: dict) -> bool:
        return isinstance(state.get("config", {}).get("ssl"), bool)

    verifier = Verifier([
        Check("file_exists",   lambda s: Path(s["path"]).exists(),
              detail_on_fail="config file must be on disk"),
        Check("valid_json",    lambda s: _safe_load(Path(s["path"])) is not None,
              detail_on_fail="config must be parseable JSON"),
        Check("all_keys",      has_all_keys,
              detail_on_fail=f"config must contain {required_keys}"),
        Check("port_range",    port_in_range,
              detail_on_fail="port must be 1..65535"),
        Check("ssl_is_bool",   ssl_is_bool,
              detail_on_fail="ssl must be a boolean"),
    ])

    # ---- 2. Error memory + skill registry ---------------------------------
    memory = ErrorMemory()
    registry = SkillRegistry.starter_pack()

    # ---- 3. Worklog ------------------------------------------------------
    worklog = Worklog(mission_id="build-config", persist_to=tmpdir / "worklog.jsonl")

    # ---- 4. Step function: pretend agent + tools -------------------------
    attempt = {"n": 0, "consecutive_failures": 0, "last_error": None}

    def step(state: dict, wl: Worklog) -> dict:
        attempt["n"] += 1
        state["path"] = str(target_file)
        wl.thought(f"attempt #{attempt['n']}")

        # Skill: if there's a last_error, record the lesson first
        ctx = SkillContext(
            worklog=wl, verifier=verifier, memory=memory,
            cache=ToolCache(), deferred=DeferredContext(),
        )
        registry.run_applicable(
            {"last_error": attempt["last_error"], "consecutive_failures": attempt["consecutive_failures"]},
            ctx,
        )

        # Mock "tool call" — simulate the agent's evolving attempts
        if attempt["n"] == 1:
            # forget to create the file
            wl.tool_call("write_file", {"path": state["path"], "content": "oops"})
            attempt["last_error"] = "FileNotFoundError: no such file 'config.json'"
            attempt["consecutive_failures"] += 1
            state["config"] = None
            return state

        if attempt["n"] == 2:
            # write a file but with wrong shape
            wl.tool_call("write_file", {"path": state["path"], "content": json.dumps({"host": "x"})})
            target_file.write_text(json.dumps({"host": "x"}))
            attempt["last_error"] = "ValueError: missing keys {'port', 'ssl'}"
            attempt["consecutive_failures"] += 1
            state["config"] = {"host": "x"}
            return state

        # n==3 -> write correct config
        cfg = {"host": "localhost", "port": 443, "ssl": True}
        target_file.write_text(json.dumps(cfg))
        wl.tool_call("write_file", {"path": state["path"], "content": json.dumps(cfg)})
        wl.tool_result("write_file", {"ok": True})
        state["config"] = cfg
        attempt["last_error"] = None
        attempt["consecutive_failures"] = 0
        return state

    loop = RalphLoop(verifier=verifier, step_fn=step, max_iters=10, max_seconds=30.0)

    # ---- 5. Run ----------------------------------------------------------
    initial_state = {"path": str(target_file), "config": None}
    result = loop.run(initial_state, worklog)

    print()
    print("=" * 60)
    print(f"SUCCESS: {result.success}  iterations: {result.iterations}  reason: {result.reason}")
    print(f"final state snapshot: {snapshot(result.final_state, 'state')}")
    print("=" * 60)
    print()
    print("--- compact worklog summary ---")
    print(worklog.compact_summary())
    print()
    print("--- lessons learned ---")
    for ls in memory.lessons:
        print(f"  [{ls.id}] (x{ls.count}) {ls.lesson}")
    print()
    print("--- memory stats ---")
    print(json.dumps(memory.stats(), indent=2))
    print()
    print(f"[demo] worklog persisted at: {tmpdir / 'worklog.jsonl'}")
    return 0 if result.success else 1


def _safe_load(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


if __name__ == "__main__":
    sys.exit(main())
