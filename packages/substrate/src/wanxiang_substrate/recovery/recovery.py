"""Crash recovery: startup from snapshot/events, in-flight policy, leases (G06C).

The crash-consistency boundary is committed events: in-flight uncommitted
commands are never partially applied. Startup restores the latest valid
snapshot or replays the event log; stale embodiment leases and scheduler queues
are recovered/expired safely.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.recovery.budget import BudgetTracker, ResourceBudget
from wanxiang_substrate.recovery.checkpoint import CheckpointService
from wanxiang_substrate.recovery.errors import CorruptSnapshot, NoSnapshot


@dataclass(frozen=True, slots=True)
class RecoveryReport:
    instance_id: str
    restored_from: str
    revision: int
    semantic_hash: str
    expired_leases: tuple[str, ...]
    in_flight_policy: str = "discard_uncommitted"


class RecoveryService:
    """Startup recovery from the latest valid snapshot or event log."""

    def __init__(
        self,
        checkpoint: CheckpointService,
        *,
        budget: ResourceBudget | None = None,
        allow_snapshot_fallback: bool = True,
    ) -> None:
        self._checkpoint = checkpoint
        self._budget_tracker = BudgetTracker(budget)
        self._allow_snapshot_fallback = allow_snapshot_fallback

    def recover(
        self,
        instance_id: str,
        replay_state: InMemoryCanonicalState,
        lease_service: object | None = None,
    ) -> RecoveryReport:
        """Restore from snapshot when valid, else replay; never half-commit."""
        restored_from = "event_replay"
        state: InMemoryCanonicalState | None = None
        try:
            state = self._checkpoint.restore(instance_id)
            if state.semantic_hash() == replay_state.semantic_hash():
                restored_from = "snapshot"
        except (NoSnapshot, CorruptSnapshot):
            if not self._allow_snapshot_fallback:
                raise
            state = replay_state
            restored_from = "event_replay"
        expired = self._expire_stale_leases(lease_service)
        return RecoveryReport(
            instance_id=instance_id,
            restored_from=restored_from,
            revision=state.revision.value,
            semantic_hash=state.semantic_hash(),
            expired_leases=expired,
        )

    @staticmethod
    def _expire_stale_leases(lease_service: object | None) -> tuple[str, ...]:
        if lease_service is None:
            return ()
        expire = getattr(lease_service, "expire_all_stale", None)
        if callable(expire):
            result = expire()
            if isinstance(result, tuple):
                items = cast(tuple[object, ...], result)
                return tuple(str(item) for item in items)
        return ()
