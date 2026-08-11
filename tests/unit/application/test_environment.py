"""GOAL_01F: WorldEnvironment facade honest subset (in-memory adapters)."""

from __future__ import annotations

import pytest
from wanxiang_application.environment import WorldEnvironment
from wanxiang_application.ports import PersistenceBundle
from wanxiang_application.synthetic_microworld import register_synthetic_resolvers
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.branch import InMemoryBranchRepository
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.snapshot import InMemorySnapshotStore


class MemoryInstanceStore:
    """Tiny in-memory instance store for unit tests."""

    def __init__(self) -> None:
        self._rows: dict[str, tuple[int, int, int]] = {}

    def create(
        self,
        instance_id: WorldInstanceId,
        schema_version: SchemaVersion,
        rule_version: RuntimeVersion,
        created_world_time: WorldTime,
    ) -> None:
        self._rows[instance_id.value] = (
            schema_version.value,
            rule_version.value,
            created_world_time.ticks,
        )

    def get(self, instance_id: WorldInstanceId) -> tuple[SchemaVersion, RuntimeVersion, WorldTime]:
        schema, rule, created = self._rows[instance_id.value]
        return SchemaVersion(schema), RuntimeVersion(rule), WorldTime(created)


def make_in_memory_runtime() -> WorldRuntime:
    registry = ResolverRegistry()
    register_synthetic_resolvers(registry)
    return WorldRuntime(
        PersistenceBundle(
            event_store=InMemoryEventStore(),
            snapshot_store=InMemorySnapshotStore(),
            branches=InMemoryBranchRepository(),
            instances=MemoryInstanceStore(),
        ),
        RuntimeVersion(1),
        resolvers=registry,
    )


@pytest.mark.unit
def test_environment_create_observe_step() -> None:
    env = WorldEnvironment(make_in_memory_runtime())
    world = env.create(instance_id=WorldInstanceId("wld_env"))
    env.step(
        world.instance_id,
        world.root_branch_id,
        "create_entity",
        {"entity_id": "alice", "count": 10},
        expected_revision=0,
    )
    observed = env.observe(world.instance_id, world.root_branch_id)
    assert observed["revision"] == 1
    assert env.legal_actions() == ("create_entity", "set_status", "transfer_resource")
    assert env.metrics(world.instance_id)["events"] == 1
    env.close()


@pytest.mark.unit
def test_environment_checkpoint_restore_branch() -> None:
    env = WorldEnvironment(make_in_memory_runtime())
    world = env.create(instance_id=WorldInstanceId("wld_env2"))
    env.step(
        world.instance_id,
        world.root_branch_id,
        "create_entity",
        {"entity_id": "alice", "count": 10},
        expected_revision=0,
    )
    env.checkpoint(world.instance_id, world.root_branch_id)
    restored = env.restore(world.instance_id, world.root_branch_id)
    assert restored["used_snapshot"] is True
    child = env.branch(world.instance_id, world.root_branch_id)
    assert child.ancestry.parent_branch_id == world.root_branch_id
