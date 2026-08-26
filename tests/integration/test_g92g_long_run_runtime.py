"""G92G real SQLite 24h reference and seven-day multi-actor run."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_substrate.body.resolver import register_body_resolvers
from wanxiang_substrate.institution.resolver import register_institution_resolvers
from wanxiang_substrate.long_horizon import (
    CompactionPolicy,
    CompactionService,
    HorizonQualification,
    HorizonSample,
    state_storage_bytes,
)
from wanxiang_substrate.population.fixture import DAY, INSTANCE, build_town_fixture_commands
from wanxiang_substrate.population.resolver import register_population_resolvers
from wanxiang_substrate.population.scheduler import AutonomousScheduler
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers


def _register(registry: ResolverRegistry) -> None:
    register_temporal_resolvers(registry)
    register_body_resolvers(registry)
    register_institution_resolvers(registry)
    register_population_resolvers(registry)


def test_accelerated_reference_run_replays_recovers_and_stays_bounded(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    world = runtime.create_world(instance_id=INSTANCE)
    for command in build_town_fixture_commands(world.root_branch_id):
        runtime.submit_command(command)
    qualification = HorizonQualification("run-g92g-town")
    for day in range(1, 8):
        result = AutonomousScheduler(runtime, seed=9200 + day).run(
            INSTANCE, world.root_branch_id, horizon_ticks=day * DAY
        )
        runtime.create_checkpoint(INSTANCE, world.root_branch_id)
        state = runtime.current_state(INSTANCE, world.root_branch_id)
        replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(
            runtime.events(INSTANCE, world.root_branch_id)
        )
        if day in (1, 7):
            label = "24h" if day == 1 else "7d"
            actors = tuple(
                entity.entity_id.value
                for entity in state.entities()
                if entity.entity_type in ("person", "actor")
            )
            qualification.record(
                HorizonSample(
                    label,
                    day * DAY,
                    result.ticks_advanced,
                    actors,
                    len(runtime.events(INSTANCE, world.root_branch_id)),
                    day,
                    state_storage_bytes(state),
                    replayed.semantic_hash(),
                    runtime.restore_and_replay(
                        INSTANCE, world.root_branch_id
                    ).state.semantic_hash(),
                )
            )
    report = qualification.finish()
    events = runtime.events(INSTANCE, world.root_branch_id)
    final_state = runtime.current_state(INSTANCE, world.root_branch_id)
    snapshot = runtime.create_checkpoint(INSTANCE, world.root_branch_id)
    manifest = CompactionService(CompactionPolicy(retain_recent_events=8)).compact(
        events,
        snapshot,
        replay_hash_before=final_state.semantic_hash(),
        replay_hash_after=runtime.restore_and_replay(
            INSTANCE, world.root_branch_id
        ).state.semantic_hash(),
    )
    assert report.qualified is True
    assert report.multiple_actor_evidence is True
    assert manifest.replay_hash == final_state.semantic_hash()
    assert len(events) > 0
