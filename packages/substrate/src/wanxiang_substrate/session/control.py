"""Human/Shadow control handoff (G05C).

ShadowPolicy is strictly advice-only: it can never submit canonical actions.
The human/lease holder commits actions through the normal command path; on
release the deterministic controller resumes from current world + memory state.
"""

from __future__ import annotations

from wanxiang_substrate.session.errors import (
    InvalidHandoff,
    ShadowCannotCommit,
)
from wanxiang_substrate.session.model import HandoffState


class ShadowPolicy:
    """Non-authoritative assistance channel."""

    def __init__(self) -> None:
        self._advice_log: dict[str, tuple[str, ...]] = {}

    def advise(self, actor_id: str, suggestion: str, *, advice_seq: int) -> tuple[str, ...]:
        """Shadow outputs only exist in the advice channel; never committed."""
        history = self._advice_log.get(actor_id, ())
        entry = f"advice:{advice_seq}:{suggestion}"
        self._advice_log[actor_id] = history + (entry,)
        return self._advice_log[actor_id]

    def history(self, actor_id: str) -> tuple[str, ...]:
        return self._advice_log.get(actor_id, ())

    def commit(self, *args: object, **kwargs: object) -> None:
        raise ShadowCannotCommit("shadow policy cannot commit canonical actions")


class ControlHandoff:
    """Authoritative per-actor handoff state machine."""

    def __init__(self, lease_service: object | None = None) -> None:
        from wanxiang_substrate.session.service import LeaseService

        self._leases = lease_service if lease_service is not None else LeaseService()
        self._states: dict[str, HandoffState] = {}

    def acquire(self, actor_id: str, controller_session: str, resume_ref: str = "") -> HandoffState:
        current = self._require(actor_id)
        if not current.can_transition_to("human_control"):
            raise InvalidHandoff(
                f"cannot acquire human control from {current.state} for {actor_id!r}"
            )
        updated = HandoffState(
            actor_id=actor_id,
            state="human_control",
            controller_session=controller_session,
            last_commit_seq=current.last_commit_seq,
            resume_ref=resume_ref,
        )
        self._states[actor_id] = updated
        return updated

    def hand_back(self, actor_id: str, last_commit_seq: int) -> HandoffState:
        current = self._require(actor_id)
        if not current.can_transition_to("handing_back"):
            raise InvalidHandoff(f"cannot hand back from {current.state} for {actor_id!r}")
        updated = HandoffState(
            actor_id=actor_id,
            state="handing_back",
            controller_session=None,
            last_commit_seq=last_commit_seq,
            resume_ref=current.resume_ref,
        )
        self._states[actor_id] = updated
        return updated

    def resume(self, actor_id: str) -> HandoffState:
        current = self._require(actor_id)
        if not current.can_transition_to("resuming_autonomous"):
            raise InvalidHandoff(f"cannot resume autonomous from {current.state} for {actor_id!r}")
        intermediate = HandoffState(
            actor_id=actor_id,
            state="resuming_autonomous",
            controller_session=None,
            last_commit_seq=current.last_commit_seq,
            resume_ref=current.resume_ref,
        )
        self._states[actor_id] = intermediate
        restored = HandoffState(
            actor_id=actor_id,
            state="autonomous",
            controller_session=None,
            last_commit_seq=current.last_commit_seq,
            resume_ref=current.resume_ref,
        )
        self._states[actor_id] = restored
        return restored

    def state(self, actor_id: str) -> HandoffState:
        return self._require(actor_id)

    def reset(self, actor_id: str) -> HandoffState:
        current = self._require(actor_id)
        restored = HandoffState(
            actor_id=actor_id,
            state="autonomous",
            controller_session=None,
            last_commit_seq=current.last_commit_seq,
            resume_ref=current.resume_ref,
        )
        self._states[actor_id] = restored
        return restored

    def _require(self, actor_id: str) -> HandoffState:
        return self._states.setdefault(
            actor_id,
            HandoffState(actor_id=actor_id, state="autonomous"),
        )
