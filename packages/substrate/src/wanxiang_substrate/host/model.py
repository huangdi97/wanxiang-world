"""World host value objects (G05A)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.ids import BranchId, WorldInstanceId

LifecycleMode = Literal["running", "paused", "stopped"]

_VALID_TRANSITIONS: dict[LifecycleMode, tuple[LifecycleMode, ...]] = {
    "running": ("paused", "stopped"),
    "paused": ("running", "stopped"),
    "stopped": (),
}


@dataclass(frozen=True, slots=True)
class HostStatus:
    """Observable host lifecycle (persisted independently of sessions)."""

    instance_id: WorldInstanceId
    root_branch_id: BranchId
    mode: LifecycleMode = "running"
    revision: int = 0
    scheduler_enabled: bool = False

    def can_transition_to(self, next_mode: LifecycleMode) -> bool:
        return next_mode in _VALID_TRANSITIONS[self.mode]
