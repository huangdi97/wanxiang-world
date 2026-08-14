"""Checkpoint save/restore with rotation and validation (G06C).

Checkpointing reuses the single runtime SnapshotStore port (production owner):
snapshot state lives only in wanxiang_runtime.snapshot. `CheckpointStore` is a
thin adapter that keeps the recovery-specific latest-per-instance and
snapshot-id indexes on top of that one store, so there is no second snapshot
state implementation.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, SnapshotId, WorldInstanceId
from wanxiang_runtime.snapshot import SnapshotStore as RuntimeSnapshotStore
from wanxiang_runtime.snapshot import create_snapshot_metadata
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.recovery.errors import CorruptSnapshot, NoSnapshot


@dataclass(frozen=True, slots=True)
class CheckpointMeta:
    instance_id: str
    branch_id: str
    revision: int
    snapshot_id: str


class CheckpointStore:
    """Checkpoint store backed by the single runtime SnapshotStore port.

    The canonical snapshot state is stored exactly once (runtime store); this
    adapter only keeps the recovery-specific indexes (latest per instance,
    snapshot-id -> location). API-compatible with the pre-v5.2 recovery store.
    """

    def __init__(self, store: RuntimeSnapshotStore | None = None) -> None:
        from wanxiang_runtime.snapshot import InMemorySnapshotStore

        self._store = store or InMemorySnapshotStore()
        self._latest: dict[str, tuple[int, str]] = {}
        self._by_snapshot: dict[str, tuple[str, str, int]] = {}

    def save(self, metadata: CheckpointMeta, state: InMemoryCanonicalState) -> CheckpointMeta:
        snapshot_meta = create_snapshot_metadata(
            state,
            EventSeq(state.revision.value),
            snapshot_id=SnapshotId(metadata.snapshot_id),
            content_ref=f"checkpoint://{metadata.snapshot_id}",
        )
        self._store.save(snapshot_meta, state)
        self._by_snapshot[metadata.snapshot_id] = (
            state.instance_id.value,
            state.branch_id.value,
            state.revision.value,
        )
        current = self._latest.get(metadata.instance_id)
        if current is None or metadata.revision > current[0]:
            self._latest[metadata.instance_id] = (metadata.revision, metadata.snapshot_id)
        return metadata

    def latest(self, instance_id: str) -> tuple[int, str] | None:
        return self._latest.get(instance_id)

    def load(self, snapshot_id: str) -> InMemoryCanonicalState:
        location = self._by_snapshot.get(snapshot_id)
        if location is None:
            raise NoSnapshot(f"snapshot {snapshot_id!r} not found")
        stored = self._store.load(
            WorldInstanceId(location[0]),
            BranchId(location[1]),
            BranchRevision(location[2]),
        )
        if stored is None:
            raise NoSnapshot(f"snapshot {snapshot_id!r} not found in store")
        return stored.state


# Deprecated aliases kept for API compatibility (pre-v5.2 names).
InMemorySnapshotStore = CheckpointStore
SnapshotStore = CheckpointStore


class CheckpointService:
    """Validated checkpoint save/restore (corrupt snapshots fail explicitly)."""

    def __init__(self, store: CheckpointStore) -> None:
        self._store = store

    def save(
        self,
        instance_id: str,
        branch_id: str,
        revision: int,
        state: InMemoryCanonicalState,
        snapshot_id: str,
    ) -> CheckpointMeta:
        expected = state.semantic_hash()
        if state.revision.value != revision:
            raise CorruptSnapshot(
                f"checkpoint revision mismatch: state {state.revision.value} != {revision}"
            )
        meta = CheckpointMeta(instance_id, branch_id, revision, snapshot_id)
        self._store.save(meta, state)
        stored = self._store.load(snapshot_id)
        if stored.semantic_hash() != expected:
            raise CorruptSnapshot("checkpoint did not round-trip")
        return meta

    def restore(self, instance_id: str) -> InMemoryCanonicalState:
        latest = self._store.latest(instance_id)
        if latest is None:
            raise NoSnapshot(f"no checkpoint for {instance_id!r}")
        state = self._store.load(latest[1])
        if state.instance_id.value != instance_id:
            raise CorruptSnapshot("snapshot instance id mismatch")
        return state
