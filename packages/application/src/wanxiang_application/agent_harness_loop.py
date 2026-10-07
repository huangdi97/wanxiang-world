"""Production R7 loop binding an AgentHarnessProvider to governed WorldRuntime.

The harness remains proposal-only. This orchestrator may submit a proposal to the
existing WorldRuntime, whose resolver/invariants/CommitAuthority decide whether it
becomes canonical reality. Every proposed action receives a committed/rejected
consequence; a harness result can never write the event store directly.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import Literal

from wanxiang_domain.errors import WanxiangError
from wanxiang_domain.hashing import semantic_sha256
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_runtime.r7_agent_harness_contract import (
    AgentHarnessProvider,
    AgentProposal,
    HarnessConsequence,
    WorldObservation,
    proposal_payload_digest,
)

from wanxiang_application.gateway import (
    AgentSessionIdentity,
    GatewayHistoryItem,
    WorldCapabilityGateway,
)
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
    trajectory_recorded: bool | None = None


class HarnessWorldLoop:
    """Drive one external harness turn through the World Capability Gateway."""

    def __init__(
        self,
        runtime: WorldRuntime,
        provider: AgentHarnessProvider,
        *,
        gateway: WorldCapabilityGateway | None = None,
        trajectory_sink: Callable[[Mapping[str, object]], object] | None = None,
    ) -> None:
        self._runtime = runtime
        self._provider = provider
        self._gateway = gateway or WorldCapabilityGateway(runtime)
        self._trajectory_sink = trajectory_sink

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
        context = dict(allowed_context or {})
        context_hash = semantic_sha256(context)
        goal_refs = (f"goal-sha256:{semantic_sha256(goal_hint)}",) if goal_hint else ()
        decision = self._provider.decide(
            WorldObservation(
                worldline_id=session.branch_id,
                revision=observed.revision,
                state_hash=observed.state_hash,
                allowed_history=tuple(item.event_id for item in history),
                allowed_context=context,
                goal_hint=goal_hint,
            )
        )
        if decision.status == "abstained":
            result = HarnessStepResult(
                status="abstained",
                proposal_id=None,
                revision=observed.revision,
                state_hash=observed.state_hash,
                reason=decision.reason,
                consequence_acknowledged=None,
            )
            return self._attach_trajectory(
                session,
                history,
                None,
                result,
                context_hash=context_hash,
                goal_refs=goal_refs,
            )

        proposal = decision.proposal
        assert proposal is not None
        expected_digest = proposal_payload_digest(proposal.action_payload)
        if proposal.payload_digest != expected_digest:
            result = self._reject(
                session,
                proposal,
                observed.revision,
                observed.state_hash,
                "proposal payload digest mismatch",
            )
            return self._attach_trajectory(
                session,
                history,
                proposal,
                result,
                context_hash=context_hash,
                goal_refs=goal_refs,
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
            result = self._reject(
                session,
                proposal,
                observed.revision,
                observed.state_hash,
                f"{exc.code}: {exc.message}",
            )
            return self._attach_trajectory(
                session,
                history,
                proposal,
                result,
                context_hash=context_hash,
                goal_refs=goal_refs,
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
        result = HarnessStepResult(
            status="committed",
            proposal_id=proposal.proposal_id,
            revision=committed.state.revision.value,
            state_hash=committed.state.semantic_hash(),
            reason=consequence.reason,
            consequence_acknowledged=acknowledged,
        )
        return self._attach_trajectory(
            session,
            history,
            proposal,
            result,
            context_hash=context_hash,
            goal_refs=goal_refs,
        )

    def _attach_trajectory(
        self,
        session: AgentSessionIdentity,
        history: tuple[GatewayHistoryItem, ...],
        proposal: AgentProposal | None,
        result: HarnessStepResult,
        *,
        context_hash: str,
        goal_refs: tuple[str, ...],
    ) -> HarnessStepResult:
        sink = self._trajectory_sink
        if sink is None:
            return result
        world_event_refs: tuple[str, ...] = ()
        if result.status == "committed":
            events = self._runtime.events(
                WorldInstanceId(session.world_id),
                BranchId(session.branch_id),
            )
            if events:
                world_event_refs = (events[-1].event_id.value,)
        proposal_id = proposal.proposal_id if proposal is not None else f"abstain:{result.revision}"
        payload = {
            "trajectory_id": f"trajectory:{session.audit_id}:{proposal_id}:{result.status}",
            "actor_id": session.actor_id or session.principal_id,
            "world_id": session.world_id,
            "worldline_id": session.branch_id,
            "decision_id": proposal_id,
            "created_at": datetime.now(UTC).isoformat(),
            "observation_refs": tuple(item.event_id for item in history),
            "memory_refs": (),
            "memory_hashes": (),
            "belief_refs": (),
            "goal_refs": goal_refs,
            "context_hash": context_hash,
            "provider_id": self._provider.provider_id,
            "model_id": "",
            "tool_refs": (proposal.action,) if proposal is not None else (),
            "plan_ref": "",
            "intent_ref": "",
            "adjudication_ref": f"wanxiang:{result.status}",
            "outcome_ref": world_event_refs[0] if world_event_refs else f"outcome:{result.status}",
            "world_event_refs": world_event_refs,
            "rights_scope": session.rights_scope,
            "retention_until": "",
            "redacted": False,
        }
        try:
            sink(payload)
        except Exception:
            return replace(result, trajectory_recorded=False)
        return replace(result, trajectory_recorded=True)

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
