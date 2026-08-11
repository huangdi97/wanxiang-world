"""Versioned serialization for history/persistence contracts.

Event, snapshot, run and ancestry serialization live in this module; command and
delta serialization live in `serialization.py`. Both use the same schema-version
compatibility boundary.
"""

from __future__ import annotations

from typing import Any

from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchAncestry, BranchRevision, EventSeq
from wanxiang_domain.ids import (
    ActorId,
    BranchId,
    CommandId,
    CorrelationId,
    EventId,
    RunId,
    SnapshotId,
    TraceId,
    WorldInstanceId,
)
from wanxiang_domain.run import RunMetadata
from wanxiang_domain.serialization import (
    decode_id,
    delta_from_primitive,
    delta_to_primitive,
    encode_id,
    expect_version,
)
from wanxiang_domain.snapshot import SnapshotMetadata
from wanxiang_domain.time import CommitTimestamp, WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion

__all__ = [
    "ancestry_from_primitive",
    "ancestry_to_primitive",
    "event_from_primitive",
    "event_to_primitive",
    "run_from_primitive",
    "run_to_primitive",
    "snapshot_from_primitive",
    "snapshot_to_primitive",
]


def event_to_primitive(event: CommittedEvent) -> dict[str, Any]:
    return {
        "schema_version": event.schema_version.value,
        "event_id": encode_id(event.event_id),
        "instance_id": encode_id(event.instance_id),
        "branch_id": encode_id(event.branch_id),
        "event_seq": event.event_seq.value,
        "revision": event.revision.value,
        "command_id": encode_id(event.command_id),
        "delta": delta_to_primitive(event.delta),
        "world_time": event.world_time.ticks,
        "rule_version": event.rule_version.value,
        "actor_id": encode_id(event.actor_id) if event.actor_id else None,
        "causation_id": (encode_id(event.causation_id) if event.causation_id else None),
        "correlation_id": (encode_id(event.correlation_id) if event.correlation_id else None),
        "trace_id": encode_id(event.trace_id) if event.trace_id else None,
        "commit_timestamp": (
            event.commit_timestamp.utc.isoformat() if event.commit_timestamp else None
        ),
    }


def event_from_primitive(data: dict[str, Any]) -> CommittedEvent:
    expect_version(data)
    timestamp = None
    if data.get("commit_timestamp"):
        timestamp = CommitTimestamp.from_isoformat(data["commit_timestamp"])
    return CommittedEvent(
        event_id=decode_id(EventId, data["event_id"]),
        instance_id=decode_id(WorldInstanceId, data["instance_id"]),
        branch_id=decode_id(BranchId, data["branch_id"]),
        event_seq=EventSeq(data["event_seq"]),
        revision=BranchRevision(data["revision"]),
        schema_version=SchemaVersion(data["schema_version"]),
        command_id=decode_id(CommandId, data["command_id"]),
        delta=delta_from_primitive(data["delta"]),
        world_time=WorldTime(data["world_time"]),
        rule_version=RuntimeVersion(data["rule_version"]),
        actor_id=decode_id(ActorId, data["actor_id"]) if data.get("actor_id") else None,
        causation_id=decode_id(CommandId, data["causation_id"])
        if data.get("causation_id")
        else None,
        correlation_id=decode_id(CorrelationId, data["correlation_id"])
        if data.get("correlation_id")
        else None,
        trace_id=decode_id(TraceId, data["trace_id"]) if data.get("trace_id") else None,
        commit_timestamp=timestamp,
    )


def snapshot_to_primitive(snapshot: SnapshotMetadata) -> dict[str, Any]:
    return {
        "schema_version": snapshot.schema_version.value,
        "snapshot_id": encode_id(snapshot.snapshot_id),
        "instance_id": encode_id(snapshot.instance_id),
        "branch_id": encode_id(snapshot.branch_id),
        "revision": snapshot.revision.value,
        "event_seq": snapshot.event_seq.value,
        "rule_version": snapshot.rule_version.value,
        "created_world_time": snapshot.created_world_time.ticks,
        "content_ref": snapshot.content_ref,
    }


def snapshot_from_primitive(data: dict[str, Any]) -> SnapshotMetadata:
    expect_version(data)
    return SnapshotMetadata(
        snapshot_id=decode_id(SnapshotId, data["snapshot_id"]),
        instance_id=decode_id(WorldInstanceId, data["instance_id"]),
        branch_id=decode_id(BranchId, data["branch_id"]),
        revision=BranchRevision(data["revision"]),
        event_seq=EventSeq(data["event_seq"]),
        schema_version=SchemaVersion(data["schema_version"]),
        rule_version=RuntimeVersion(data["rule_version"]),
        created_world_time=WorldTime(data["created_world_time"]),
        content_ref=data["content_ref"],
    )


def run_to_primitive(run: RunMetadata) -> dict[str, Any]:
    return {
        "schema_version": run.schema_version.value,
        "run_id": encode_id(run.run_id),
        "instance_id": encode_id(run.instance_id),
        "seed": run.seed,
        "rule_version": run.rule_version.value,
        "started_world_time": run.started_world_time.ticks,
    }


def run_from_primitive(data: dict[str, Any]) -> RunMetadata:
    expect_version(data)
    return RunMetadata(
        run_id=decode_id(RunId, data["run_id"]),
        instance_id=decode_id(WorldInstanceId, data["instance_id"]),
        seed=data["seed"],
        rule_version=RuntimeVersion(data["rule_version"]),
        schema_version=SchemaVersion(data["schema_version"]),
        started_world_time=WorldTime(data["started_world_time"]),
    )


def ancestry_to_primitive(ancestry: BranchAncestry) -> dict[str, Any]:
    return {
        "parent_branch_id": encode_id(ancestry.parent_branch_id)
        if ancestry.parent_branch_id
        else None,
        "fork_revision": ancestry.fork_revision.value if ancestry.fork_revision else None,
        "fork_event_seq": (ancestry.fork_event_seq.value if ancestry.fork_event_seq else None),
        "fork_snapshot_ref": ancestry.fork_snapshot_ref,
    }


def ancestry_from_primitive(data: dict[str, Any]) -> BranchAncestry:
    parent = data.get("parent_branch_id")
    rev = data.get("fork_revision")
    seq = data.get("fork_event_seq")
    return BranchAncestry(
        parent_branch_id=decode_id(BranchId, parent) if parent else None,
        fork_revision=BranchRevision(rev) if rev is not None else None,
        fork_event_seq=EventSeq(seq) if seq is not None else None,
        fork_snapshot_ref=data.get("fork_snapshot_ref"),
    )
