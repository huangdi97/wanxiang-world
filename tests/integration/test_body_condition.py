"""G02D: body/condition constraints block otherwise-valid actions."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator, Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ActorId, BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.body.errors import BodyConstraintViolation, InvalidConditionRange
from wanxiang_substrate.body.fixture import (
    HEALTHY,
    TIRED,
    build_condition_fixture_commands,
)
from wanxiang_substrate.body.query import BodyQuery
from wanxiang_substrate.body.resolver import (
    ACTION_APPLY_CONDITION,
    ACTION_EXERT,
    ACTION_REST,
    ACTION_SET_VISIBILITY,
    register_body_resolvers,
)
from wanxiang_substrate.spatial.fixture import (
    build_house_fixture_commands,
)
from wanxiang_substrate.spatial.resolver import register_spatial_resolvers

COMBINED = WorldInstanceId("wld_combined")


def make_body_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_spatial_resolvers(registry)
        register_body_resolvers(registry)

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
        instance_id=COMBINED,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=dict(payload),
        actor_id=ActorId(actor_id) if actor_id else None,
        world_time=WorldTime(revision + 1),
    )


@pytest.fixture
def body_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_body_runtime(path)
    w = runtime.create_world(instance_id=COMBINED)
    for command in build_house_fixture_commands(w.root_branch_id, instance_id=COMBINED):
        runtime.submit_command(command)
    for command in build_condition_fixture_commands(
        w.root_branch_id, start_revision=1, instance_id=COMBINED
    ):
        runtime.submit_command(command)
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_exert_and_rest_are_deterministic(
    body_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = body_world
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            ACTION_EXERT,
            {"actor_id": HEALTHY.value, "energy_cost": 30},
            "cmd_exert",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    condition = BodyQuery(state).condition(HEALTHY)
    assert condition is not None and condition.energy == 60
    runtime.submit_command(
        cmd(w.root_branch_id, 3, ACTION_REST, {"actor_id": HEALTHY.value, "ticks": 25}, "cmd_rest")
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    condition = BodyQuery(state).condition(HEALTHY)
    assert condition is not None and condition.energy == 85


@pytest.mark.integration
def test_fatigued_actor_cannot_move_through_valid_path(
    body_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = body_world
    from wanxiang_substrate.spatial.fixture import KITCHEN

    # TIRED (energy 10) tries hall->kitchen (open door, valid spatial path).
    with pytest.raises(BodyConstraintViolation):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                2,
                "spatial.move",
                {"entity_id": TIRED.value, "target_place_id": KITCHEN.value},
                "cmd_move_tired",
                actor_id=TIRED.value,
            )
        )
    # Healthy actor can move freely.
    result = runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            "spatial.move",
            {"entity_id": HEALTHY.value, "target_place_id": KITCHEN.value},
            "cmd_move_healthy",
            actor_id=HEALTHY.value,
        )
    )
    assert BodyQuery(result.state).condition(HEALTHY) is not None


@pytest.mark.integration
def test_invalid_condition_range_rejected(
    body_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = body_world
    with pytest.raises(InvalidConditionRange):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                2,
                ACTION_APPLY_CONDITION,
                {"actor_id": HEALTHY.value, "energy": 150},
                "cmd_bad",
            )
        )


@pytest.mark.integration
def test_condition_evolution_replays_deterministically(
    body_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = body_world
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            ACTION_EXERT,
            {"actor_id": HEALTHY.value, "energy_cost": 20},
            "cmd_e1",
        )
    )
    runtime.submit_command(
        cmd(w.root_branch_id, 3, ACTION_REST, {"actor_id": HEALTHY.value, "ticks": 10}, "cmd_r1")
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    events = runtime.events(w.instance_id, w.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == state.semantic_hash()
    condition = BodyQuery(replayed).condition(HEALTHY)
    assert condition is not None and condition.energy == 80


@pytest.mark.integration
def test_private_condition_facet_excluded_from_public_projection(
    body_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = body_world
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            2,
            ACTION_APPLY_CONDITION,
            {"actor_id": TIRED.value, "pain": 90},
            "cmd_pain",
        )
    )
    runtime.submit_command(
        cmd(
            w.root_branch_id,
            3,
            ACTION_SET_VISIBILITY,
            {"actor_id": TIRED.value, "private": "pain"},
            "cmd_vis",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = BodyQuery(state)
    # Authorized view includes pain; public projection excludes it.
    authorized = query.condition(TIRED)
    assert authorized is not None and authorized.pain == 90
    public = query.public_condition(TIRED)
    assert "pain" not in public
