"""Bounded reputation evolution and review-gated projection advancement (G93F)."""

from __future__ import annotations

from dataclasses import dataclass, replace

from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.evolution.delta import EvolutionProvenance, StateDelta
from wanxiang_substrate.evolution.reputation_model import (
    ReputationEvent,
    ReputationProjection,
    ReputationScope,
    ReputationState,
)
from wanxiang_substrate.evolution.reputation_proposal import (
    ReputationUpdateProposal,
    reputation_field,
)


@dataclass(frozen=True, slots=True)
class ReputationPolicy:
    """Rate limits and reviewer authority for social reputation projections."""

    maximum_abs_change: float = 0.2
    minimum_strength: float = 0.0
    reviewers: tuple[str, ...] = ("reviewer", "policy", "actor")

    def __post_init__(self) -> None:
        if not 0.0 < self.maximum_abs_change <= 0.5:
            raise ContractError("reputation maximum change must be in (0, 0.5]")
        if not 0.0 <= self.minimum_strength <= 1.0:
            raise ContractError("reputation minimum strength must be in [0, 1]")
        if not self.reviewers or any(not reviewer.strip() for reviewer in self.reviewers):
            raise ContractError("reputation policy requires reviewers")


_DEFAULT_REPUTATION_POLICY = ReputationPolicy()


def _merged_provenance(
    provenance: EvolutionProvenance, events: tuple[ReputationEvent, ...]
) -> EvolutionProvenance:
    return EvolutionProvenance(
        origin_ref=provenance.origin_ref,
        source_refs=provenance.source_refs,
        event_refs=tuple(
            sorted(set(provenance.event_refs) | {event.event_ref for event in events})
        ),
        producer=provenance.producer,
    )


def _matches(state: ReputationState, event: ReputationEvent) -> bool:
    if (event.subject_actor_id, event.dimension, event.scope, event.scope_ref) != (
        state.subject_actor_id,
        state.dimension,
        state.scope,
        state.scope_ref,
    ):
        return False
    return state.observer_actor_id is None or event.observer_id == state.observer_actor_id


def propose_reputation_update(
    *,
    proposal_id: str,
    current: ReputationState,
    events: tuple[ReputationEvent, ...],
    provenance: EvolutionProvenance,
    provider_ref: str = "policy:reputation",
    policy: ReputationPolicy = _DEFAULT_REPUTATION_POLICY,
) -> ReputationUpdateProposal:
    """Aggregate new observed events into one bounded, review-gated proposal."""
    if not proposal_id.strip():
        raise ContractError("reputation proposal requires id")
    if not events:
        raise ContractError("reputation update requires social events")
    if any(event.at_ticks < current.updated_ticks for event in events):
        raise ContractError("reputation evidence precedes current state")
    if any(event.strength < policy.minimum_strength for event in events):
        raise ContractError("reputation event is below the evidence strength floor")
    matching = tuple(event for event in events if _matches(current, event))
    if len(matching) != len(events):
        raise ContractError("reputation evidence does not match projection scope")
    new_events = tuple(event for event in matching if event.event_ref not in current.event_refs)
    if not new_events:
        raise ContractError("reputation update contains no new evidence")
    total_strength = sum(event.strength for event in new_events)
    if total_strength <= 0.0:
        raise ContractError("reputation update requires positive evidence strength")
    weighted_valence = sum(event.valence * event.strength for event in new_events)
    change = policy.maximum_abs_change * weighted_valence / total_strength
    after_score = round(max(-1.0, min(1.0, current.score + change)), 6)
    if after_score == current.score:
        raise ContractError("reputation evidence produces no bounded change")
    merged = _merged_provenance(provenance, new_events)
    after = replace(
        current,
        score=after_score,
        updated_ticks=max(event.at_ticks for event in new_events),
        event_refs=current.event_refs + tuple(event.event_ref for event in new_events),
        evidence_refs=current.evidence_refs
        + tuple(
            event.evidence_ref
            for event in new_events
            if event.evidence_ref not in current.evidence_refs
        ),
    )
    delta = StateDelta(
        delta_id=f"reputation_{proposal_id}",
        subject_id=current.subject_actor_id,
        field=reputation_field(current),
        before=current.score,
        after=after_score,
        reason=f"social_event:{proposal_id}",
        provenance=merged,
    )
    return ReputationUpdateProposal(
        proposal_id=proposal_id,
        before=current,
        after=after,
        events=new_events,
        state_delta=delta,
        provenance=merged,
        provider_ref=provider_ref,
    )


def review_reputation_proposal(
    proposal: ReputationUpdateProposal,
    *,
    reviewer: str,
    approved: bool = True,
    policy: ReputationPolicy = _DEFAULT_REPUTATION_POLICY,
) -> ReputationUpdateProposal:
    """Record an explicit review decision without changing canonical state."""
    if reviewer not in policy.reviewers:
        raise PermissionDenied(f"reputation reviewer {reviewer!r} is not authorized")
    return replace(proposal, approved=approved)


def apply_reputation_proposal(
    current: ReputationState, proposal: ReputationUpdateProposal
) -> ReputationState:
    """Advance a reputation view only after explicit review and stale checking."""
    if not proposal.approved:
        raise PermissionDenied("reputation proposal requires explicit review")
    if current != proposal.before:
        raise ContractError("reputation proposal is stale")
    return proposal.after


def advance_reputation_projection(
    projection: ReputationProjection, proposal: ReputationUpdateProposal
) -> ReputationProjection:
    """Replace one immutable projection state; this is not a canonical commit."""
    current = projection.state(
        proposal.before.subject_actor_id,
        proposal.before.dimension,
        proposal.before.scope,
        proposal.before.scope_ref,
        proposal.before.observer_actor_id,
    )
    if current is None:
        raise ContractError("reputation projection state is missing")
    if current != proposal.before:
        raise ContractError("reputation projection proposal is stale")
    updated = apply_reputation_proposal(current, proposal)
    states = tuple(
        updated if item.key == proposal.before.key else item for item in projection.states
    )
    return ReputationProjection(states=states)


def empty_reputation_projection() -> ReputationProjection:
    """Return an explicit empty non-canonical social projection."""
    return ReputationProjection()


def initial_reputation_state(
    subject_actor_id: EntityId,
    *,
    dimension: str,
    scope: ReputationScope,
    scope_ref: str,
    observer_actor_id: EntityId | None = None,
) -> ReputationState:
    """Build a zero baseline for a scoped actor reputation view."""
    return ReputationState(
        subject_actor_id=subject_actor_id,
        dimension=dimension,
        scope=scope,
        scope_ref=scope_ref,
        observer_actor_id=observer_actor_id,
    )
