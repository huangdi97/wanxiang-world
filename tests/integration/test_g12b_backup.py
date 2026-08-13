"""G12B: backup/restore and migration qualification.

A SQLite world file is backed up, restored into a clean environment, and
replays to the identical canonical hash; the backup also migrates through the
declared Alembic path.
"""

from __future__ import annotations

import pathlib
import shutil

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine

INSTANCE = WorldInstanceId("wld_g12b")
TOWN = EntityId("town")


def make_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        registry.register("g12b.instantiate", _instantiate)

    return make_world_runtime(path, extra_resolvers=register)


def _instantiate(command: CommandEnvelope, state: object) -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(EntityCreate(entity_id=TOWN, entity_type="spatial.place", components=()),)
    )


@pytest.mark.integration
def test_g12b_backup_restore_replays_identical_hash() -> None:
    source = fresh_db_path()
    backup = fresh_db_path()
    try:
        runtime = make_runtime(source)
        w = runtime.create_world(instance_id=INSTANCE)
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId("cmd_g12b_instantiate"),
                instance_id=INSTANCE,
                branch_id=w.root_branch_id,
                expected_revision=BranchRevision(0),
                action_type="g12b.instantiate",
                payload={},
                world_time=WorldTime(1),
            )
        )
        for i in range(20):
            revision = runtime.current_state(w.instance_id, w.root_branch_id).revision.value
            runtime.submit_command(
                CommandEnvelope(
                    command_id=CommandId(f"cmd_b_{i}"),
                    instance_id=INSTANCE,
                    branch_id=w.root_branch_id,
                    expected_revision=BranchRevision(revision),
                    action_type="create_entity",
                    payload={"entity_id": f"obj_{i}", "entity_type": "material.item"},
                    world_time=WorldTime(revision + 1),
                )
            )
        expected_hash = runtime.current_state(w.instance_id, w.root_branch_id).semantic_hash()
        # 1) Backup the SQLite file.
        shutil.copy2(source, backup)
        # 2) Restore into a clean environment (fresh runtime on the backup).
        restored = make_runtime(backup)
        events = restored.events(INSTANCE, w.root_branch_id)
        replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
        assert replayed.semantic_hash() == expected_hash
        # 3) The backup migrates through the declared path (upgrade_db idempotent).
        from tests.conftest import upgrade_db

        upgrade_db(backup)
        restored_after = make_runtime(backup)
        events_after = restored_after.events(INSTANCE, w.root_branch_id)
        assert (
            ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events_after).semantic_hash()
            == expected_hash
        )
    finally:
        cleanup_db_file(source)
        cleanup_db_file(backup)
