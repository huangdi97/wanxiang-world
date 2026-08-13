"""Session, embodiment lease and control handoff value objects (G05B, G05C)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.ids import WorldInstanceId

LeaseState = Literal["acquired", "renewed", "released", "expired"]
ControlState = Literal[
    "autonomous",
    "human_control",
    "handing_back",
    "resuming_autonomous",
]


@dataclass(frozen=True, slots=True)
class Session:
    """A client session bound to a world instance with a mode."""

    session_id: str
    controller: str
    instance_id: WorldInstanceId
    mode: Literal["observe", "embody", "admin"]
    created_seq: int

    def may_embody(self) -> bool:
        return self.mode in ("embody", "admin")

    def may_admin(self) -> bool:
        return self.mode == "admin"


@dataclass(frozen=True, slots=True)
class EmbodimentLease:
    """One primary embodiment controller per actor."""

    lease_id: str
    session_id: str
    actor_id: str
    state: LeaseState
    acquired_seq: int
    expires_seq: int
    released_seq: int | None = None

    @property
    def active(self) -> bool:
        return self.state in ("acquired", "renewed")


@dataclass(frozen=True, slots=True)
class HandoffState:
    """Authoritative control state per actor (shadow is advice-only)."""

    actor_id: str
    state: ControlState
    controller_session: str | None = None
    last_commit_seq: int = 0
    resume_ref: str = ""

    def can_transition_to(self, next_state: ControlState) -> bool:
        table: dict[ControlState, tuple[ControlState, ...]] = {
            "autonomous": ("human_control",),
            "human_control": ("handing_back",),
            "handing_back": ("resuming_autonomous",),
            "resuming_autonomous": ("autonomous",),
        }
        return next_state in table[self.state]
