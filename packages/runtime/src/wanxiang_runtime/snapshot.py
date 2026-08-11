"""Snapshot store: checkpoint baseline, never a replacement for history."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, SnapshotId, WorldInstanceId
from wanxiang_domain.snapshot import SnapshotMetadata
from wanxiang_domain.time import WorldTime

from wanxiang_runtime.state import InMemoryCanonicalState


@dataclass(frozen=True, slots=True)
class StoredSnapshot:
    metadata: SnapshotMetadata
    state: InMemoryCanonicalState


class SnapshotStore(Protocol):
    def save(
        self, metadata: SnapshotMetadata, state: InMemoryCanonicalState
    ) -> SnapshotMetadata: ...

    def load(
        self, instance_id: WorldInstanceId, branch_id: BranchId, revision: BranchRevision
    ) -> StoredSnapshot | None: ...

    def latest(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        *,
        at_or_before_revision: BranchRevision | None = None,
    ) -> StoredSnapshot | None: ...


def create_snapshot_metadata(
    state: InMemoryCanonicalState,
    event_seq: EventSeq,
    *,
    snapshot_id: SnapshotId | None = None,
    content_ref: str | None = None,
    created_world_time: WorldTime | None = None,
) -> SnapshotMetadata:
    """Build snapshot metadata for the current state at the given event seq."""
    world_time = (
        created_world_time if created_world_time is not None else WorldTime(state.revision.value)
    )
    return SnapshotMetadata(
        snapshot_id=snapshot_id or SnapshotId.generate(),
        instance_id=state.instance_id,
        branch_id=state.branch_id,
        revision=state.revision,
        event_seq=event_seq,
        schema_version=state.schema_version,
        rule_version=state.rule_version,
        created_world_time=world_time,
        content_ref=content_ref or f"mem://{state.branch_id.value}/{state.revision.value}",
    )


@dataclass(slots=True)
class InMemorySnapshotStore:
    """Deterministic in-memory snapshot store."""

    _snapshots: dict[tuple[str, str], list[StoredSnapshot]] = field(
        default_factory=dict[tuple[str, str], list[StoredSnapshot]]
    )

    def save(self, metadata: SnapshotMetadata, state: InMemoryCanonicalState) -> SnapshotMetadata:
        key = (metadata.instance_id.value, metadata.branch_id.value)
        self._snapshots.setdefault(key, []).append(StoredSnapshot(metadata=metadata, state=state))
        return metadata

    def load(
        self, instance_id: WorldInstanceId, branch_id: BranchId, revision: BranchRevision
    ) -> StoredSnapshot | None:
        for stored in self._snapshots.get((instance_id.value, branch_id.value), []):
            if stored.metadata.revision == revision:
                return stored
        return None

    def latest(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        *,
        at_or_before_revision: BranchRevision | None = None,
    ) -> StoredSnapshot | None:
        candidates = self._snapshots.get((instance_id.value, branch_id.value), [])
        if at_or_before_revision is not None:
            candidates = [
                s for s in candidates if s.metadata.revision.value <= at_or_before_revision.value
            ]
        if not candidates:
            return None
        return max(candidates, key=lambda s: s.metadata.revision.value)
