"""Production R7 loop binding an AgentHarnessProvider to governed WorldRuntime.

The harness remains proposal-only. This orchestrator may submit a proposal to the
existing WorldRuntime, whose resolver/invariants/CommitAuthority decide whether it
becomes canonical reality. Every proposed action receives a committed/rejected
consequence; a harness result can never write the event store directly.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import WanxiangError
from wanxiang_runtime.r7_agent_harness_contract import (
    AgentHarnessProvider,
    AgentProposal,
    HarnessConsequence,
    WorldObservation,
    proposal_payload_digest,
)

from wanxiang_application.gateway import AgentSessionIdentity, WorldCapabilityGateway
from wanxiang_application.world_runtime import WorldRuntime

_HarnessStepStatus = Literal["abstained", "committed", "rejected"]


@dataclass(frozen=True, slots=True)
class HarnessStepResult:
    """One governed harness turn and the canonical outcome it observed."""

    status: _HarnessStepStatus
    proposal_id: str | None
    revision: int
    state_hash: str
    reason: str
    consequence_acknowledged: bool | None


class HarnessWorldLoop:
    """Drive one external harness turn through the World Capability Gateway."""

    def __init__(
        self,
        runtime: WorldRuntime,
        provider: AgentHarnessProvider,
        *,
        gateway: WorldCapabilityGateway | None = None,
    ) -> None:
        self._runtime = runtime
        self._provider = provider
        self._gateway = gateway or WorldCapabilityGateway(runtime)

    def step(
        self,
        session: AgentSessionIdentity,
        *,
        goal_hint: str = "",
        allowed_context: Mapping[str, str] | None = None,
    ) -> HarnessStepResult:
        """Observe -> decide -> governed proposal -> commit/reject -> consequence."""
        observed = self._gateway.observe(session)
        history = self._gateway.query_history(session)
        decision = self._provider.decide(
            WorldObservation(
                worldline_id=session.branch_id,
                revision=observed.revision,
                state_hash=observed.state_hash,
                allowed_history=tuple(item.event_id for item in history),
                allowed_context=dict(allowed_context or {}),
                goal_hint=goal_hint,
            )
        )
        if decision.status == "abstained":
            return HarnessStepResult(
                status="abstained",
                proposal_id=None,
                revision=observed.revision,
                state_hash=observed.state_hash,
                reason=decision.reason,
                consequence_acknowledged=None,
            )

        proposal = decision.proposal
        assert proposal is not None
        expected_digest = proposal_payload_digest(proposal.action_payload)
        if proposal.payload_digest != expected_digest:
            return self._reject(
                session,
                proposal,
                observed.revision,
                observed.state_hash,
                "proposal payload digest mismatch",
            )

        try:
            gateway_proposal = self._gateway.propose_action(
                session,
                expected_revision=observed.revision,
                action_type=proposal.action,
                payload=proposal.action_payload,
            )
            committed = self._runtime.submit_command(gateway_proposal.command)
        except WanxiangError as exc:
            return self._reject(
                session,
                proposal,
                observed.revision,
                observed.state_hash,
                f"{exc.code}: {exc.message}",
            )

        consequence = HarnessConsequence(
            worldline_id=session.branch_id,
            proposal_id=proposal.proposal_id,
            status="committed",
            revision=committed.state.revision.value,
            state_hash=committed.state.semantic_hash(),
            reason="accepted by Wanxiang authority",
        )
        acknowledged = self._provider.deliver_consequence(consequence)
        return HarnessStepResult(
            status="committed",
            proposal_id=proposal.proposal_id,
            revision=committed.state.revision.value,
            state_hash=committed.state.semantic_hash(),
            reason=consequence.reason,
            consequence_acknowledged=acknowledged,
        )

    def _reject(
        self,
        session: AgentSessionIdentity,
        proposal: AgentProposal,
        revision: int,
        state_hash: str,
        reason: str,
    ) -> HarnessStepResult:
        consequence = HarnessConsequence(
            worldline_id=session.branch_id,
            proposal_id=proposal.proposal_id,
            status="rejected",
            revision=None,
            state_hash=None,
            reason=reason,
        )
        acknowledged = self._provider.deliver_consequence(consequence)
        return HarnessStepResult(
            status="rejected",
            proposal_id=proposal.proposal_id,
            revision=revision,
            state_hash=state_hash,
            reason=reason,
            consequence_acknowledged=acknowledged,
        )

    def close(self) -> None:
        """Close the provider transport/process owned by this loop."""
        self._provider.close()


__all__ = ["HarnessStepResult", "HarnessWorldLoop"]
