"""
panel_and_factory.py — show the panel-of-opposing-philosophies + factory.

A fake product decision: "should we ship a public beta with rate-limiting?"
Each persona argues from their priors. A judge reads and synthesizes.

No real LLM is called — we stub the runner so this is runnable offline.
The shape is what you'd plug into your own client.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from suit import Panel, Persona, AgentFactory, AgentSpec, SkillRegistry


# ---- stub LLM runner so the example is offline-runnable -----------------
def stub_runner(persona: Persona, prompt: str) -> str:
    p = persona.name
    if p == "Ship-Fast Founder":
        return ("Ship the beta today. Real users > perfect code. We can add limits in v2 "
                "once we know the real abuse patterns. Speed wins the market.")
    if p == "Security-Paranoid Architect":
        return ("DO NOT ship without rate-limiting and auth. One breach burns the brand "
                "for a decade. Ship private beta to 10 known users first. Deny-by-default.")
    if p == "User-Empathy Researcher":
        return ("Talk to 5 target users this week. Their actual usage will surprise you. "
                "What looks like abuse might be a real need we should support, not block.")
    if p == "Pragmatic Operator":
        return ("Ship the beta to a closed list (200 invites) WITH a simple per-user "
                "rate limit and a kill-switch. Boring tech, real dashboard, on-call rotation.")
    return "I have no opinion."


def judge_synthesis(opinions):
    """A tiny deterministic synthesizer. Replace with an LLM judge in prod."""
    text = "\n".join(f"- [{o.persona.name}]: {o.response}" for o in opinions)
    return (
        "Synthesis (judge):\n"
        "  Agreements: rate-limiting is needed; no panel wants to ship wide-open.\n"
        "  Conflict: Founder wants max speed; Architect wants minimum exposure.\n"
        "  Pragmatic + Researcher split the difference: closed beta + simple limits + user research.\n"
        "  Recommendation: ship closed beta (~200 invites) with per-user rate limit and a kill-switch.\n\n"
        f"Inputs considered:\n{text}"
    )


def main():
    # ---- factory with four blueprints -------------------------------------
    def build_fn(spec: AgentSpec, agent_id: str):
        # In real code, this would build a real client/agent object.
        return {"id": agent_id, "spec": spec}

    factory = AgentFactory(build_fn)
    for name, spec in AgentFactory.default_blueprints().items():
        factory.register(spec)

    researcher, _ = factory.build("researcher")
    critic, _    = factory.build("critic")
    print(f"spawned: {researcher['spec'].name} ({researcher['id']}), "
          f"{critic['spec'].name} ({critic['id']})\n")

    # ---- panel of opposing philosophies -----------------------------------
    panel = Panel(personas=Panel.opposing_philosophies(), runner=stub_runner)
    opinions = panel.ask("Should we ship a public beta with rate-limiting enabled?")

    print("=" * 60)
    print("PANEL OPINIONS")
    print("=" * 60)
    for o in opinions:
        print(f"\n[{o.persona.name}]")
        print(f"  priors: {'; '.join(o.persona.priors)}")
        print(f"  position: {o.response}")

    print("\n" + "=" * 60)
    print("JUDGE SYNTHESIS")
    print("=" * 60)
    print(judge_synthesis(opinions))

    # ---- skill registry sanity check --------------------------------------
    reg = SkillRegistry.starter_pack()
    print("\n--- applicable skills when last_error is set ---")
    applicable = reg.applicable({"last_error": "TypeError: bad arg"})
    for s in applicable:
        print(f"  - {s.name}: {s.description}")


if __name__ == "__main__":
    main()
