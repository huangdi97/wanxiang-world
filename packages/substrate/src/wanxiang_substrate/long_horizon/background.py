"""Offline/background simulation policy over the recurring scheduler."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.long_horizon.scheduler import (
    RecurringScheduler,
    ScheduledOccurrence,
    SchedulerCursor,
)
from wanxiang_substrate.playable.models import RuntimeProfile

BackgroundMode = Literal["paused", "realtime", "accelerated", "background", "full_autonomy"]
BACKGROUND_MODES: tuple[BackgroundMode, ...] = (
    "paused",
    "realtime",
    "accelerated",
    "background",
    "full_autonomy",
)


@dataclass(frozen=True, slots=True)
class BackgroundPolicy:
    """RuntimeProfile-bound policy for offline world-time progression."""

    runtime_profile: RuntimeProfile
    mode: BackgroundMode = "background"
    offline_enabled: bool = True

    def __post_init__(self) -> None:
        if self.mode not in BACKGROUND_MODES:
            raise ContractError(f"unsupported background mode {self.mode!r}")
        if not self.offline_enabled and self.mode != "paused":
            raise ContractError("offline-disabled policy must be paused")

    def world_ticks(self, elapsed_ticks: int) -> int:
        """Convert detached wall-time ticks into monotonic world ticks."""
        if elapsed_ticks < 0:
            raise ContractError("elapsed_ticks must be non-negative")
        if self.mode == "paused":
            return 0
        if self.mode == "realtime":
            return elapsed_ticks
        return elapsed_ticks * self.runtime_profile.time_scale


@dataclass(frozen=True, slots=True)
class SessionCursor:
    """Persistable leave-world boundary; no live user session is required."""

    world_ref: str
    branch_ref: str
    session_id: str
    world_tick: int
    scheduler_cursor: SchedulerCursor

    def __post_init__(self) -> None:
        if not self.world_ref or not self.branch_ref or not self.session_id:
            raise ContractError("session cursor refs must be non-empty")
        if self.world_tick < 0:
            raise ContractError("session cursor world_tick must be non-negative")
        if self.scheduler_cursor.current_tick != self.world_tick:
            raise ContractError("scheduler cursor must match session world_tick")

    def to_dict(self) -> dict[str, object]:
        return {
            "world_ref": self.world_ref,
            "branch_ref": self.branch_ref,
            "session_id": self.session_id,
            "world_tick": self.world_tick,
            "scheduler_cursor": {
                "current_tick": self.scheduler_cursor.current_tick,
                "pending": [list(item) for item in self.scheduler_cursor.pending],
            },
        }


@dataclass(frozen=True, slots=True)
class BackgroundRun:
    """Observable offline run result and its next re-entry cursor."""

    cursor_before: SessionCursor
    cursor_after: SessionCursor
    mode: BackgroundMode
    elapsed_ticks: int
    world_ticks_advanced: int
    occurrences: tuple[ScheduledOccurrence, ...]

    @property
    def session_independent(self) -> bool:
        return True


class BackgroundSimulation:
    """Run scheduler proposals while the interactive session is detached."""

    def __init__(
        self,
        scheduler: RecurringScheduler,
        policy: BackgroundPolicy,
        *,
        world_ref: str,
        branch_ref: str,
    ) -> None:
        if not world_ref or not branch_ref:
            raise ContractError("background world and branch refs must be non-empty")
        self._scheduler = scheduler
        self._policy = policy
        self._world_ref = world_ref
        self._branch_ref = branch_ref

    @property
    def policy(self) -> BackgroundPolicy:
        return self._policy

    def leave(self, session_id: str) -> SessionCursor:
        """Create a durable leave cursor without storing a user session."""
        if not session_id:
            raise ContractError("session_id must be non-empty")
        tick = self._scheduler.current_tick
        return SessionCursor(
            world_ref=self._world_ref,
            branch_ref=self._branch_ref,
            session_id=session_id,
            world_tick=tick,
            scheduler_cursor=self._scheduler.cursor(),
        )

    def run_offline(self, cursor: SessionCursor, *, elapsed_ticks: int) -> BackgroundRun:
        """Advance from a leave cursor and return proposal occurrences."""
        self._assert_cursor(cursor)
        if cursor.world_tick != self._scheduler.current_tick:
            raise ContractError("session cursor is stale for this scheduler")
        world_ticks = self._policy.world_ticks(elapsed_ticks)
        target = cursor.world_tick + world_ticks
        occurrences = self._scheduler.advance_to(target)
        after = SessionCursor(
            world_ref=cursor.world_ref,
            branch_ref=cursor.branch_ref,
            session_id=cursor.session_id,
            world_tick=target,
            scheduler_cursor=self._scheduler.cursor(),
        )
        return BackgroundRun(
            cursor_before=cursor,
            cursor_after=after,
            mode=self._policy.mode,
            elapsed_ticks=elapsed_ticks,
            world_ticks_advanced=world_ticks,
            occurrences=occurrences,
        )

    def reenter(self, run: BackgroundRun) -> SessionCursor:
        """Return the cursor a new interactive session may consume."""
        self._assert_cursor(run.cursor_after)
        return run.cursor_after

    def _assert_cursor(self, cursor: SessionCursor) -> None:
        if cursor.world_ref != self._world_ref or cursor.branch_ref != self._branch_ref:
            raise ContractError("session cursor worldline does not match background runtime")


__all__ = [
    "BACKGROUND_MODES",
    "BackgroundMode",
    "BackgroundPolicy",
    "BackgroundRun",
    "BackgroundSimulation",
    "SessionCursor",
]
