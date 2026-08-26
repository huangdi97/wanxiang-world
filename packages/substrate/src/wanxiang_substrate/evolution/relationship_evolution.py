"""Rule-driven relationship evolution proposals and replayable feedback (G93D)."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.actor_continuity.relationship_graph import (
    RelationshipGraph,
    RelationshipRevisionEvent,
)
from wanxiang_substrate.actor_continuity.relationship_model import (
    RelationshipDimensions,
    RelationshipState,
)
from wanxiang_substrate.evolution.delta import EvolutionProvenance, RelationshipDelta

RelationshipDimension = Literal[
    "trust",
    "affection",
    "hostility",
    "debt",
    "loyalty",
    "dependency",
    "authority",
    "reputation",
]
RelationshipSignal = Literal[
    "shared_aid", "betrayal", "conflict", "debt_paid", "information_shared"
]
RELATIONSHIP_DIMENSIONS = tuple(RelationshipDimensions().to_dict())


@dataclass(frozen=True, slots=True)
class RelationshipEvolutionEvent:
    """An observed event that may produce a relationship projection proposal."""

    event_ref: str
    relationship_id: str
    source_actor_id: EntityId
    target_actor_id: EntityId
    signal: RelationshipSignal
    strength: float
    at_ticks: int
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.event_ref.strip() or not self.relationship_id.strip():
            raise ContractError("relationship evolution event requires ids")
        if self.source_actor_id == self.target_actor_id:
            raise ContractError("relationship evolution event cannot be self-directed")
        if self.signal not in (
            "shared_aid",
            "betrayal",
            "conflict",
            "debt_paid",
            "information_shared",
        ):
            raise ContractError(f"invalid relationship signal {self.signal!r}")
        if not 0.0 <= self.strength <= 1.0 or self.at_ticks < 0:
            raise ContractError("relationship event strength or time is invalid")
        if any(not ref.strip() for ref in self.evidence_refs):
            raise ContractError("relationship event evidence refs cannot be blank")


@dataclass(frozen=True, slots=True)
class RelationshipDeltaRule:
    """A bounded mapping from an observed signal to one relation dimension."""

    signal: RelationshipSignal
    dimension: RelationshipDimension
    coefficient: float
    maximum_step: float = 0.25

    def __post_init__(self) -> None:
        if self.signal not in (
            "shared_aid",
            "betrayal",
            "conflict",
            "debt_paid",
            "information_shared",
        ):
            raise ContractError(f"invalid relationship rule signal {self.signal!r}")
        if self.dimension not in RELATIONSHIP_DIMENSIONS:
            raise ContractError(f"invalid relationship rule dimension {self.dimension!r}")
        if not -1.0 <= self.coefficient <= 1.0:
            raise ContractError("relationship rule coefficient must be in [-1, 1]")
        if not 0.0 < self.maximum_step <= 0.5:
            raise ContractError("relationship rule maximum step must be in (0, 0.5]")


@dataclass(frozen=True, slots=True)
class RelationshipEvolutionProposal:
    """Proposal with before/after state and a typed G93A RelationshipDelta."""

    proposal_id: str
    before: RelationshipState
    after: RelationshipState
    delta: RelationshipDelta
    event: RelationshipEvolutionEvent
    provider_ref: str
    approved: bool = False

    def __post_init__(self) -> None:
        if not self.proposal_id.strip() or not self.provider_ref.strip():
            raise ContractError("relationship proposal requires id and provider")
        if self.before.relationship_id != self.after.relationship_id:
            raise ContractError("relationship proposal ids do not match")
        if self.delta.relationship_id != self.before.relationship_id:
            raise ContractError("relationship delta does not match proposal")
        if self.event.relationship_id != self.before.relationship_id:
            raise ContractError("relationship event does not match proposal")
        if self.event.at_ticks < self.before.valid_from:
            raise ContractError("relationship proposal moves backwards in time")


@dataclass(frozen=True, slots=True)
class RelationshipProviderProposal:
    """Provider output remains a proposal and can never be a commit authority."""

    provider_ref: str
    proposal: RelationshipEvolutionProposal

    def __post_init__(self) -> None:
        if not self.provider_ref.strip() or self.provider_ref in {
            "commit_authority",
            "commit-authority",
        }:
            raise PermissionDenied("Commit Authority cannot produce relationship proposals")
        if self.proposal.provider_ref != self.provider_ref:
            raise ContractError("provider proposal identity does not match")


@dataclass(frozen=True, slots=True)
class RelationshipBehaviorFeedback:
    """Read-only future behavior bias derived from relationship projection state."""

    relationship_id: str
    at_ticks: int
    cooperation_bias: float
    avoidance_bias: float
    source_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.relationship_id.strip() or self.at_ticks < 0:
            raise ContractError("relationship feedback identity or time is invalid")
        if not -1.0 <= self.cooperation_bias <= 1.0 or not 0.0 <= self.avoidance_bias <= 1.0:
            raise ContractError("relationship feedback is out of bounds")


def propose_relationship_evolution(
    *,
    proposal_id: str,
    state: RelationshipState,
    event: RelationshipEvolutionEvent,
    rules: tuple[RelationshipDeltaRule, ...],
    provenance: EvolutionProvenance,
    provider_ref: str = "policy:relationship",
) -> RelationshipEvolutionProposal:
    """Turn one event into a clamped projection proposal; no graph is mutated."""
    if event.relationship_id != state.relationship_id:
        raise ContractError("relationship event does not target state")
    if (event.source_actor_id, event.target_actor_id) != (
        state.source_actor_id,
        state.target_actor_id,
    ):
        raise ContractError("relationship event actors do not match state")
    matches = tuple(rule for rule in rules if rule.signal == event.signal)
    if len(matches) != 1:
        raise ContractError("relationship event requires exactly one evolution rule")
    rule = matches[0]
    before_value = getattr(state.dimensions, rule.dimension)
    change = max(-rule.maximum_step, min(rule.maximum_step, rule.coefficient * event.strength))
    after_value = round(max(-1.0, min(1.0, before_value + change)), 6)
    if after_value == before_value:
        raise ContractError("relationship event produces no bounded change")
    event_refs = tuple(sorted(set(provenance.event_refs + (event.event_ref,))))
    merged_provenance = EvolutionProvenance(
        origin_ref=provenance.origin_ref,
        source_refs=provenance.source_refs,
        event_refs=event_refs,
        producer=provenance.producer,
    )
    after = replace(
        state,
        dimensions=replace(state.dimensions, **{rule.dimension: after_value}),
        valid_from=event.at_ticks,
        event_refs=tuple(sorted(set(state.event_refs + event_refs + event.evidence_refs))),
    )
    delta = RelationshipDelta(
        delta_id=f"relationship_{proposal_id}",
        relationship_id=state.relationship_id,
        source_actor_id=state.source_actor_id,
        target_actor_id=state.target_actor_id,
        dimension=rule.dimension,
        before=before_value,
        after=after_value,
        reason=f"{event.signal}:{proposal_id}",
        provenance=merged_provenance,
    )
    return RelationshipEvolutionProposal(
        proposal_id=proposal_id,
        before=state,
        after=after,
        delta=delta,
        event=event,
        provider_ref=provider_ref,
    )


def apply_relationship_proposal(
    graph: RelationshipGraph,
    proposal: RelationshipEvolutionProposal,
) -> tuple[RelationshipGraph, RelationshipRevisionEvent]:
    """Append accepted projection history through the existing RelationshipGraph."""
    if not proposal.approved:
        raise PermissionDenied("relationship proposal requires explicit review")
    current = graph.state(proposal.before.relationship_id)
    if current != proposal.before:
        raise ContractError("relationship proposal is stale")
    return graph.revise(
        proposal.after,
        event_ref=proposal.event.event_ref,
        at_ticks=proposal.event.at_ticks,
        reason=proposal.delta.reason,
    )


def relationship_behavior_feedback(
    state: RelationshipState, *, at_ticks: int
) -> RelationshipBehaviorFeedback:
    """Project relation dimensions into bounded behavior bias without committing anything."""
    if at_ticks < state.valid_from:
        raise ContractError("relationship feedback time precedes state")
    dimensions = state.dimensions
    cooperation = max(
        -1.0,
        min(
            1.0,
            (dimensions.trust + dimensions.affection + dimensions.loyalty - dimensions.hostility)
            / 3,
        ),
    )
    avoidance = max(0.0, min(1.0, (dimensions.hostility + max(0.0, -dimensions.trust)) / 2))
    return RelationshipBehaviorFeedback(
        relationship_id=state.relationship_id,
        at_ticks=at_ticks,
        cooperation_bias=round(cooperation, 6),
        avoidance_bias=round(avoidance, 6),
        source_refs=state.event_refs,
    )
