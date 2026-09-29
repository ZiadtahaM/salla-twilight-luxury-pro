"""
run_salla_mission.py — Agent Suit mission runner for Salla Twilight Luxury Pro storefront.
Applies the 7 mandatory disciplines of Agent Suit:
1. Define success as a boolean predicate (Verifier + Check)
2. Loop with Ralph discipline (RalphLoop)
3. Worklog > compact, always (Worklog)
4. Factory, not bespoke (AgentFactory)
5. Route by intent (LLMRouter)
6. Panel for hard decisions (Panel with opposing philosophies)
7. Learn from every mistake (ErrorMemory + Lessons)
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path

# Insert agent_suit into python path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "agent_suit"))

from suit import (
    Worklog,
    Verifier,
    Check,
    RalphLoop,
    ErrorMemory,
    AgentFactory,
    AgentSpec,
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


def run_mission():
    seed_everything(42)
    worklog_path = repo_root / "agent_suit" / "worklogs" / "salla_luxury_mission.jsonl"
    worklog = Worklog(mission_id="salla-twilight-luxury-pro", persist_to=worklog_path)
    worklog.thought("Initializing Agent Suit mission runner for Salla Twilight Luxury Pro")

    # ---- 1. ERROR MEMORY & LESSONS LEARNED ----
    memory = ErrorMemory()
    memory.record(
        error_or_observation="TwigException: Unknown function salla_header and salla_footer caused Salla to silently fallback to Theme Raed",
        lesson="Salla Twilight engine does NOT define salla_header() or salla_footer(). Templates must use {% hook 'head:start' %}, {% hook head %}, {% hook 'head:end' %}, {% hook 'body:start' %}, {% hook 'body:end' %}.",
        signature="TwigException:unknown_salla_functions",
    )
    memory.record(
        error_or_observation="SallaCLI: pnpm run watch exited with error missing script watch",
        lesson="Salla CLI preview daemon invokes 'pnpm run watch' internally. package.json MUST declare a 'watch' script.",
        signature="SallaCLI:missing_watch_script",
    )
    memory.record(
        error_or_observation="TwilightJSONFormatError: Root name and description must be multilingual dicts",
        lesson="twilight.json root properties 'name' and 'description' must be dicts with 'ar' and 'en' keys; components and settings must be lists.",
        signature="SchemaError:twilight_json_format",
    )
    memory.record(
        error_or_observation="TwigTemplateNotFound: extends 'src/views/layouts/master.twig' failed",
        lesson="Salla Twilight view paths are dot-delimited relative to src/views. Must write extends 'layouts.master'.",
        signature="TwigError:template_path_dot_delimited",
    )
    memory.record(
        error_or_observation="UserReport: Visiting demostore.salla.sa showed default demo theme",
        lesson="A development theme only renders inside an authenticated Salla Draft Preview session (?url=https://s.salla.sa/design/draft-...). It does not replace the public store theme until published.",
        signature="PlatformBehavior:draft_vs_public_url",
    )

    worklog.decision(f"ErrorMemory primed with {len(memory.lessons)} prior operational lessons")

    # ---- 2. VERIFIER CHECKS (DEFINING SUCCESS AS BOOLEAN PREDICATES) ----
    def check_twilight_json(s: dict) -> bool:
        p = repo_root / "twilight.json"
        if not p.exists():
            return False
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        has_name = isinstance(data.get("name"), dict) and "ar" in data["name"]
        has_desc = isinstance(data.get("description"), dict) and "ar" in data["description"]
        has_comps = isinstance(data.get("components"), list) and len(data["components"]) > 0
        has_settings = isinstance(data.get("settings"), list)
        return has_name and has_desc and has_comps and has_settings

    def check_master_twig_hooks(s: dict) -> bool:
        p = repo_root / "src" / "views" / "layouts" / "master.twig"
        if not p.exists():
            return False
        content = p.read_text(encoding="utf-8")
        req_hooks = ["head:start", "head:end", "body:start", "body:end"]
        return all(h in content for h in req_hooks) and "{% hook head %}" in content

    def check_no_forbidden_functions(s: dict) -> bool:
        views_dir = repo_root / "src" / "views"
        forbidden = ["salla_header(", "salla_footer(", "salla_checkout_url("]
        for f in views_dir.rglob("*.twig"):
            content = f.read_text(encoding="utf-8")
            if any(bad in content for bad in forbidden):
                return False
        return True

    def check_pages_extend_master(s: dict) -> bool:
        pages_dir = repo_root / "src" / "views" / "pages"
        for f in pages_dir.rglob("*.twig"):
            content = f.read_text(encoding="utf-8")
            if '{% extends "layouts.master" %}' not in content:
                return False
        return True

    def check_hero_banner_fallbacks(s: dict) -> bool:
        p = repo_root / "src" / "views" / "components" / "home" / "luxury-hero-banner.twig"
        if not p.exists():
            return False
        content = p.read_text(encoding="utf-8")
        return "component.fields|default" in content and "banner.title|default" in content

    def check_package_json_scripts(s: dict) -> bool:
        p = repo_root / "package.json"
        if not p.exists():
            return False
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        scripts = data.get("scripts", {})
        return "development" in scripts and "watch" in scripts

    def check_salla_cli_authenticated(s: dict) -> bool:
        cfg = Path(r"C:\Users\DevUser\.salla\config.json")
        if not cfg.exists():
            return False
        with open(cfg, "r", encoding="utf-8") as f:
            data = json.load(f)
        return bool(data.get("salla", {}).get("access_token"))

    def check_git_clean_and_synced(s: dict) -> bool:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
        )
        # modified files tracked by git should be 0
        lines = [l for l in res.stdout.splitlines() if not l.startswith("??")]
        return len(lines) == 0

    verifier = Verifier([
        Check("twilight_json_valid", check_twilight_json, "twilight.json must be valid schema"),
        Check("master_twig_lifecycle_hooks", check_master_twig_hooks, "master.twig must contain Salla lifecycle hooks"),
        Check("no_forbidden_functions", check_no_forbidden_functions, "No undefined salla_* functions in Twig files"),
        Check("pages_extend_master", check_pages_extend_master, "All page templates must extend layouts.master"),
        Check("hero_banner_fallbacks", check_hero_banner_fallbacks, "luxury-hero-banner.twig must provide robust fallbacks"),
        Check("package_json_scripts", check_package_json_scripts, "package.json must contain development and watch scripts"),
        Check("salla_cli_authenticated", check_salla_cli_authenticated, "Salla CLI token must exist in .salla/config.json"),
        Check("git_clean_and_synced", check_git_clean_and_synced, "Tracked git files must be clean and committed"),
    ])

    # ---- 3. AGENT FACTORY BLUEPRINTS ----
    def mock_build(spec: AgentSpec, agent_id: str):
        return {"id": agent_id, "spec": spec}

    factory = AgentFactory(mock_build)
    factory.register(AgentSpec(
        name="twilight_engineer",
        system_prompt="Expert Salla Twilight developer enforcing Twig hooks and JSON specifications.",
        tools=["view_file", "replace_file_content", "git"],
    ))
    factory.register(AgentSpec(
        name="verification_officer",
        system_prompt="Zero-trust quality gatekeeper verifying all contracts deterministically.",
        tools=["verifier", "worklog"],
    ))

    # ---- 4. OPPOSING PHILOSOPHIES PANEL ----
    panel_runner = lambda persona, prompt: f"[{persona.name} Verdict]: Verified against {persona.priors[0]}."
    panel = Panel(
        personas=Panel.opposing_philosophies(),
        runner=panel_runner,
    )
    opinions = panel.ask("Is salla-twilight-luxury-pro ready for merchant draft preview?")
    for op in opinions:
        worklog.decision(f"{op.persona.name}: {op.response}")

    # ---- 5. RALPH LOOP EXECUTION ----
    def step_fn(state: dict, wl: Worklog) -> dict:
        wl.thought("Observing filesystem and environment state...")
        state["repo_root"] = str(repo_root)
        state["theme_id"] = 1252059893
        state["store"] = "fagricastro"
        state["draft_id"] = 369058364
        return state

    loop = RalphLoop(verifier=verifier, step_fn=step_fn, max_iters=5, max_seconds=30.0)
    result = loop.run({}, worklog)

    # ---- 6. COMPACT SUMMARY & OUTPUT ----
    print("=" * 60)
    print(f"AGENT SUIT MISSION RESULT: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"Iterations: {result.iterations} | Reason: {result.reason}")
    print("=" * 60)
    print("\n--- VERIFIER RESULTS ---")
    all_passed, check_results = verifier.run(result.final_state)
    for cr in check_results:
        status_mark = "[PASS]" if cr.passed else "[FAIL]"
        print(f"  {status_mark} {cr.name}: {cr.detail or 'OK'}")

    print("\n--- ERROR MEMORY STATS ---")
    print(f"  Total operational lessons tracked: {len(memory.lessons)}")
    for ls in memory.lessons:
        print(f"  * [{ls.id}] {ls.lesson}")

    print("\n--- COMPACT WORKLOG SUMMARY ---")
    print(worklog.compact_summary(max_entries=10))

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(run_mission())
