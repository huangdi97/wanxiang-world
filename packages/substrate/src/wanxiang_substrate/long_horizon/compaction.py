"""Replay-safe snapshot cadence and logical event compaction references."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from wanxiang_domain.errors import ContractError
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.snapshot import SnapshotMetadata


@dataclass(frozen=True, slots=True)
class CompactionPolicy:
    """Bounded policy; compaction never deletes the authoritative event stream."""

    snapshot_every_events: int = 10
    retain_recent_events: int = 10
    memory_summary_every_events: int = 10
    archive_after_events: int = 50

    def __post_init__(self) -> None:
        for name in (
            "snapshot_every_events",
            "retain_recent_events",
            "memory_summary_every_events",
            "archive_after_events",
        ):
            if getattr(self, name) < 1:
                raise ContractError(f"{name} must be positive")

    def checkpoint_due(self, event_head: int) -> bool:
        if event_head < 0:
            raise ContractError("event_head must be non-negative")
        return event_head > 0 and event_head % self.snapshot_every_events == 0


@dataclass(frozen=True, slots=True)
class EventArchiveRef:
    event_seq: int
    event_id: str
    digest: str


@dataclass(frozen=True, slots=True)
class MemorySummaryRef:
    summary_id: str
    start_event_seq: int
    end_event_seq: int
    source_event_refs: tuple[str, ...]
    digest: str


@dataclass(frozen=True, slots=True)
class CompactionManifest:
    """Reference-only manifest; source events remain replayable and append-only."""

    instance_id: str
    branch_id: str
    snapshot_id: str
    snapshot_revision: int
    source_event_count: int
    archived_event_refs: tuple[EventArchiveRef, ...]
    retained_event_seqs: tuple[int, ...]
    memory_summary_refs: tuple[MemorySummaryRef, ...]
    replay_hash: str
    archive_ref: str
    schema_version: int = 1

    @property
    def compacted(self) -> bool:
        return bool(self.archived_event_refs)

    @property
    def retained_event_count(self) -> int:
        return len(self.retained_event_seqs)

    def to_dict(self) -> dict[str, object]:
        return {
            "instance_id": self.instance_id,
            "branch_id": self.branch_id,
            "snapshot_id": self.snapshot_id,
            "snapshot_revision": self.snapshot_revision,
            "source_event_count": self.source_event_count,
            "archived_event_refs": [
                {"event_seq": item.event_seq, "event_id": item.event_id, "digest": item.digest}
                for item in self.archived_event_refs
            ],
            "retained_event_seqs": list(self.retained_event_seqs),
            "memory_summary_refs": [
                {
                    "summary_id": item.summary_id,
                    "start_event_seq": item.start_event_seq,
                    "end_event_seq": item.end_event_seq,
                    "source_event_refs": list(item.source_event_refs),
                    "digest": item.digest,
                }
                for item in self.memory_summary_refs
            ],
            "replay_hash": self.replay_hash,
            "archive_ref": self.archive_ref,
            "schema_version": self.schema_version,
        }


@dataclass(slots=True)
class CompactionService:
    """Builds deterministic references without owning event or snapshot state."""

    policy: CompactionPolicy = field(default_factory=CompactionPolicy)

    def compact(
        self,
        events: tuple[CommittedEvent, ...],
        snapshot: SnapshotMetadata,
        *,
        replay_hash_before: str,
        replay_hash_after: str,
    ) -> CompactionManifest:
        if not replay_hash_before or replay_hash_before != replay_hash_after:
            raise ContractError("golden replay must match before and after compaction")
        if snapshot.instance_id.value != (
            events[0].instance_id.value if events else snapshot.instance_id.value
        ):
            raise ContractError("snapshot instance does not match event stream")
        if snapshot.branch_id.value != (
            events[0].branch_id.value if events else snapshot.branch_id.value
        ):
            raise ContractError("snapshot branch does not match event stream")
        self._validate_events(events)
        cutoff = max(0, len(events) - self.policy.retain_recent_events)
        archived = tuple(self._event_ref(event) for event in events[:cutoff])
        retained = tuple(event.event_seq.value for event in events[cutoff:])
        summaries = self._summaries(archived)
        archive_ref = (
            f"archive://{snapshot.instance_id.value}/{snapshot.branch_id.value}/"
            f"through-{archived[-1].event_seq if archived else 0}"
        )
        return CompactionManifest(
            instance_id=snapshot.instance_id.value,
            branch_id=snapshot.branch_id.value,
            snapshot_id=snapshot.snapshot_id.value,
            snapshot_revision=snapshot.revision.value,
            source_event_count=len(events),
            archived_event_refs=archived,
            retained_event_seqs=retained,
            memory_summary_refs=summaries,
            replay_hash=replay_hash_after,
            archive_ref=archive_ref,
        )

    def _summaries(self, refs: tuple[EventArchiveRef, ...]) -> tuple[MemorySummaryRef, ...]:
        size = self.policy.memory_summary_every_events
        summaries: list[MemorySummaryRef] = []
        for offset in range(0, len(refs), size):
            batch = refs[offset : offset + size]
            ids = tuple(item.event_id for item in batch)
            digest = hashlib.sha256("|".join(item.digest for item in batch).encode()).hexdigest()
            summaries.append(
                MemorySummaryRef(
                    summary_id=f"memory-summary-{batch[0].event_seq}-{batch[-1].event_seq}",
                    start_event_seq=batch[0].event_seq,
                    end_event_seq=batch[-1].event_seq,
                    source_event_refs=ids,
                    digest=digest,
                )
            )
        return tuple(summaries)

    @staticmethod
    def _event_ref(event: CommittedEvent) -> EventArchiveRef:
        material = "|".join(
            (
                event.event_id.value,
                event.command_id.value,
                str(event.event_seq.value),
                str(event.revision.value),
                str(event.world_time.ticks),
                repr(event.delta),
            )
        )
        return EventArchiveRef(
            event_seq=event.event_seq.value,
            event_id=event.event_id.value,
            digest=hashlib.sha256(material.encode()).hexdigest(),
        )

    @staticmethod
    def _validate_events(events: tuple[CommittedEvent, ...]) -> None:
        expected = 1
        for event in events:
            if event.event_seq.value != expected:
                raise ContractError("event stream is not contiguous")
            expected += 1


__all__ = [
    "CompactionManifest",
    "CompactionPolicy",
    "CompactionService",
    "EventArchiveRef",
    "MemorySummaryRef",
]
