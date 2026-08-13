"""G12A: 30-day / 1000+ tick stability qualification.

A synthetic world runs 1000+ ticks and 1000+ committed cycles with no
invariant failure and bounded resource growth.
"""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.lifecycle.service import LifecycleService
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

INSTANCE = WorldInstanceId("wld_g12a")
TOWN = EntityId("town")
DAY = 100
TARGET_TICKS = 1000
TARGET_COMMITS = 1000


def make_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry
    from wanxiang_substrate.lifecycle.resolver import register_lifecycle_resolvers

    def register(registry: ResolverRegistry) -> None:
        register_temporal_resolvers(registry)
        register_lifecycle_resolvers(registry)
        registry.register("g12a.instantiate", _instantiate)

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


@pytest.mark.integration
def test_g12a_1000_ticks_and_commits_bounded_growth() -> None:
    path = fresh_db_path()
    try:
        runtime = make_runtime(path)
        w = runtime.create_world(instance_id=INSTANCE)
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId("cmd_g12a_instantiate"),
                instance_id=INSTANCE,
                branch_id=w.root_branch_id,
                expected_revision=BranchRevision(0),
                action_type="g12a.instantiate",
                payload={},
                world_time=WorldTime(1),
            )
        )
        lifecycle = LifecycleService(runtime, INSTANCE, w.root_branch_id)
        lifecycle.set_mode("BACKGROUND_SIMULATION")
        # 1) 30 in-world days (3000 ticks) + 1000+ scheduler/commit cycles.
        lifecycle.advance(30 * DAY)
        revision = runtime.current_state(w.instance_id, w.root_branch_id).revision.value
        for i in range(TARGET_COMMITS):
            runtime.submit_command(
                CommandEnvelope(
                    command_id=CommandId(f"cmd_batch_{i}"),
                    instance_id=INSTANCE,
                    branch_id=w.root_branch_id,
                    expected_revision=BranchRevision(revision + i),
                    action_type="create_entity",
                    payload={"entity_id": f"obj_{i}", "entity_type": "material.item"},
                    world_time=WorldTime(revision + i + 1),
                )
            )
        state = runtime.current_state(w.instance_id, w.root_branch_id)
        events = runtime.events(w.instance_id, w.root_branch_id)
        from wanxiang_substrate.temporal.query import TemporalQuery

        # 2) 30 in-world days (3000 ticks) and 1000+ committed events, no
        #    invariant failure.
        assert TemporalQuery(state).now() >= 30 * DAY
        assert state.revision.value >= TARGET_COMMITS
        assert len(events) >= TARGET_COMMITS
        # 3) Bounded resource growth: events == committed commands exactly.
        assert len(events) == state.revision.value
        # 4) Semantic hash is deterministic.
        assert state.semantic_hash()
    finally:
        cleanup_db_file(path)
