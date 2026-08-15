"""Embodiment + ShadowPolicy handoff with control modes (G36F).

Extends the G05C handoff with intent/co-drive/full-control modes and an
append-only ControlHandoffEvent audit. ShadowPolicy is strictly advice-only:
it can never make major decisions or commit canonical actions. Reuses
LeaseService (one primary embodiment controller per actor).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.session.control import ShadowPolicy
from wanxiang_substrate.session.errors import InvalidHandoff, ShadowCannotCommit
from wanxiang_substrate.session.model import Session
from wanxiang_substrate.session.service import LeaseService

ControlMode = Literal["intent", "co_drive", "full_control"]
VALID_CONTROL_MODES = ("intent", "co_drive", "full_control")


@dataclass(frozen=True, slots=True)
class EmbodimentState:
    """Control state of an embodied actor under a specific mode."""

    actor_key: str
    controller_session: str | None
    control_mode: ControlMode
    lease_active: bool
    last_commit_seq: int

    def __post_init__(self) -> None:
        if not self.actor_key:
            raise ContractError("embodiment state requires an actor key")
        if self.control_mode not in VALID_CONTROL_MODES:
            raise ContractError(f"invalid control mode {self.control_mode!r}")


@dataclass(frozen=True, slots=True)
class ControlHandoffEvent:
    """Append-only audit event for embodiment handoff transitions."""

    event_id: str
    actor_key: str
    event_type: Literal["acquire", "mode_change", "release"]
    control_mode: ControlMode
    controller_session: str | None
    at_seq: int

    def __post_init__(self) -> None:
        if not self.event_id or not self.actor_key:
            raise ContractError("handoff event requires id and actor key")
        if self.event_type not in ("acquire", "mode_change", "release"):
            raise ContractError(f"invalid handoff event type {self.event_type!r}")


class EmbodimentController:
    """Thin controller composing LeaseService + ShadowPolicy + handoff events."""

    def __init__(
        self,
        leases: LeaseService | None = None,
        shadow: ShadowPolicy | None = None,
    ) -> None:
        self._leases = leases or LeaseService()
        self._shadow = shadow or ShadowPolicy()
        self._states: dict[str, EmbodimentState] = {}
        self._events: dict[str, tuple[ControlHandoffEvent, ...]] = {}
        self._seq = 0

    def acquire(
        self,
        session: Session,
        actor_key: str,
        *,
        lease_id: str,
        mode: ControlMode,
        acquired_seq: int,
        expires_seq: int,
    ) -> EmbodimentState:
        """Acquire the primary embodiment lease under a control mode."""
        if mode not in VALID_CONTROL_MODES:
            raise InvalidHandoff(f"invalid control mode {mode!r}")
        self._leases.acquire(session, actor_key, lease_id, acquired_seq, expires_seq)
        state = EmbodimentState(
            actor_key=actor_key,
            controller_session=session.session_id,
            control_mode=mode,
            lease_active=True,
            last_commit_seq=acquired_seq,
        )
        self._states[actor_key] = state
        self._emit(actor_key, "acquire", mode, session.session_id, acquired_seq)
        return state

    def set_mode(self, actor_key: str, mode: ControlMode, *, at_seq: int) -> EmbodimentState:
        """Change the control mode of an active embodiment (co-drive etc.)."""
        current = self._require(actor_key)
        if not current.lease_active:
            raise InvalidHandoff(f"actor {actor_key!r} has no active lease")
        if mode not in VALID_CONTROL_MODES:
            raise InvalidHandoff(f"invalid control mode {mode!r}")
        updated = EmbodimentState(
            actor_key=actor_key,
            controller_session=current.controller_session,
            control_mode=mode,
            lease_active=True,
            last_commit_seq=at_seq,
        )
        self._states[actor_key] = updated
        self._emit(actor_key, "mode_change", mode, current.controller_session, at_seq)
        return updated

    def release(self, actor_key: str, lease_id: str, *, released_seq: int) -> EmbodimentState:
        """Release the embodiment lease and hand back to autonomous."""
        self._require(actor_key)
        self._leases.release(lease_id, released_seq)
        updated = EmbodimentState(
            actor_key=actor_key,
            controller_session=None,
            control_mode="intent",
            lease_active=False,
            last_commit_seq=released_seq,
        )
        self._states[actor_key] = updated
        self._emit(actor_key, "release", updated.control_mode, None, released_seq)
        return updated

    def state(self, actor_key: str) -> EmbodimentState:
        return self._require(actor_key)

    def events(self, actor_key: str) -> tuple[ControlHandoffEvent, ...]:
        return self._events.get(actor_key, ())

    def shadow(self) -> ShadowPolicy:
        return self._shadow

    def _require(self, actor_key: str) -> EmbodimentState:
        state = self._states.get(actor_key)
        if state is None:
            raise InvalidHandoff(f"actor {actor_key!r} is not embodied")
        return state

    def _emit(
        self,
        actor_key: str,
        event_type: str,
        mode: ControlMode,
        session_id: str | None,
        at_seq: int,
    ) -> None:
        self._seq += 1
        event = ControlHandoffEvent(
            event_id=f"handoff_{self._seq:04d}",
            actor_key=actor_key,
            event_type=event_type,  # type: ignore[arg-type]
            control_mode=mode,
            controller_session=session_id,
            at_seq=at_seq,
        )
        self._events[actor_key] = self._events.get(actor_key, ()) + (event,)


def major_decision(actor_id: str, suggestion: str, *, advice_seq: int) -> None:
    """ShadowPolicy never makes major decisions: always raises ShadowCannotCommit."""
    raise ShadowCannotCommit(
        f"shadow cannot make the major decision {suggestion!r} for {actor_id!r}"
    )
