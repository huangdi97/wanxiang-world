"""Agent-native query/proposal boundary; canonical writes stay in CommitAuthority."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import UTC, datetime

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import ContractError, PermissionDenied, ValidationRejected
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import ActorId, BranchId, CommandId, WorldInstanceId
from wanxiang_runtime.state import state_to_primitive

from wanxiang_application.gateway_contract import (
    AgentSessionIdentity,
    GatewayHistoryItem,
    GatewayObservation,
    GatewayProposal,
    GovernedOperationRequest,
    WorldSkill,
)
from wanxiang_application.gateway_queries import GatewayQueries
from wanxiang_application.world_runtime import WorldRuntime

_GatewayNow = Callable[[], datetime]
_RAW_CANONICAL_RIGHT = "world.canonical.read"

_OPERATION_SCOPE = {
    "observe": "world.observe",
    "inspect_world_metadata": "world.inspect",
    "inspect_world_schema": "world.inspect",
    "query_entities": "world.entities",
    "query_relations": "world.relations",
    "query_worldline": "world.worldline",
    "list_capabilities": "world.capabilities",
    "query_history": "world.history",
    "query_branch_diff": "world.branch.diff",
    "propose_action": "world.propose",
    "request_fork": "world.fork",
    "request_experiment": "world.experiment",
    "request_simulation": "world.simulation",
    "submit_order": "world.order",
}


class WorldCapabilityGateway:
    def __init__(self, runtime: WorldRuntime, *, now: _GatewayNow | None = None) -> None:
        self._runtime = runtime
        self._now = now or (lambda: datetime.now(UTC))

    def observe(self, session: AgentSessionIdentity) -> GatewayObservation:
        self._require_operation(session, "observe")
        instance_id, branch_id = self._refs(session)
        state = self._runtime.current_state(instance_id, branch_id)
        return GatewayObservation(
            world_id=instance_id.value,
            branch_id=branch_id.value,
            revision=state.revision.value,
            state_hash=state.semantic_hash(),
            state=state_to_primitive(state) if _RAW_CANONICAL_RIGHT in session.rights_scope else {},
            action_types=self._runtime.action_types(),
        )

    def inspect_world_metadata(self, session: AgentSessionIdentity) -> dict[str, object]:
        self._require_operation(session, "inspect_world_metadata")
        instance_id, branch_id = self._refs(session)
        return GatewayQueries.inspect_world_metadata(self._runtime, instance_id, branch_id)

    def inspect_world_schema(self, session: AgentSessionIdentity) -> dict[str, object]:
        self._require_operation(session, "inspect_world_schema")
        instance_id, _branch_id = self._refs(session)
        return GatewayQueries.inspect_world_schema(self._runtime, instance_id)

    def query_entities(self, session: AgentSessionIdentity) -> tuple[dict[str, object], ...]:
        self._require_operation(session, "query_entities")
        self._require_canonical_read(session)
        instance_id, branch_id = self._refs(session)
        return GatewayQueries.query_entities(self._runtime, instance_id, branch_id)

    def query_relations(self, session: AgentSessionIdentity) -> tuple[dict[str, object], ...]:
        self._require_operation(session, "query_relations")
        self._require_canonical_read(session)
        instance_id, branch_id = self._refs(session)
        return GatewayQueries.query_relations(self._runtime, instance_id, branch_id)

    def query_worldline(self, session: AgentSessionIdentity) -> dict[str, object]:
        self._require_operation(session, "query_worldline")
        instance_id, branch_id = self._refs(session)
        return GatewayQueries.query_worldline(self._runtime, instance_id, branch_id)

    def list_capabilities(self, session: AgentSessionIdentity) -> dict[str, tuple[str, ...]]:
        self._require_operation(session, "list_capabilities")
        return GatewayQueries.list_capabilities(self._runtime, session)

    def query_history(
        self,
        session: AgentSessionIdentity,
        *,
        after_revision: int = 0,
        limit: int = 100,
    ) -> tuple[GatewayHistoryItem, ...]:
        self._require_operation(session, "query_history")
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
        self,
        session: AgentSessionIdentity,
        other_branch_id: str,
    ) -> dict[str, tuple[str, ...]]:
        self._require_operation(session, "query_branch_diff")
        self._require_canonical_read(session)
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
        self._require_operation(session, "propose_action")
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
        self,
        session: AgentSessionIdentity,
        *,
        at_revision: int | None = None,
    ) -> GovernedOperationRequest:
        self._require_operation(session, "request_fork")
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
        self._require_operation(session, "request_experiment", capability_id=capability_id)
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

    def request_simulation(
        self,
        session: AgentSessionIdentity,
        *,
        simulation_id: str,
        parameters: Mapping[str, FieldValue],
    ) -> GovernedOperationRequest:
        self._require_operation(session, "request_simulation")
        instance_id, branch_id = self._refs(session)
        if not simulation_id.strip():
            raise ContractError("simulation_id must be non-empty")
        payload = dict(parameters)
        payload["simulation_id"] = simulation_id
        return GovernedOperationRequest(
            request_id=f"governed:{CommandId.generate().value}",
            operation="request_simulation",
            world_id=instance_id.value,
            branch_id=branch_id.value,
            audit_id=session.audit_id,
            parameters=payload,
        )

    def submit_order(
        self,
        session: AgentSessionIdentity,
        *,
        order_type: str,
        parameters: Mapping[str, FieldValue],
    ) -> GovernedOperationRequest:
        self._require_operation(session, "submit_order")
        instance_id, branch_id = self._refs(session)
        if not order_type.strip():
            raise ContractError("order_type must be non-empty")
        payload = dict(parameters)
        payload["order_type"] = order_type
        return GovernedOperationRequest(
            request_id=f"governed:{CommandId.generate().value}",
            operation="submit_order",
            world_id=instance_id.value,
            branch_id=branch_id.value,
            audit_id=session.audit_id,
            parameters=payload,
        )

    def describe_skill(self, session: AgentSessionIdentity) -> WorldSkill:
        self._refs(session)
        return GatewayQueries.describe_skill(self._runtime, session, _OPERATION_SCOPE)

    def _require_operation(
        self,
        session: AgentSessionIdentity,
        operation: str,
        *,
        capability_id: str = "",
    ) -> None:
        self._refs(session)
        required = _OPERATION_SCOPE[operation]
        if required in session.capability_scope:
            return
        if operation == "request_experiment" and capability_id in session.capability_scope:
            return
        raise PermissionDenied(f"session {session.audit_id} lacks capability scope {required!r}")

    @staticmethod
    def _require_canonical_read(session: AgentSessionIdentity) -> None:
        if _RAW_CANONICAL_RIGHT not in session.rights_scope:
            raise PermissionDenied("raw canonical query requires world.canonical.read right")

    def _refs(self, session: AgentSessionIdentity) -> tuple[WorldInstanceId, BranchId]:
        if session.expiry_utc() <= self._now().astimezone(UTC):
            raise PermissionDenied(f"session {session.audit_id} has expired")
        return WorldInstanceId(session.world_id), BranchId(session.branch_id)


__all__ = [
    "AgentSessionIdentity",
    "GatewayHistoryItem",
    "GatewayObservation",
    "GatewayProposal",
    "GovernedOperationRequest",
    "WorldCapabilityGateway",
    "WorldSkill",
]
