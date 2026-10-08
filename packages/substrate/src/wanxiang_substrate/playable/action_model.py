"""Immutable action proposal records used by the intent compiler."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ActorId, BranchId, CommandId, WorldInstanceId

ProposalStatus = Literal["proposed", "needs_clarification", "unsupported", "rejected"]


@dataclass(frozen=True, slots=True)
class ActionAffordance:
    action_type: str
    required_fields: tuple[str, ...] = ()
    text_aliases: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.action_type.strip():
            raise ContractError("affordance action_type must be non-empty")


@dataclass(frozen=True, slots=True)
class ActionProposal:
    """Immutable proposal; conversion to a command still requires Commit Authority."""

    proposal_id: str
    session_id: str
    instance_id: str
    branch_id: str
    actor_id: str
    action_type: str
    payload: Mapping[str, FieldValue]
    status: ProposalStatus
    input_text: str = ""
    clarification: str = ""
    rejection_reason: str = ""

    def __post_init__(self) -> None:
        if (
            not self.proposal_id
            or not self.session_id
            or not self.instance_id
            or not self.branch_id
        ):
            raise ContractError("proposal requires session and world refs")
        if self.status == "proposed" and (not self.action_type or not self.actor_id):
            raise ContractError("a proposed action requires action_type and actor_id")
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))

    @property
    def accepted(self) -> bool:
        return self.status == "proposed"

    def to_dict(self) -> dict[str, object]:
        return {
            "proposal_id": self.proposal_id,
            "session_id": self.session_id,
            "instance_id": self.instance_id,
            "branch_id": self.branch_id,
            "actor_id": self.actor_id,
            "action_type": self.action_type,
            "payload": dict(self.payload),
            "status": self.status,
            "input_text": self.input_text,
            "clarification": self.clarification,
            "rejection_reason": self.rejection_reason,
        }

    def to_command(self, expected_revision: int, command_id: str | None = None) -> CommandEnvelope:
        """Create a transport-neutral command proposal; this method never commits."""

        if not self.accepted:
            raise ContractError("only an accepted ActionProposal can become a command")
        return CommandEnvelope(
            command_id=CommandId(command_id) if command_id else CommandId.generate(),
            instance_id=WorldInstanceId(self.instance_id),
            branch_id=BranchId(self.branch_id),
            expected_revision=BranchRevision(expected_revision),
            action_type=self.action_type,
            payload=self.payload,
            actor_id=ActorId(self.actor_id),
        )


@dataclass(frozen=True, slots=True)
class IntentCompileResult:
    proposal: ActionProposal

    @property
    def status(self) -> ProposalStatus:
        return self.proposal.status
