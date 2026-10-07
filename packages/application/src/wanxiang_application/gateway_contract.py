"""World Capability Gateway contracts and least-privilege session identity.

These are data contracts only. They carry no commit capability and no canonical
state writer.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Literal

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import ContractError

GatewayOperation = Literal["fork_worldline", "request_experiment"]

_OPERATION_SCOPE = {
    "observe": "world.observe",
    "query_history": "world.history",
    "query_branch_diff": "world.branch.diff",
    "propose_action": "world.propose",
    "request_fork": "world.fork",
    "request_experiment": "world.experiment",
}


def _parse_expiry(value: str) -> datetime:
    """Parse an offset-aware ISO-8601 expiry and normalize it to UTC."""
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ContractError("session_expiry must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ContractError("session_expiry must include a timezone")
    return parsed.astimezone(UTC)


@dataclass(frozen=True, slots=True)
class AgentSessionIdentity:
    """Explicit least-privilege identity for one external-agent world session."""

    principal_id: str
    role: str
    world_id: str
    branch_id: str
    audit_id: str
    session_expiry: str
    actor_id: str = ""
    capability_scope: tuple[str, ...] = ()
    rights_scope: tuple[str, ...] = ()
    secret_scope: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "principal_id",
            "role",
            "world_id",
            "branch_id",
            "audit_id",
            "session_expiry",
        ):
            if not str(getattr(self, name)).strip():
                raise ContractError(f"{name} must be non-empty")
        for name in ("capability_scope", "rights_scope", "secret_scope"):
            values = getattr(self, name)
            if len(set(values)) != len(values) or any(not value.strip() for value in values):
                raise ContractError(f"{name} must contain unique non-empty values")
        if not self.capability_scope:
            raise ContractError("capability_scope must not be empty")
        if not self.rights_scope:
            raise ContractError("rights_scope must not be empty")
        _parse_expiry(self.session_expiry)


@dataclass(frozen=True, slots=True)
class WorldSkill:
    """Agent-facing use contract for one world session; never an authority token."""

    world_id: str
    branch_id: str
    principal_id: str
    role: str
    allowed_operations: tuple[str, ...]
    allowed_actions: tuple[str, ...]
    rights_scope: tuple[str, ...]
    actor_lease_present: bool
    secret_scope_present: bool
    approval_required: tuple[str, ...] = ("fork_worldline", "request_experiment")
    error_codes: tuple[str, ...] = (
        "contract_error",
        "permission_denied",
        "validation_rejected",
    )


@dataclass(frozen=True, slots=True)
class GatewayObservation:
    """Read-only projection of one canonical worldline."""

    world_id: str
    branch_id: str
    revision: int
    state_hash: str
    state: Mapping[str, object]
    action_types: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "state", MappingProxyType(dict(self.state)))


@dataclass(frozen=True, slots=True)
class GatewayHistoryItem:
    """One read-only history entry exposed to an external session."""

    event_id: str
    command_id: str
    revision: int
    event_seq: int
    actor_id: str
    world_time: int


@dataclass(frozen=True, slots=True)
class GatewayProposal:
    """Proposal-only command envelope; creating this object never commits it."""

    proposal_id: str
    audit_id: str
    command: CommandEnvelope


@dataclass(frozen=True, slots=True)
class GovernedOperationRequest:
    """A structural/experiment request that still requires a governance path."""

    request_id: str
    operation: GatewayOperation
    world_id: str
    branch_id: str
    audit_id: str
    parameters: Mapping[str, FieldValue]

    def __post_init__(self) -> None:
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))


__all__ = [
    "AgentSessionIdentity",
    "GatewayHistoryItem",
    "GatewayObservation",
    "GatewayOperation",
    "GatewayProposal",
    "GovernedOperationRequest",
    "WorldSkill",
]
