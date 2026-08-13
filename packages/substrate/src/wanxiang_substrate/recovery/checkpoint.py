"""Checkpoint save/restore with rotation and validation (G06C)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.recovery.errors import CorruptSnapshot, NoSnapshot


class SnapshotStore(Protocol):
    """Port for snapshot persistence."""

    def save(self, metadata: CheckpointMeta, state: InMemoryCanonicalState) -> CheckpointMeta: ...
    def latest(self, instance_id: str) -> tuple[int, str] | None: ...
    def load(self, snapshot_id: str) -> InMemoryCanonicalState: ...


@dataclass(frozen=True, slots=True)
class CheckpointMeta:
    instance_id: str
    branch_id: str
    revision: int
    snapshot_id: str


class InMemorySnapshotStore:
    """Deterministic in-memory snapshot store for tests."""

    def __init__(self) -> None:
        self._snapshots: dict[str, InMemoryCanonicalState] = {}
        self._latest: dict[str, tuple[int, str]] = {}

    def save(self, metadata: CheckpointMeta, state: InMemoryCanonicalState) -> CheckpointMeta:
        self._snapshots[metadata.snapshot_id] = state
        current = self._latest.get(metadata.instance_id)
        if current is None or metadata.revision > current[0]:
            self._latest[metadata.instance_id] = (metadata.revision, metadata.snapshot_id)
        return metadata

    def latest(self, instance_id: str) -> tuple[int, str] | None:
        return self._latest.get(instance_id)

    def load(self, snapshot_id: str) -> InMemoryCanonicalState:
        state = self._snapshots.get(snapshot_id)
        if state is None:
            raise NoSnapshot(f"snapshot {snapshot_id!r} not found")
        return state


class CheckpointService:
    """Validated checkpoint save/restore (corrupt snapshots fail explicitly)."""

    def __init__(self, store: SnapshotStore) -> None:
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
