"""R7 agent-harness contract: read-only world view, proposals, consequences.

An agent harness (DeepSeek Harness or any other) participates through this port
only. It can observe a world view, decide, and receive the committed or rejected
consequence; it can never append to canonical history, because this module holds
no authority and no commit path at all (a guard test asserts that).

`scripts/r7_reference_harness.py` is a real JSON-RPC process implementing the
protocol; it is a **reference** harness, never presented as the official DSH.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Protocol, cast

HARNESS_PROTOCOL = "wanxiang.r7.agent-harness-rpc.v1"

ERROR_UNKNOWN_METHOD = -32601
ERROR_INVALID_PARAMS = -32602
ERROR_HARNESS_FAILED = -32010


class HarnessError(Exception):
    """Base error for the agent-harness bridge."""


class HarnessUnavailable(HarnessError):
    """The harness process could not be started, or died or timed out."""


class HarnessProtocolError(HarnessError):
    """The harness answered something that does not match the protocol."""


@dataclass(frozen=True, slots=True)
class WorldObservation:
    """The read-only world view an agent harness is allowed to see."""

    worldline_id: str
    revision: int
    state_hash: str
    allowed_history: tuple[str, ...] = ()
    allowed_context: Mapping[str, str] = field(default_factory=dict[str, str])
    goal_hint: str = ""

    def payload(self) -> dict[str, object]:
        return {
            "worldlineId": self.worldline_id,
            "revision": self.revision,
            "stateHash": self.state_hash,
            "allowedHistory": list(self.allowed_history),
            "allowedContext": dict(self.allowed_context),
            "goalHint": self.goal_hint,
        }


@dataclass(frozen=True, slots=True)
class AgentProposal:
    """A proposal only: it carries no authority and no commit reference."""

    proposal_id: str
    action: str
    rationale_ref: str
    payload_digest: str

    def payload(self) -> dict[str, object]:
        return {
            "proposalId": self.proposal_id,
            "action": self.action,
            "rationaleRef": self.rationale_ref,
            "payloadDigest": self.payload_digest,
        }


@dataclass(frozen=True, slots=True)
class AgentDecision:
    """What the harness decided: a proposal, or an explicit abstention."""

    status: str
    proposal: AgentProposal | None
    reason: str

    def __post_init__(self) -> None:
        if self.status not in ("proposed", "abstained"):
            raise HarnessProtocolError(f"unknown decision status {self.status!r}")
        if self.status == "proposed" and self.proposal is None:
            raise HarnessProtocolError("a proposed decision must carry a proposal")
        if self.status == "abstained" and self.proposal is not None:
            raise HarnessProtocolError("an abstained decision must not carry a proposal")


@dataclass(frozen=True, slots=True)
class HarnessConsequence:
    """What the world did with the proposal, sent back to the harness."""

    worldline_id: str
    proposal_id: str
    status: str
    revision: int | None
    state_hash: str | None
    reason: str

    def __post_init__(self) -> None:
        if self.status not in ("committed", "rejected"):
            raise HarnessProtocolError(f"unknown consequence status {self.status!r}")

    def payload(self) -> dict[str, object]:
        return {
            "worldlineId": self.worldline_id,
            "proposalId": self.proposal_id,
            "status": self.status,
            "revision": self.revision,
            "stateHash": self.state_hash,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class HarnessInfo:
    """Harness identity, including whether it is the official DSH binary."""

    harness_id: str
    harness_version: str
    kind: str
    official_dsh: bool


class AgentHarnessProvider(Protocol):
    """The port the world host depends on; every transport implements it."""

    @property
    def provider_id(self) -> str:
        """Stable provider identity, recorded in the resolved graph."""
        ...

    def info(self) -> HarnessInfo:
        """Harness identity and whether it is the official DSH binary."""
        ...

    def decide(self, observation: WorldObservation) -> AgentDecision:
        """Ask the harness for a proposal; the harness cannot commit."""
        ...

    def deliver_consequence(self, consequence: HarnessConsequence) -> bool:
        """Tell the harness what happened, committed or rejected."""
        ...

    def close(self) -> None:
        """Release the harness process."""
        ...


def parse_decision(result: Mapping[str, object]) -> AgentDecision:
    """Build a decision from a harness response, rejecting anything malformed."""
    status = result.get("status")
    if not isinstance(status, str):
        raise HarnessProtocolError("harness decision is missing 'status'")
    raw = result.get("proposal")
    proposal: AgentProposal | None = None
    if raw is not None:
        if not isinstance(raw, Mapping):
            raise HarnessProtocolError("harness proposal must be an object")
        # SAFETY: the proposal arrives over the wire, so it is treated as an
        # untyped mapping and every field is validated as a non-empty string below.
        fields: dict[str, object] = {
            key: cast("Mapping[str, object]", raw).get(key)
            for key in ("proposalId", "action", "rationaleRef", "payloadDigest")
        }
        if not all(isinstance(value, str) and value for value in fields.values()):
            raise HarnessProtocolError("harness proposal is missing required fields")
        proposal = AgentProposal(
            proposal_id=str(fields["proposalId"]),
            action=str(fields["action"]),
            rationale_ref=str(fields["rationaleRef"]),
            payload_digest=str(fields["payloadDigest"]),
        )
    reason = result.get("reason")
    return AgentDecision(
        status=status,
        proposal=proposal,
        reason=reason if isinstance(reason, str) else "",
    )
