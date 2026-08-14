"""G19D: cognitive LOD & large-population scheduling research.

- LOD transition preserves identity/required obligations.
- Declared scale profile improves resource use without invariant failures.
- Benchmark is reproducible.
"""

from __future__ import annotations

from wanxiang_research.cognitive_lod import Actor, CognitiveLodScheduler


def test_lod_transition_preserves_identity_and_obligations() -> None:
    sched = CognitiveLodScheduler()
    sched.register(Actor("a1", tier="active", obligations=("guard_rounds",)))
    sched.set_tier("a1", "dormant")
    sched.wake("a1", "intruder")
    actor = sched.actor("a1")
    assert actor.actor_id == "a1"
    assert actor.obligations == ("guard_rounds",)  # obligation preserved
    assert actor.tier == "active"  # event-driven wakeup promoted
    assert sched.wakeup_count("a1") == 1


def test_scale_profile_improves_resource_use() -> None:
    sched = CognitiveLodScheduler()
    for i in range(100):
        sched.register(Actor(f"p{i}", tier="dormant"))
    sched.register(Actor("lead", tier="active", obligations=("lead",)))
    # Dormant crowd costs no resource budget; only the active leader does.
    assert sched.resource_cost() == 4
    # Demoting the leader to dormant drops cost to zero.
    sched.demote("lead", "dormant")
    assert sched.resource_cost() == 0
    # Waking one crowd member does not silently delete or duplicate anyone.
    before = sched.active_count()
    sched.wake("p10", "event")
    assert sched.active_count() == before + 1
    assert sched.actor("p10").actor_id == "p10"


def test_benchmark_reproducible() -> None:
    def run() -> list[int]:
        sched = CognitiveLodScheduler()
        for i in range(50):
            sched.register(Actor(f"p{i}", tier="dormant"))
        for i in range(0, 50, 5):
            sched.wake(f"p{i}", "market_day")
            sched.demote(f"p{i}", "dormant")
        return [sched.wakeup_count(f"p{i}") for i in range(0, 50, 5)]

    assert run() == run()  # deterministic benchmark
