"""Atomic long-run cursor checkpoints over the existing runtime history."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.long_horizon.scheduler import RecurringScheduler, SchedulerCursor


class CheckpointCrash(ContractError):
    """Deterministic test-only crash injection before checkpoint publication."""


@dataclass(frozen=True, slots=True)
class CrashPlan:
    """Checkpoint sequence numbers at which publication must fail."""

    fail_on_sequences: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if any(item < 1 for item in self.fail_on_sequences):
            raise ContractError("crash sequence numbers must be positive")
        if tuple(sorted(set(self.fail_on_sequences))) != self.fail_on_sequences:
            raise ContractError("crash sequence numbers must be unique and sorted")

    def should_fail(self, checkpoint_seq: int) -> bool:
        return checkpoint_seq in self.fail_on_sequences


@dataclass(frozen=True, slots=True)
class RunCheckpoint:
    """Cursor-only checkpoint; canonical events remain in the runtime ledger."""

    run_id: str
    world_ref: str
    branch_ref: str
    checkpoint_seq: int
    scheduler_cursor: SchedulerCursor
    state_hash: str
    event_head: int
    schema_version: int = 1

    def __post_init__(self) -> None:
        if not self.run_id or not self.world_ref or not self.branch_ref:
            raise ContractError("checkpoint refs must be non-empty")
        if self.checkpoint_seq < 1 or self.event_head < 0:
            raise ContractError("checkpoint sequence and event head are invalid")
        if not self.state_hash:
            raise ContractError("checkpoint state_hash must be non-empty")
        if self.schema_version != 1:
            raise ContractError("unsupported run checkpoint schema")

    @property
    def fingerprint(self) -> str:
        payload = {
            "run_id": self.run_id,
            "world_ref": self.world_ref,
            "branch_ref": self.branch_ref,
            "checkpoint_seq": self.checkpoint_seq,
            "scheduler": {
                "current_tick": self.scheduler_cursor.current_tick,
                "pending": self.scheduler_cursor.pending,
            },
            "state_hash": self.state_hash,
            "event_head": self.event_head,
            "schema_version": self.schema_version,
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "world_ref": self.world_ref,
            "branch_ref": self.branch_ref,
            "checkpoint_seq": self.checkpoint_seq,
            "scheduler_cursor": {
                "current_tick": self.scheduler_cursor.current_tick,
                "pending": [list(item) for item in self.scheduler_cursor.pending],
            },
            "state_hash": self.state_hash,
            "event_head": self.event_head,
            "schema_version": self.schema_version,
            "fingerprint": self.fingerprint,
        }


@dataclass(slots=True)
class RunCheckpointStore:
    """Atomic in-memory cursor store; canonical state stays in Runtime stores."""

    crash_plan: CrashPlan = field(default_factory=CrashPlan)
    _history: dict[str, tuple[RunCheckpoint, ...]] = field(
        init=False, default_factory=dict[str, tuple[RunCheckpoint, ...]]
    )

    def save(self, checkpoint: RunCheckpoint) -> RunCheckpoint:
        history = self._history.get(checkpoint.run_id, ())
        latest = history[-1] if history else None
        if latest is not None:
            if checkpoint.checkpoint_seq != latest.checkpoint_seq + 1:
                raise ContractError("checkpoint sequence must advance exactly once")
            if checkpoint.scheduler_cursor.current_tick < latest.scheduler_cursor.current_tick:
                raise ContractError("checkpoint world time cannot regress")
            if checkpoint.event_head < latest.event_head:
                raise ContractError("checkpoint event head cannot regress")
        if self.crash_plan.should_fail(checkpoint.checkpoint_seq):
            raise CheckpointCrash(
                f"injected crash before checkpoint {checkpoint.checkpoint_seq} publication"
            )
        self._history[checkpoint.run_id] = history + (checkpoint,)
        return checkpoint

    def latest(self, run_id: str) -> RunCheckpoint | None:
        history = self._history.get(run_id, ())
        return history[-1] if history else None

    def history(self, run_id: str) -> tuple[RunCheckpoint, ...]:
        return self._history.get(run_id, ())


class LongRunCheckpointService:
    """Build, atomically publish, and restore cursor checkpoints."""

    def __init__(self, store: RunCheckpointStore) -> None:
        self._store = store

    def checkpoint(
        self,
        run_id: str,
        world_ref: str,
        branch_ref: str,
        scheduler: RecurringScheduler,
        *,
        state_hash: str,
        event_head: int,
    ) -> RunCheckpoint:
        latest = self._store.latest(run_id)
        checkpoint = RunCheckpoint(
            run_id=run_id,
            world_ref=world_ref,
            branch_ref=branch_ref,
            checkpoint_seq=(latest.checkpoint_seq + 1 if latest is not None else 1),
            scheduler_cursor=scheduler.cursor(),
            state_hash=state_hash,
            event_head=event_head,
        )
        return self._store.save(checkpoint)

    def resume(self, run_id: str, scheduler: RecurringScheduler) -> RunCheckpoint:
        checkpoint = self._store.latest(run_id)
        if checkpoint is None:
            raise ContractError(f"no checkpoint for run {run_id!r}")
        scheduler.restore_cursor(checkpoint.scheduler_cursor)
        return checkpoint


__all__ = [
    "CheckpointCrash",
    "CrashPlan",
    "LongRunCheckpointService",
    "RunCheckpoint",
    "RunCheckpointStore",
]
