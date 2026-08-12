"""G03D: affordances + validated action hands candidate to resolver."""

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
from wanxiang_substrate.actions.affordance import compute_affordances
from wanxiang_substrate.actions.registry import ActionRegistry, register_reference_actions
from wanxiang_substrate.actions.validator import ActionValidator
from wanxiang_substrate.body.resolver import register_body_resolvers
from wanxiang_substrate.material.resolver import register_material_resolvers
from wanxiang_substrate.observation.fixture import (
    ALICE,
    BOB,
    INSTANCE,
    LETTER,
    build_confidential_fixture_commands,
)
from wanxiang_substrate.observation.resolver import register_observation_resolvers
from wanxiang_substrate.spatial.resolver import register_spatial_resolvers
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers


def make_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_spatial_resolvers(registry)
        register_material_resolvers(registry)
        register_temporal_resolvers(registry)
        register_observation_resolvers(registry)
        register_body_resolvers(registry)

    return make_world_runtime(path, extra_resolvers=register)


def cmd(
    branch: BranchId,
    revision: int,
    action: str,
    payload: Mapping[str, FieldValue],
    command_id: str,
    actor: str | None = None,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=INSTANCE,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        actor_id=ActorId(actor) if actor else None,
        world_time=WorldTime(revision + 1),
    )


@pytest.fixture
def world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    for command in build_confidential_fixture_commands(w.root_branch_id):
        runtime.submit_command(command)
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_validated_move_candidate_commits(world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = world
    registry = ActionRegistry()
    register_reference_actions(registry)
    validator = ActionValidator(registry)
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    command = cmd(
        w.root_branch_id,
        1,
        "spatial.move",
        {"entity_id": ALICE.value, "target_place_id": "kitchen"},
        "cmd_v",
        actor=ALICE.value,
    )
    result = validator.validate(command, state)
    assert result.ok is True, result.issues
    runtime.submit_command(command)
    from wanxiang_substrate.spatial.query import SpatialQuery

    after = runtime.current_state(w.instance_id, w.root_branch_id)
    assert SpatialQuery(after).location(ALICE) == EntityId("kitchen")


@pytest.mark.integration
def test_affordances_available_for_actor(world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = world
    registry = ActionRegistry()
    register_reference_actions(registry)
    validator = ActionValidator(registry)
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    affordances = compute_affordances(ALICE, state, registry, validator)
    by_type = {a.action_type: a for a in affordances}
    assert by_type["body.rest"].available is False  # alice has no body condition in this fixture
    assert by_type["spatial.move"].available is True  # alice is in hall; reachable targets exist


@pytest.mark.integration
def test_invisible_knowledge_reference_rejected(
    world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = world
    registry = ActionRegistry()
    register_reference_actions(registry)
    validator = ActionValidator(registry)
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    # Bob has no knowledge of the confidential letter (not custodian, no memory).
    command = cmd(
        w.root_branch_id,
        1,
        "material.read_payload",
        {"item_id": LETTER.value, "reader_id": BOB.value},
        "cmd_r",
        actor=BOB.value,
    )
    result = validator.validate(command, state)
    assert result.ok is False
    assert any(i.code == "no_knowledge" for i in result.issues)
