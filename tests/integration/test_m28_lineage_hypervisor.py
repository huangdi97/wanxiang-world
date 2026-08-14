"""G31H: M28 gate ? parent isolation and multi-instance replay independence."""

from __future__ import annotations

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.lineage import LineageEdge, LineageGraph, LineageNode


def _cmd(
    instance_id: WorldInstanceId,
    branch_id: object,
    action: str,
    payload: dict[str, object],
    revision: int,
    cid: str,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(cid),
        instance_id=instance_id,
        branch_id=branch_id,  # type: ignore[arg-type]
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,  # type: ignore[arg-type]
        world_time=WorldTime(revision + 1),
    )


@pytest.mark.integration
def test_parent_not_modified_by_child_or_promotion() -> None:
    path = fresh_db_path()
    try:
        runtime = make_world_runtime(path)
        created = runtime.create_world()
        instance_id = created.instance_id
        root = created.root_branch_id
        runtime.submit_command(
            _cmd(
                instance_id, root, "create_entity", {"entity_id": "alice", "count": 10}, 0, "cmd_p1"
            )
        )
        parent_hash = runtime.current_state(instance_id, root).semantic_hash()
        parent_events = runtime.events(instance_id, root)

        # Fork a child (a worldline fork) and write to it.
        child = runtime.create_branch(instance_id, root)
        runtime.submit_command(
            _cmd(
                instance_id,
                child.branch_id,
                "create_entity",
                {"entity_id": "bob", "count": 5},
                1,
                "cmd_c1",
            )
        )
        # Lineage records the fork/promotion derivation (graph only, no history copy).
        graph = LineageGraph()
        graph.add_node(LineageNode(node_id=root.value, kind="worldline"))
        graph.add_node(LineageNode(node_id=child.branch_id.value, kind="worldline"))
        graph.add_node(LineageNode(node_id="wd_derived", kind="derived_world"))
        graph.add_edge(LineageEdge(root.value, child.branch_id.value, edge_kind="fork"))
        graph.add_edge(
            LineageEdge(
                child.branch_id.value, "wd_derived", edge_kind="promotion", origin_ref="cand_rc"
            )
        )

        # Parent history/state unchanged by the child + promotion derivation.
        assert runtime.current_state(instance_id, root).semantic_hash() == parent_hash
        assert runtime.events(instance_id, root) == parent_events
        assert set(graph.ancestors("wd_derived")) == {
            child.branch_id.value,
            root.value,
        }  # sorted order
    finally:
        cleanup_db_file(path)


@pytest.mark.integration
def test_multi_instance_replay_is_independent() -> None:
    path_a = fresh_db_path()
    path_b = fresh_db_path()
    try:
        runtime_a = make_world_runtime(path_a)
        runtime_b = make_world_runtime(path_b)
        a = runtime_a.create_world()
        b = runtime_b.create_world()
        runtime_a.submit_command(
            _cmd(
                a.instance_id,
                a.root_branch_id,
                "create_entity",
                {"entity_id": "x", "count": 1},
                0,
                "cmd_a1",
            )
        )
        runtime_b.submit_command(
            _cmd(
                b.instance_id,
                b.root_branch_id,
                "create_entity",
                {"entity_id": "x", "count": 9},
                0,
                "cmd_b1",
            )
        )
        hash_a = (
            ReplayEngine(RuntimeVersion(1), SchemaVersion(1))
            .replay(runtime_a.events(a.instance_id, a.root_branch_id))
            .semantic_hash()
        )
        hash_b = (
            ReplayEngine(RuntimeVersion(1), SchemaVersion(1))
            .replay(runtime_b.events(b.instance_id, b.root_branch_id))
            .semantic_hash()
        )
        # Same local entity id, different counts -> independent replay hashes.
        assert hash_a != hash_b
    finally:
        cleanup_db_file(path_a)
        cleanup_db_file(path_b)
