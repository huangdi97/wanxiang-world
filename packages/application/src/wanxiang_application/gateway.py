"""World Capability Gateway: agent-native query/proposal boundary over one WorldRuntime.

The gateway intentionally has no commit method. It turns an authenticated world
session into read/query views and proposal/governance requests; canonical writes
remain owned by WorldRuntime -> CommitAuthority.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import ContractError, ValidationRejected
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ActorId, BranchId, CommandId, WorldInstanceId
from wanxiang_runtime.state import state_to_primitive

from wanxiang_application.world_runtime import WorldRuntime

GatewayOperation = Literal["fork_worldline", "request_experiment"]


@dataclass(frozen=True, slots=True)
class AgentSessionIdentity:
    """Explicit least-privilege identity for one external-agent world session."""

    principal_id: str
    role: str
    world_id: str
    branch_id: str
    audit_id: str
    actor_id: str = ""
    capability_scope: tuple[str, ...] = ()
    rights_scope: tuple[str, ...] = ()
    secret_scope: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("principal_id", "role", "world_id", "branch_id", "audit_id"):
            if not str(getattr(self, name)).strip():
                raise ContractError(f"{name} must be non-empty")
        for name in ("capability_scope", "rights_scope", "secret_scope"):
            values = getattr(self, name)
            if len(set(values)) != len(values) or any(not value.strip() for value in values):
                raise ContractError(f"{name} must contain unique non-empty values")


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


class WorldCapabilityGateway:
    """Python SDK adapter for agent-native world access without direct commit."""

    def __init__(self, runtime: WorldRuntime) -> None:
        self._runtime = runtime

    def observe(self, session: AgentSessionIdentity) -> GatewayObservation:
        instance_id, branch_id = self._refs(session)
        state = self._runtime.current_state(instance_id, branch_id)
        return GatewayObservation(
            world_id=instance_id.value,
            branch_id=branch_id.value,
            revision=state.revision.value,
            state_hash=state.semantic_hash(),
            state=state_to_primitive(state),
            action_types=self._runtime.action_types(),
        )

    def query_history(
        self,
        session: AgentSessionIdentity,
        *,
        after_revision: int = 0,
        limit: int = 100,
    ) -> tuple[GatewayHistoryItem, ...]:
        if after_revision < 0:
            raise ContractError("after_revision must be >= 0")
        if limit < 1 or limit > 500:
            raise ContractError("limit must be within 1..500")
        instance_id, branch_id = self._refs(session)
        events = (
            event
            for event in self._runtime.events(instance_id, branch_id)
            if event.revision.value > after_revision
        )
        return tuple(
            GatewayHistoryItem(
                event_id=event.event_id.value,
                command_id=event.command_id.value,
                revision=event.revision.value,
                event_seq=event.event_seq.value,
                actor_id=event.actor_id.value if event.actor_id is not None else "",
                world_time=event.world_time.ticks,
            )
            for event in list(events)[:limit]
        )

    def query_branch_diff(
        self, session: AgentSessionIdentity, other_branch_id: str
    ) -> dict[str, tuple[str, ...]]:
        instance_id, branch_id = self._refs(session)
        other = BranchId(other_branch_id)
        diff = self._runtime.diff(instance_id, branch_id, other)
        return {
            "added_entities": tuple(item.value for item in diff.added_entities),
            "removed_entities": tuple(item.value for item in diff.removed_entities),
            "updated_entities": tuple(item.value for item in diff.updated_entities),
            "added_relations": tuple(item.value for item in diff.added_relations),
            "removed_relations": tuple(item.value for item in diff.removed_relations),
        }

    def propose_action(
        self,
        session: AgentSessionIdentity,
        *,
        expected_revision: int,
        action_type: str,
        payload: Mapping[str, FieldValue],
    ) -> GatewayProposal:
        instance_id, branch_id = self._refs(session)
        if not session.actor_id:
            raise ValidationRejected("an action proposal requires an actor lease")
        if action_type not in self._runtime.action_types():
            raise ValidationRejected(f"unsupported action_type {action_type!r}")
        if expected_revision < 0:
            raise ContractError("expected_revision must be >= 0")
        command_id = CommandId.generate()
        command = CommandEnvelope(
            command_id=command_id,
            instance_id=instance_id,
            branch_id=branch_id,
            expected_revision=BranchRevision(expected_revision),
            action_type=action_type,
            payload=dict(payload),
            actor_id=ActorId(session.actor_id),
        )
        return GatewayProposal(
            proposal_id=f"proposal:{command_id.value}",
            audit_id=session.audit_id,
            command=command,
        )

    def request_fork(
        self, session: AgentSessionIdentity, *, at_revision: int | None = None
    ) -> GovernedOperationRequest:
        instance_id, branch_id = self._refs(session)
        if at_revision is not None and at_revision < 0:
            raise ContractError("at_revision must be >= 0")
        params: dict[str, FieldValue] = {}
        if at_revision is not None:
            params["at_revision"] = at_revision
        return GovernedOperationRequest(
            request_id=f"governed:{CommandId.generate().value}",
            operation="fork_worldline",
            world_id=instance_id.value,
            branch_id=branch_id.value,
            audit_id=session.audit_id,
            parameters=params,
        )

    def request_experiment(
        self,
        session: AgentSessionIdentity,
        *,
        capability_id: str,
        parameters: Mapping[str, FieldValue],
    ) -> GovernedOperationRequest:
        instance_id, branch_id = self._refs(session)
        if not capability_id.strip():
            raise ContractError("capability_id must be non-empty")
        payload = dict(parameters)
        payload["capability_id"] = capability_id
        return GovernedOperationRequest(
            request_id=f"governed:{CommandId.generate().value}",
            operation="request_experiment",
            world_id=instance_id.value,
            branch_id=branch_id.value,
            audit_id=session.audit_id,
            parameters=payload,
        )

    @staticmethod
    def _refs(session: AgentSessionIdentity) -> tuple[WorldInstanceId, BranchId]:
        return WorldInstanceId(session.world_id), BranchId(session.branch_id)


__all__ = [
    "AgentSessionIdentity",
    "GatewayHistoryItem",
    "GatewayObservation",
    "GatewayProposal",
    "GovernedOperationRequest",
    "WorldCapabilityGateway",
]
