"""Sanitized, derived evidence for one playable action.

This record is a response projection, not a persistence ledger. It is derived
after the injected runtime returns and contains hashes for user/session input
instead of the raw values.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from wanxiang_substrate.playable.action_model import ActionProposal
from wanxiang_substrate.playable.state_diff import CommittedStateDiff

PLAYER_EVIDENCE_SCHEMA_VERSION = 1


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class PlayerActionEvidence:
    """A sanitized trace from player input to a committed projection."""

    trace_id: str
    input_sha256: str
    session_ref: str
    proposal_ref: str
    command_id: str
    event_id: str
    instance_id: str
    branch_id: str
    actor_ref: str
    action_type: str
    proposal_status: str
    before_revision: int
    after_revision: int
    before_state_hash: str
    after_state_hash: str
    state_diff_event_id: str
    projection_ref: str
    stages: tuple[str, ...]
    redactions: tuple[str, ...]
    schema_version: int = PLAYER_EVIDENCE_SCHEMA_VERSION

    @classmethod
    def from_committed(
        cls,
        proposal: ActionProposal,
        *,
        command_id: str,
        event_id: str,
        before_revision: int,
        after_revision: int,
        before_state_hash: str,
        after_state_hash: str,
        diff: CommittedStateDiff,
    ) -> PlayerActionEvidence:
        input_sha = _digest(proposal.input_text)
        proposal_ref = f"proposal:{_digest(proposal.proposal_id)}"
        session_ref = f"session:{_digest(proposal.session_id)}"
        material = "|".join((proposal_ref, command_id, event_id, after_state_hash))
        return cls(
            trace_id=f"trace:{_digest(material)}",
            input_sha256=input_sha,
            session_ref=session_ref,
            proposal_ref=proposal_ref,
            command_id=command_id,
            event_id=event_id,
            instance_id=proposal.instance_id,
            branch_id=proposal.branch_id,
            actor_ref=f"actor:{_digest(proposal.actor_id)}",
            action_type=proposal.action_type,
            proposal_status=proposal.status,
            before_revision=before_revision,
            after_revision=after_revision,
            before_state_hash=before_state_hash,
            after_state_hash=after_state_hash,
            state_diff_event_id=diff.event_id,
            projection_ref=f"playable-action:{event_id}",
            stages=(
                "input",
                "proposal",
                "validate_resolve",
                "commit_authority",
                "state_diff",
                "projection",
            ),
            redactions=(
                "raw_input",
                "proposal_payload",
                "session_id",
                "actor_id",
                "source_path",
                "source_digest",
            ),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "trace_id": self.trace_id,
            "input_sha256": self.input_sha256,
            "session_ref": self.session_ref,
            "proposal_ref": self.proposal_ref,
            "command_id": self.command_id,
            "event_id": self.event_id,
            "instance_id": self.instance_id,
            "branch_id": self.branch_id,
            "actor_ref": self.actor_ref,
            "action_type": self.action_type,
            "proposal_status": self.proposal_status,
            "before_revision": self.before_revision,
            "after_revision": self.after_revision,
            "before_state_hash": self.before_state_hash,
            "after_state_hash": self.after_state_hash,
            "state_diff_event_id": self.state_diff_event_id,
            "projection_ref": self.projection_ref,
            "stages": list(self.stages),
            "redactions": list(self.redactions),
        }
