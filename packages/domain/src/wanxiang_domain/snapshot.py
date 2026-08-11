"""Snapshot metadata.

A snapshot is a checkpoint baseline for replay/performance, never a replacement
for event history.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, SnapshotId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion


@dataclass(frozen=True, slots=True)
class SnapshotMetadata:
    snapshot_id: SnapshotId
    instance_id: WorldInstanceId
    branch_id: BranchId
    revision: BranchRevision
    event_seq: EventSeq
    schema_version: SchemaVersion
    rule_version: RuntimeVersion
    created_world_time: WorldTime
    content_ref: str
