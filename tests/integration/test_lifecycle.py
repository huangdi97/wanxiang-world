"""G06A: persistent lifecycle, pause/advance/background and budgets."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.lifecycle.errors import InvalidLifecycleTransition
from wanxiang_substrate.lifecycle.model import can_transition
from wanxiang_substrate.lifecycle.resolver import register_lifecycle_resolvers
from wanxiang_substrate.lifecycle.service import LifecycleService
from wanxiang_substrate.recovery.budget import BudgetTracker, ResourceBudget
from wanxiang_substrate.recovery.errors import BudgetExceeded
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component
from wanxiang_substrate.temporal.query import TemporalQuery
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

INSTANCE = WorldInstanceId("wld_life")
TOWN = EntityId("town")


def make_life_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_temporal_resolvers(registry)
        register_lifecycle_resolvers(registry)
        registry.register("life.instantiate", _instantiate)

    return make_world_runtime(path, extra_resolvers=register)


def _instantiate(command: CommandEnvelope, state: object) -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(entity_id=TOWN, entity_type="spatial.place", components=()),
        )
    )


@pytest.fixture
def life_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_life_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_life_instantiate"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="life.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.unit
def test_transition_permissions() -> None:
    assert can_transition("PAUSED", "REALTIME") is True
    assert can_transition("PAUSED", "FULL_AUTONOMY") is False
    assert can_transition("REALTIME", "PAUSED") is True
    assert can_transition("FULL_AUTONOMY", "BATCH_SIMULATION") is True
    assert can_transition("BATCH_SIMULATION", "FULL_AUTONOMY") is False


@pytest.mark.integration
def test_pause_stops_advancement_without_losing_state(
    life_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = life_world
    service = LifecycleService(runtime, INSTANCE, w.root_branch_id)
    service.set_mode("PAUSED")
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    before = TemporalQuery(state).now()
    # A paused world refuses further time advancement through the gate.
    with pytest.raises(InvalidLifecycleTransition):
        service.set_mode("FULL_AUTONOMY")
    service.set_mode("REALTIME")
    service.advance(5)
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert TemporalQuery(state).now() == before + 5


@pytest.mark.integration
def test_background_mode_advances_without_active_session(
    life_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = life_world
    service = LifecycleService(runtime, INSTANCE, w.root_branch_id)
    service.set_mode("BACKGROUND_SIMULATION")
    service.advance(10)
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert TemporalQuery(state).now() == 10


@pytest.mark.integration
def test_lifecycle_recovers_deterministically(
    life_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = life_world
    service = LifecycleService(runtime, INSTANCE, w.root_branch_id)
    service.set_mode("ACCELERATED")
    service.advance(3)
    assert service.current().mode == "ACCELERATED"
    assert service.current().tick == 3


@pytest.mark.unit
def test_budget_blocks_runaway_loop() -> None:
    tracker = BudgetTracker(ResourceBudget(max_commands=5, max_ticks=100))
    for _ in range(5):
        tracker.consume(commands=1)
    with pytest.raises(BudgetExceeded):
        tracker.consume(commands=1)
    assert tracker.remaining()["commands"] == 0


@pytest.mark.integration
def test_catch_up_policy_after_downtime(
    life_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = life_world
    service = LifecycleService(runtime, INSTANCE, w.root_branch_id)
    service.set_mode("REALTIME")
    reached = service.catch_up(target_ticks=40)
    assert reached == 40
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert TemporalQuery(state).now() == 40
