"""Transport-neutral result records for the playable service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.playable.action_model import ActionProposal
from wanxiang_substrate.playable.state_diff import CommittedStateDiff


class SubmittedResult(Protocol):
    state: InMemoryCanonicalState
    event: object


class EventLike(Protocol):
    event_id: object


@dataclass(frozen=True, slots=True)
class PlayableActionResult:
    proposal: ActionProposal
    event_id: str
    revision: int
    state_hash: str
    diff: CommittedStateDiff

    def to_dict(self) -> dict[str, object]:
        return {
            "proposal": self.proposal.to_dict(),
            "event_id": self.event_id,
            "revision": self.revision,
            "state_hash": self.state_hash,
            "diff": self.diff.to_dict(),
        }
