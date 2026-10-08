"""Safe public WorldHandle over the proposal/query gateway.

WorldHandle is the public entry point for one authenticated world session. It
never exposes the WorldRuntime, persistence backend, CommitAuthority, Cordis
root context or secrets. Structural operations and capability use are returned
as governed requests; ordinary action use returns a proposal only.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from wanxiang_domain.entity import FieldValue

from wanxiang_application.gateway import WorldCapabilityGateway
from wanxiang_application.gateway_contract import (
    AgentSessionIdentity,
    GatewayHistoryItem,
    GatewayObservation,
    GatewayProposal,
    GovernedOperationRequest,
    WorldSkill,
)
from wanxiang_application.world_runtime import WorldRuntime


@dataclass(frozen=True, slots=True)
class WorldHandleMetadata:
    """Safe session/world metadata; no provider or storage implementation leaks."""

    world_id: str
    branch_id: str
    principal_id: str
    role: str
    revision: int
    state_hash: str
    session_expiry: str


class WorldHandle:
    """Bounded observe/propose/history/branch/capability facade for one session."""

    __slots__ = ("__gateway", "__session")

    def __init__(self, runtime: WorldRuntime, session: AgentSessionIdentity) -> None:
        self.__gateway = WorldCapabilityGateway(runtime)
        self.__session = session

    def observe(self) -> GatewayObservation:
        """Return the scope-filtered canonical projection."""
        return self.__gateway.observe(self.__session)

    def history(
        self,
        *,
        after_revision: int = 0,
        limit: int = 100,
    ) -> tuple[GatewayHistoryItem, ...]:
        """Read committed history through the bounded gateway."""
        return self.__gateway.query_history(
            self.__session,
            after_revision=after_revision,
            limit=limit,
        )

    def propose(
        self,
        *,
        expected_revision: int,
        action_type: str,
        payload: Mapping[str, FieldValue],
    ) -> GatewayProposal:
        """Create a proposal only; WorldHandle cannot commit it."""
        return self.__gateway.propose_action(
            self.__session,
            expected_revision=expected_revision,
            action_type=action_type,
            payload=payload,
        )

    def branch(self, *, at_revision: int | None = None) -> GovernedOperationRequest:
        """Request a branch operation; governance/authority still decides."""
        return self.__gateway.request_fork(self.__session, at_revision=at_revision)

    def capability(
        self,
        capability_id: str,
        *,
        parameters: Mapping[str, FieldValue],
    ) -> GovernedOperationRequest:
        """Request capability execution without granting execution/commit authority."""
        return self.__gateway.request_experiment(
            self.__session,
            capability_id=capability_id,
            parameters=parameters,
        )

    def skill(self) -> WorldSkill:
        """Describe what this bound session is actually allowed to do."""
        return self.__gateway.describe_skill(self.__session)

    def metadata(self) -> WorldHandleMetadata:
        """Return safe identity/head metadata derived from the current observation."""
        observation = self.observe()
        return WorldHandleMetadata(
            world_id=observation.world_id,
            branch_id=observation.branch_id,
            principal_id=self.__session.principal_id,
            role=self.__session.role,
            revision=observation.revision,
            state_hash=observation.state_hash,
            session_expiry=self.__session.session_expiry,
        )


__all__ = ["WorldHandle", "WorldHandleMetadata"]
