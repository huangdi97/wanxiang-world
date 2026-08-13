"""Persistent world lifecycle modes and transitions (G06A)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.ids import BranchId, WorldInstanceId

LifecycleMode = Literal[
    "PAUSED",
    "REALTIME",
    "ACCELERATED",
    "EVENT_DRIVEN",
    "BACKGROUND_SIMULATION",
    "FULL_AUTONOMY",
    "BATCH_SIMULATION",
]

LIFECYCLE_MODES: tuple[LifecycleMode, ...] = (
    "PAUSED",
    "REALTIME",
    "ACCELERATED",
    "EVENT_DRIVEN",
    "BACKGROUND_SIMULATION",
    "FULL_AUTONOMY",
    "BATCH_SIMULATION",
)

_TRANSITIONS: dict[LifecycleMode, tuple[LifecycleMode, ...]] = {
    "PAUSED": (
        "REALTIME",
        "ACCELERATED",
        "EVENT_DRIVEN",
        "BACKGROUND_SIMULATION",
        "BATCH_SIMULATION",
    ),
    "REALTIME": (
        "PAUSED",
        "ACCELERATED",
        "EVENT_DRIVEN",
        "BACKGROUND_SIMULATION",
        "FULL_AUTONOMY",
        "BATCH_SIMULATION",
    ),
    "ACCELERATED": (
        "PAUSED",
        "REALTIME",
        "EVENT_DRIVEN",
        "BACKGROUND_SIMULATION",
        "BATCH_SIMULATION",
    ),
    "EVENT_DRIVEN": (
        "PAUSED",
        "REALTIME",
        "BACKGROUND_SIMULATION",
        "BATCH_SIMULATION",
    ),
    "BACKGROUND_SIMULATION": (
        "PAUSED",
        "REALTIME",
        "ACCELERATED",
        "EVENT_DRIVEN",
        "FULL_AUTONOMY",
        "BATCH_SIMULATION",
    ),
    "FULL_AUTONOMY": (
        "PAUSED",
        "REALTIME",
        "BACKGROUND_SIMULATION",
        "BATCH_SIMULATION",
    ),
    "BATCH_SIMULATION": ("PAUSED", "REALTIME"),
}


def can_transition(current: LifecycleMode, next_mode: LifecycleMode) -> bool:
    return next_mode in _TRANSITIONS[current]


def advances_time(mode: LifecycleMode) -> bool:
    """Modes that advance world time (PAUSED never advances)."""
    return mode != "PAUSED"


@dataclass(frozen=True, slots=True)
class LifecycleState:
    """Persisted lifecycle mode with tick and audit revision."""

    instance_id: WorldInstanceId
    branch_id: BranchId
    mode: LifecycleMode
    tick: int
    updated_revision: int

    def can_transition_to(self, next_mode: LifecycleMode) -> bool:
        return can_transition(self.mode, next_mode)
