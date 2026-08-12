"""G03A: observation & perspective isolation through the authoritative path."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator, Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ActorId, BranchId, CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.material.resolver import register_material_resolvers
from wanxiang_substrate.observation.fixture import (
    ALICE,
    BOB,
    INSTANCE,
    KITCHEN,
    build_confidential_fixture_commands,
)
from wanxiang_substrate.observation.model import Observation
from wanxiang_substrate.observation.query import PerspectiveService
from wanxiang_substrate.observation.resolver import register_observation_resolvers
from wanxiang_substrate.spatial.resolver import register_spatial_resolvers
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers


def make_obs_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_spatial_resolvers(registry)
        register_material_resolvers(registry)
        register_temporal_resolvers(registry)
        register_observation_resolvers(registry)

    return make_world_runtime(path, extra_resolvers=register)


def cmd(
    branch: BranchId,
    revision: int,
    action: str,
    payload: Mapping[str, FieldValue],
    command_id: str,
    actor_id: str | None = None,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=INSTANCE,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        actor_id=ActorId(actor_id) if actor_id else None,
        world_time=WorldTime(revision + 1),
    )


@pytest.fixture
def obs_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_obs_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    for command in build_confidential_fixture_commands(w.root_branch_id):
        runtime.submit_command(command)
    yield runtime, w
    cleanup_db_file(path)


def _observations(
    runtime: WorldRuntime, w: CreateWorldResult, observer: str
) -> tuple[Observation, ...]:
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    events = runtime.events(w.instance_id, w.root_branch_id)
    return PerspectiveService(state).context_for(EntityId(observer), events)


@pytest.mark.integration
def test_actor_in_same_place_observes_movement(
    obs_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = obs_world
    # Alice (hall) moves to kitchen; Bob (kitchen) sees her arrive visually.
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "spatial.move",
            {"entity_id": ALICE.value, "target_place_id": KITCHEN.value},
            "cmd_move",
            actor_id=ALICE.value,
        )
    )
    observations = _observations(runtime, w, BOB.value)
    assert observations
    movement = [o for o in observations if o.fact.kind == "movement"]
    assert movement
    assert movement[0].rule_refs and "visual" in movement[0].rule_refs[0]


@pytest.mark.integration
def test_sealed_payload_content_never_leaks(
    obs_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = obs_world
    # Alice (hall) sees the messenger hold the letter; the confidential payload
    # content must not appear in any observation.
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "spatial.move",
            {"entity_id": ALICE.value, "target_place_id": KITCHEN.value},
            "cmd_move",
            actor_id=ALICE.value,
        )
    )
    observations = _observations(runtime, w, BOB.value)
    for obs in observations:
        rendered = repr(obs.fact)
        assert "confidential" not in rendered
        assert "body" not in rendered or "ref://" not in rendered


@pytest.mark.integration
def test_actor_outside_zone_cannot_observe(
    obs_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = obs_world
    from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.state import InMemoryCanonicalState, apply_delta
    from wanxiang_substrate.observation.query import PerspectiveService
    from wanxiang_substrate.spatial.components import place_component, position_component
    from wanxiang_substrate.spatial.fixture import HALL

    # Build an in-memory state: a house (hall+kitchen, open door) and an
    # isolated cellar with an observer and NO portal connection.
    base_state = apply_delta(
        InMemoryCanonicalState(
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            revision=BranchRevision(0),
            schema_version=SchemaVersion(1),
            rule_version=RuntimeVersion(1),
        ),
        ProposedWorldDelta(
            operations=(
                EntityCreate(
                    entity_id=HALL,
                    entity_type="spatial.place",
                    components=(place_component(EntityId("house"), "hall"),),
                ),
                EntityCreate(
                    entity_id=KITCHEN,
                    entity_type="spatial.place",
                    components=(place_component(EntityId("house"), "kitchen"),),
                ),
                EntityCreate(
                    entity_id=EntityId("door_hk"),
                    entity_type="spatial.portal",
                    components=(
                        __import__(
                            "wanxiang_substrate.spatial.components", fromlist=["portal_component"]
                        ).portal_component(HALL, KITCHEN, state="open"),
                    ),
                ),
                EntityCreate(
                    entity_id=EntityId("cellar"),
                    entity_type="spatial.place",
                    components=(place_component(EntityId("house"), "cellar"),),
                ),
                EntityCreate(
                    entity_id=EntityId("eve"),
                    entity_type="person",
                    components=(position_component(EntityId("eve"), EntityId("cellar")),),
                ),
                EntityCreate(
                    entity_id=ALICE,
                    entity_type="person",
                    components=(position_component(ALICE, HALL),),
                ),
            )
        ),
    )
    # A move by Alice in the house produces an event; Eve in the cellar cannot
    # perceive it (disconnected, no line of sight / acoustic path).
    event = runtime.events(w.instance_id, w.root_branch_id)[0]
    from wanxiang_domain.event import CommittedEvent

    move_event = CommittedEvent(
        event_id=event.event_id,
        instance_id=event.instance_id,
        branch_id=event.branch_id,
        event_seq=event.event_seq,
        revision=event.revision,
        schema_version=event.schema_version,
        command_id=event.command_id,
        delta=__import__(
            "wanxiang_domain.delta", fromlist=["ProposedWorldDelta"]
        ).ProposedWorldDelta(
            operations=(
                __import__("wanxiang_domain.delta", fromlist=["EntityUpdate"]).EntityUpdate(
                    entity_id=ALICE,
                    components=(
                        __import__(
                            "wanxiang_substrate.spatial.components", fromlist=["position_component"]
                        ).position_component(ALICE, KITCHEN),
                    ),
                ),
            )
        ),
        world_time=event.world_time,
        rule_version=event.rule_version,
        actor_id=event.actor_id,
    )
    observations = PerspectiveService(base_state).context_for(EntityId("eve"), (move_event,))
    assert observations == ()
    # Alice herself (same place as the move start) does observe it.
    alice_obs = PerspectiveService(base_state).context_for(ALICE, (move_event,))
    assert alice_obs


@pytest.mark.integration
def test_branch_perspectives_differ_only_when_events_justify(
    obs_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = obs_world
    # Parent commits a move; child commits an extra announcement.
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "spatial.move",
            {"entity_id": ALICE.value, "target_place_id": KITCHEN.value},
            "cmd_move",
            actor_id=ALICE.value,
        )
    )
    parent_events = runtime.events(w.instance_id, w.root_branch_id)
    child = runtime.create_branch(w.instance_id, w.root_branch_id)
    state = runtime.current_state(w.instance_id, child.branch_id)
    child_rev = state.revision.value
    runtime.submit_command(
        cmd(
            child.branch_id,
            child_rev,
            "observation.announce",
            {"actor_id": BOB.value, "message": "kitchen ready"},
            "cmd_ann",
            actor_id=BOB.value,
        )
    )
    child_events = runtime.events(w.instance_id, child.branch_id)
    parent_perspective = PerspectiveService(
        runtime.current_state(w.instance_id, w.root_branch_id)
    ).context_for(BOB, parent_events)
    child_perspective = PerspectiveService(
        runtime.current_state(w.instance_id, child.branch_id)
    ).context_for(BOB, child_events)
    assert len(child_perspective) > len(parent_perspective)
    assert any(o.fact.kind == "announcement" for o in child_perspective)
    assert not any(o.fact.kind == "announcement" for o in parent_perspective)


@pytest.mark.integration
def test_private_visibility_hides_event(obs_world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = obs_world
    # Mark Alice private, then Alice moves; Bob must not observe it.
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            1,
            "observation.set_visibility",
            {"entity_id": ALICE.value, "level": "private"},
            "cmd_vis",
            actor_id=ALICE.value,
        )
    )
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            "spatial.move",
            {"entity_id": ALICE.value, "target_place_id": KITCHEN.value},
            "cmd_move",
            actor_id=ALICE.value,
        )
    )
    observations = _observations(runtime, w, BOB.value)
    assert not any(
        o.fact.kind == "movement" and o.fact.subject == ALICE.value for o in observations
    )
