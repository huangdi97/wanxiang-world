"""GOAL_01A: versioned serialization round trips and version rejection."""

from __future__ import annotations

import pytest
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import (
    EntityCreate,
    EntityUpdate,
    ProposedWorldDelta,
    RelationCreate,
)
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import IncompatibleVersion
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchAncestry, BranchRevision, EventSeq
from wanxiang_domain.ids import (
    BranchId,
    CommandId,
    ComponentId,
    EntityId,
    EventId,
    RelationId,
    RunId,
    SnapshotId,
    WorldInstanceId,
)
from wanxiang_domain.run import RunMetadata
from wanxiang_domain.serialization import (
    command_from_primitive,
    command_to_primitive,
    delta_from_primitive,
    delta_to_primitive,
)
from wanxiang_domain.serialization_history import (
    ancestry_from_primitive,
    ancestry_to_primitive,
    event_from_primitive,
    event_to_primitive,
    run_from_primitive,
    run_to_primitive,
    snapshot_from_primitive,
    snapshot_to_primitive,
)
from wanxiang_domain.snapshot import SnapshotMetadata
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion


@pytest.mark.unit
def test_command_round_trip() -> None:
    command = CommandEnvelope(
        command_id=CommandId("cmd_1"),
        instance_id=WorldInstanceId("wld_1"),
        branch_id=BranchId("br_1"),
        expected_revision=BranchRevision(3),
        action_type="transfer_resource",
        payload={"amount": 2},
        world_time=WorldTime(7),
    )
    assert command_from_primitive(command_to_primitive(command)) == command


@pytest.mark.unit
def test_delta_round_trip_with_operations() -> None:
    delta = ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=EntityId("ent_a"),
                entity_type="token_holder",
                components=(
                    ComponentData(
                        component_id=ComponentId("cmp_res"),
                        component_type="resource",
                        schema_version=SchemaVersion(1),
                        fields={"count": 5},
                    ),
                ),
            ),
            EntityUpdate(
                entity_id=EntityId("ent_b"),
                components=(
                    ComponentData(
                        component_id=ComponentId("cmp_res2"),
                        component_type="resource",
                        schema_version=SchemaVersion(1),
                        fields={"count": 2},
                    ),
                ),
            ),
            RelationCreate(
                relation_id=RelationId("rel_1"),
                relation_type="owns",
                source_id=EntityId("ent_a"),
                target_id=EntityId("ent_b"),
                attributes={"since": 1},
            ),
        )
    )
    assert delta_from_primitive(delta_to_primitive(delta)) == delta


@pytest.mark.unit
def test_event_round_trip() -> None:
    delta = ProposedWorldDelta(
        operations=(EntityCreate(entity_id=EntityId("ent_a"), entity_type="token_holder"),)
    )
    event = CommittedEvent(
        event_id=EventId("evt_1"),
        instance_id=WorldInstanceId("wld_1"),
        branch_id=BranchId("br_1"),
        event_seq=EventSeq(2),
        revision=BranchRevision(2),
        schema_version=SchemaVersion(1),
        command_id=CommandId("cmd_1"),
        delta=delta,
        world_time=WorldTime(3),
        rule_version=RuntimeVersion(1),
    )
    assert event_from_primitive(event_to_primitive(event)) == event


@pytest.mark.unit
def test_snapshot_and_run_round_trip() -> None:
    snapshot = SnapshotMetadata(
        snapshot_id=SnapshotId("snap_1"),
        instance_id=WorldInstanceId("wld_1"),
        branch_id=BranchId("br_1"),
        revision=BranchRevision(5),
        event_seq=EventSeq(5),
        schema_version=SchemaVersion(1),
        rule_version=RuntimeVersion(1),
        created_world_time=WorldTime(9),
        content_ref="snapshots/snap_1.json",
    )
    run = RunMetadata(
        run_id=RunId("run_1"),
        instance_id=WorldInstanceId("wld_1"),
        seed=42,
        rule_version=RuntimeVersion(1),
        schema_version=SchemaVersion(1),
        started_world_time=WorldTime(0),
    )
    assert snapshot_from_primitive(snapshot_to_primitive(snapshot)) == snapshot
    assert run_from_primitive(run_to_primitive(run)) == run


@pytest.mark.unit
def test_ancestry_round_trip_and_validation() -> None:
    ancestry = BranchAncestry(
        parent_branch_id=BranchId("br_0"),
        fork_revision=BranchRevision(4),
        fork_event_seq=EventSeq(4),
        fork_snapshot_ref="snapshots/snap_4.json",
    )
    assert ancestry_from_primitive(ancestry_to_primitive(ancestry)) == ancestry
    assert BranchAncestry() == BranchAncestry()


@pytest.mark.unit
def test_unknown_schema_version_is_rejected() -> None:
    delta = ProposedWorldDelta()
    data = delta_to_primitive(delta)
    data["schema_version"] = 999
    with pytest.raises(IncompatibleVersion):
        delta_from_primitive(data)
