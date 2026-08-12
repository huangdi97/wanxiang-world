"""G02F: deterministic multi-rate autonomous scheduler (no user input)."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_substrate.body.resolver import register_body_resolvers
from wanxiang_substrate.institution.resolver import register_institution_resolvers
from wanxiang_substrate.population.errors import SchedulerBudgetExceeded
from wanxiang_substrate.population.fixture import DAY, INSTANCE, build_town_fixture_commands
from wanxiang_substrate.population.model import SchedulerConfig, SchedulerRunResult
from wanxiang_substrate.population.resolver import register_population_resolvers
from wanxiang_substrate.population.scheduler import AutonomousScheduler
from wanxiang_substrate.temporal.query import TemporalQuery
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers


def make_town_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_temporal_resolvers(registry)
        register_body_resolvers(registry)
        register_institution_resolvers(registry)
        register_population_resolvers(registry)

    return make_world_runtime(path, extra_resolvers=register)


@pytest.fixture
def town() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_town_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    for command in build_town_fixture_commands(w.root_branch_id):
        runtime.submit_command(command)
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_scheduler_advances_world_without_user_input(
    town: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = town
    scheduler = AutonomousScheduler(runtime, seed=42)
    result = scheduler.run(w.instance_id, w.root_branch_id, horizon_ticks=5 * DAY)
    assert result.events_submitted > 0
    assert result.ticks_advanced == 5 * DAY
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert TemporalQuery(state).now() == 5 * DAY


@pytest.mark.integration
def test_scheduler_is_deterministic() -> None:
    results: list[SchedulerRunResult] = []
    for _ in range(2):
        path = fresh_db_path()
        try:
            runtime = make_town_runtime(path)
            w = runtime.create_world(instance_id=INSTANCE)
            for command in build_town_fixture_commands(w.root_branch_id):
                runtime.submit_command(command)
            results.append(
                AutonomousScheduler(runtime, seed=7).run(
                    w.instance_id, w.root_branch_id, horizon_ticks=4 * DAY
                )
            )
        finally:
            cleanup_db_file(path)
    first, second = results
    assert first.events_submitted == second.events_submitted
    assert first.final_hash == second.final_hash


@pytest.mark.integration
def test_scheduler_respects_budget(town: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = town
    scheduler = AutonomousScheduler(
        runtime, seed=1, config=SchedulerConfig(total_event_budget=2, max_events_per_tick=1)
    )
    with pytest.raises(SchedulerBudgetExceeded):
        scheduler.run(w.instance_id, w.root_branch_id, horizon_ticks=2 * DAY)


@pytest.mark.integration
def test_duplicate_scheduled_command_does_not_duplicate_effect(
    town: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = town
    AutonomousScheduler(runtime, seed=3).run(w.instance_id, w.root_branch_id, horizon_ticks=DAY)
    event_count_before = len(runtime.events(w.instance_id, w.root_branch_id))
    assert event_count_before > 0
    # The M1 idempotency path rejects an exact duplicate command (same command id).
    from wanxiang_domain.command import CommandEnvelope
    from wanxiang_domain.hierarchy import BranchRevision
    from wanxiang_domain.ids import CommandId
    from wanxiang_domain.time import WorldTime

    events = runtime.events(w.instance_id, w.root_branch_id)
    first_event = events[0]
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    duplicate = CommandEnvelope(
        command_id=CommandId(first_event.command_id.value),
        instance_id=INSTANCE,
        branch_id=w.root_branch_id,
        expected_revision=BranchRevision(state.revision.value),
        action_type="body.rest",
        payload={"actor_id": "resident_a", "ticks": 5},
        world_time=WorldTime(state.revision.value + 1),
    )
    prior = runtime.submit_command(duplicate)
    assert prior.duplicate is True
    assert len(runtime.events(w.instance_id, w.root_branch_id)) == event_count_before


@pytest.mark.integration
def test_72h_micro_town_run_is_coherent_and_bounded(
    town: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = town
    scheduler = AutonomousScheduler(runtime, seed=99)
    result = scheduler.run(w.instance_id, w.root_branch_id, horizon_ticks=72 * DAY)
    assert result.ticks_advanced == 72 * DAY
    assert result.events_submitted > 100
    assert result.queue_stats["peak_tick_events"] <= 8
    # World clock reached the horizon; canonical state is replayable.
    events = runtime.events(w.instance_id, w.root_branch_id)
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.replay import ReplayEngine

    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert (
        replayed.semantic_hash()
        == runtime.current_state(w.instance_id, w.root_branch_id).semantic_hash()
    )
