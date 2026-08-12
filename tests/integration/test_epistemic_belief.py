"""G03B: belief/memory evolution with corrections, privacy and replay."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator, Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.epistemic.errors import MemoryAccessDenied
from wanxiang_substrate.epistemic.fixture import (
    ACTOR,
    BELIEF_RUMOR,
    INSTANCE,
    build_rumor_fixture_commands,
)
from wanxiang_substrate.epistemic.query import EpistemicQuery
from wanxiang_substrate.epistemic.resolver import register_epistemic_resolvers


def make_epistemic_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_epistemic_resolvers(registry)

    return make_world_runtime(path, extra_resolvers=register)


def cmd(
    branch: BranchId,
    revision: int,
    action: str,
    payload: Mapping[str, FieldValue],
    command_id: str,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=INSTANCE,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        world_time=WorldTime(revision + 1),
    )


@pytest.fixture
def rumor_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_epistemic_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    for command in build_rumor_fixture_commands(w.root_branch_id):
        runtime.submit_command(command)
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_rumor_then_correction_keeps_lineage(
    rumor_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = rumor_world
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = EpistemicQuery(state, now_ticks=10)
    assert query.active_belief(ACTOR, "treasure_is_in_the_cellar").belief_id == BELIEF_RUMOR  # type: ignore[union-attr]

    # Correct the rumor belief with higher confidence.
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "epistemic.correct_belief",
            {
                "belief_id": BELIEF_RUMOR.value,
                "new_belief_id": "belief_correction",
                "actor_id": ACTOR.value,
                "proposition": "treasure_is_in_the_cellar",
                "confidence": 0.9,
                "at_ticks": 30,
            },
            "cmd_correct",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = EpistemicQuery(state, now_ticks=30)
    active = query.active_belief(ACTOR, "treasure_is_in_the_cellar")
    assert active is not None and active.belief_id == EntityId("belief_correction")
    assert active.supersedes == BELIEF_RUMOR
    history = query.belief_history(ACTOR, "treasure_is_in_the_cellar")
    assert len(history) == 2
    corrected = query.belief(BELIEF_RUMOR)
    assert corrected is not None and corrected.status == "corrected"
    assert corrected.corrected_by == EntityId("belief_correction")


@pytest.mark.integration
def test_contradictory_beliefs_are_retained(
    rumor_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = rumor_world
    # Adopt a contradictory belief (different proposition value) ? both retained.
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "epistemic.adopt_belief",
            {
                "belief_id": "belief_elsewhere",
                "actor_id": ACTOR.value,
                "proposition": "treasure_is_in_the_garden",
                "confidence": 0.5,
                "at_ticks": 20,
            },
            "cmd_b2",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = EpistemicQuery(state, now_ticks=20)
    assert query.active_belief(ACTOR, "treasure_is_in_the_cellar") is not None
    assert query.active_belief(ACTOR, "treasure_is_in_the_garden") is not None


@pytest.mark.integration
def test_forget_marks_memory_and_compaction_bounds(
    rumor_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = rumor_world
    runtime.submit_command(
        cmd(w.root_branch_id, 1, "epistemic.forget", {"memory_id": "memory_rumor"}, "cmd_forget")
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = EpistemicQuery(state, now_ticks=10)
    assert not any(m.memory_id == EntityId("memory_rumor") for m in query.memories(ACTOR))
    assert any(
        m.memory_id == EntityId("memory_rumor")
        for m in query.memories(ACTOR, include_forgotten=True)
    )
    # Compaction keeps the most salient and archives the rest (lineage preserved).
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            "epistemic.compact_memory",
            {"actor_id": ACTOR.value, "keep": 1},
            "cmd_compact",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = EpistemicQuery(state, now_ticks=10)
    active_memories = query.memories(ACTOR)
    assert len(active_memories) <= 1
    # Audit lineage preserved: forgotten records still retrievable with flag.
    assert len(query.memories(ACTOR, include_forgotten=True)) >= 2


@pytest.mark.integration
def test_memory_access_is_authorized(rumor_world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = rumor_world
    stranger = EntityId("stranger")
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = EpistemicQuery(state, now_ticks=10)
    with pytest.raises(MemoryAccessDenied):
        query.require_memory_access(ACTOR, stranger)
    # Grant access then it works.
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "epistemic.grant_memory_access",
            {"owner_id": ACTOR.value, "authorized_actor": stranger.value},
            "cmd_grant",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = EpistemicQuery(state, now_ticks=10)
    query.require_memory_access(ACTOR, stranger)
    assert query.can_read_memory(ACTOR, stranger) is True


@pytest.mark.integration
def test_belief_adoption_never_creates_canonical_facts(
    rumor_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = rumor_world
    before_entities = len(runtime.current_state(w.instance_id, w.root_branch_id).entities())
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "epistemic.adopt_belief",
            {
                "belief_id": "belief_claim",
                "actor_id": ACTOR.value,
                "proposition": "alice_owns_a_sword",
                "confidence": 0.6,
                "at_ticks": 40,
            },
            "cmd_claim",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    # Only the new belief entity was added; no material item / person appeared.
    from wanxiang_substrate.material.query import MaterialQuery

    assert MaterialQuery(state).item(EntityId("sword")) is None
    assert len(state.entities()) == before_entities + 1


@pytest.mark.integration
def test_epistemic_graph_replays(rumor_world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = rumor_world
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "epistemic.correct_belief",
            {
                "belief_id": BELIEF_RUMOR.value,
                "new_belief_id": "belief_correction",
                "actor_id": ACTOR.value,
                "proposition": "treasure_is_in_the_cellar",
                "confidence": 0.9,
                "at_ticks": 30,
            },
            "cmd_correct",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    events = runtime.events(w.instance_id, w.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == state.semantic_hash()
    query = EpistemicQuery(replayed, now_ticks=30)
    active = query.active_belief(ACTOR, "treasure_is_in_the_cellar")
    assert active is not None and active.belief_id == EntityId("belief_correction")
