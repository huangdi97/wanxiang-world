"""R7 Gate B: authoritative history replays when the snapshot store is absent."""

from __future__ import annotations

from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.experience_player_service import ExperiencePlayerService
from wanxiang_application.ports import PersistenceBundle
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.snapshot import InMemorySnapshotStore


def test_complete_history_rebuilds_same_state_with_fresh_empty_snapshot_store() -> None:
    original = build_reference_runtime()
    world = original.create_world(instance_id=WorldInstanceId("wld_r7_snapshotless"))
    player = ExperiencePlayerService(original)
    branch = world.root_branch_id
    player.act(
        world.instance_id,
        branch,
        0,
        "create_entity",
        {"entity_id": "ent_snapshotless", "count": 3},
        "act_snapshotless",
        "cmd_snapshotless_create",
    )
    player.act(
        world.instance_id,
        branch,
        1,
        "set_status",
        {"entity_id": "ent_snapshotless", "status": "awake"},
        "act_snapshotless",
        "cmd_snapshotless_status",
    )
    original.create_checkpoint(world.instance_id, branch)
    expected = original.current_state(world.instance_id, branch).semantic_hash()

    without_snapshots = WorldRuntime(
        PersistenceBundle(
            event_store=original.persistence.event_store,
            snapshot_store=InMemorySnapshotStore(),
            branches=original.persistence.branches,
            instances=original.persistence.instances,
            audit=original.persistence.audit,
        ),
        RuntimeVersion(1),
        schema_version=SchemaVersion(1),
    )
    restored = without_snapshots.restore_and_replay(world.instance_id, branch)

    assert restored.used_snapshot is False
    assert restored.snapshot_rejected is False
    assert restored.state.semantic_hash() == expected
    assert restored.state.revision.value == 2
