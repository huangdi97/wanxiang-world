"""G92E SimulationLOD transition and aggregate tests."""

from __future__ import annotations

from wanxiang_substrate.long_horizon import (
    ActorActivityInput,
    LODState,
    SimulationLODRuntime,
)


def test_activity_scoring_selects_all_lod_levels() -> None:
    runtime = SimulationLODRuntime()

    def level(activity: ActorActivityInput) -> str:
        return runtime.policy.level_for(runtime.score(activity).score)

    assert level(ActorActivityInput("a", 10, 10, 1, 1, 1)) == "L0"
    assert level(ActorActivityInput("a", 10, 10, 1, 0, 0)) == "L1"
    assert level(ActorActivityInput("a", 10, 10, 0, 0, 1)) == "L2"
    assert level(ActorActivityInput("a", 1001, 0, 0, 0, 1)) == "L3"
    assert level(ActorActivityInput("a", 1001, 0, 0, 0, 0)) == "L4"


def test_lod_transition_and_promotion_preserve_state_ref() -> None:
    runtime = SimulationLODRuntime()
    state = LODState("alice", "L0", "state-hash", "memory-summary")
    low = runtime.score(ActorActivityInput("alice", 1001, 0, 0, 0, 1))
    transition = runtime.transition(state, low)
    assert transition.to_level == "L3"
    assert transition.state_ref == state.state_ref
    promoted = runtime.promote_to_active(
        LODState("alice", transition.to_level, transition.state_ref, state.memory_summary_ref),
        runtime.score(ActorActivityInput("alice", 100, 100, 1, 1, 1)),
    )
    assert promoted.from_level == "L3" and promoted.to_level == "L0"
    assert promoted.state_ref == state.state_ref
    assert promoted.continuity_ref == transition.continuity_ref


def test_cohort_aggregation_retains_actor_and_state_refs() -> None:
    runtime = SimulationLODRuntime()
    states = (
        LODState("alice", "L3", "state-a", "memory-a"),
        LODState("bob", "L4", "state-b", "memory-b"),
    )
    scores = tuple(runtime.score(ActorActivityInput(actor, 1001, 0)) for actor in ("alice", "bob"))
    aggregate = runtime.aggregate("cohort-1", states, scores)
    assert aggregate.level == "L3"
    assert aggregate.actor_ids == ("alice", "bob")
    assert aggregate.state_refs == ("state-a", "state-b")
