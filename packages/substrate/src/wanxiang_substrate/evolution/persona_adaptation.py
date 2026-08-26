"""Slow, evidence-windowed persona adaptation proposals (G93C)."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.evolution.delta import (
    EvolutionProvenance,
    PersonaDelta,
)

PersonaTrait = Literal["trust", "caution", "openness", "resolve", "empathy", "discipline"]
PersonaDirection = Literal["increase", "decrease"]
PersonaProposalStatus = Literal["review", "approved", "rejected"]
PERSONA_TRAITS = ("trust", "caution", "openness", "resolve", "empathy", "discipline")


@dataclass(frozen=True, slots=True)
class PersonaTraitState:
    """A slow actor-local trait variable bounded to [-1, 1]."""

    actor_id: EntityId
    trait: PersonaTrait
    value: float = 0.0
    updated_ticks: int = 0
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.trait not in PERSONA_TRAITS:
            raise ContractError(f"unsupported persona trait {self.trait!r}")
        if not -1.0 <= self.value <= 1.0 or self.updated_ticks < 0:
            raise ContractError("persona trait value or time is invalid")
        if any(not ref.strip() for ref in self.evidence_refs):
            raise ContractError("persona trait evidence refs cannot be blank")


@dataclass(frozen=True, slots=True)
class PersonaObservation:
    """One event-bound signal; it cannot rewrite a persona by itself."""

    observation_id: str
    actor_id: EntityId
    trait: PersonaTrait
    direction: PersonaDirection
    strength: float
    at_ticks: int
    event_ref: str

    def __post_init__(self) -> None:
        if not self.observation_id.strip() or not self.event_ref.strip():
            raise ContractError("persona observation requires ids")
        if self.trait not in PERSONA_TRAITS or self.direction not in ("increase", "decrease"):
            raise ContractError("invalid persona observation dimension")
        if not 0.0 < self.strength <= 1.0 or self.at_ticks < 0:
            raise ContractError("persona observation strength or time is invalid")


@dataclass(frozen=True, slots=True)
class PersonaAdaptationPolicy:
    """Review and rate limits for slow-variable persona changes."""

    window_ticks: int = 30
    minimum_observations: int = 3
    minimum_span_ticks: int = 7
    maximum_abs_change: float = 0.1
    reviewers: tuple[str, ...] = ("reviewer", "policy", "actor")

    def __post_init__(self) -> None:
        if self.window_ticks < 1 or self.minimum_observations < 2:
            raise ContractError("persona policy window and observation floors are invalid")
        if self.minimum_span_ticks < 1 or not 0.0 < self.maximum_abs_change <= 0.25:
            raise ContractError("persona policy change limits are invalid")
        if not self.reviewers or any(not item.strip() for item in self.reviewers):
            raise ContractError("persona policy requires reviewers")


_DEFAULT_PERSONA_POLICY = PersonaAdaptationPolicy()


@dataclass(frozen=True, slots=True)
class PersonaAdaptationProposal:
    """A one-trait, review-gated adaptation proposal."""

    proposal_id: str
    actor_id: EntityId
    trait: PersonaTrait
    window_start: int
    window_end: int
    before: float
    after: float
    evidence_refs: tuple[str, ...]
    rationale: str
    persona_delta: PersonaDelta
    review_required: bool = True
    status: PersonaProposalStatus = "review"

    def __post_init__(self) -> None:
        if not self.proposal_id.strip() or not self.rationale.strip():
            raise ContractError("persona proposal requires id and rationale")
        if self.trait not in PERSONA_TRAITS or self.window_start < 0:
            raise ContractError("persona proposal dimension or window is invalid")
        if self.window_end < self.window_start or not -1.0 <= self.before <= 1.0:
            raise ContractError("persona proposal window or before value is invalid")
        if not -1.0 <= self.after <= 1.0:
            raise ContractError("persona proposal after value is invalid")
        if abs(self.after - self.before) > 0.25:
            raise ContractError("persona proposal change is not bounded")
        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise ContractError("persona proposal requires evidence refs")
        if self.persona_delta.actor_id != self.actor_id or self.persona_delta.trait != self.trait:
            raise ContractError("persona delta does not match proposal")
        if self.status not in ("review", "approved", "rejected"):
            raise ContractError(f"invalid persona proposal status {self.status!r}")
        if self.status == "review" and not self.review_required:
            raise ContractError("review proposals must require review")


def propose_persona_adaptation(
    *,
    proposal_id: str,
    current: PersonaTraitState,
    observations: tuple[PersonaObservation, ...],
    now_ticks: int,
    provenance: EvolutionProvenance,
    policy: PersonaAdaptationPolicy = _DEFAULT_PERSONA_POLICY,
) -> PersonaAdaptationProposal:
    """Aggregate a sufficiently long evidence window into one bounded proposal."""
    if now_ticks < current.updated_ticks:
        raise ContractError("persona adaptation time cannot move backwards")
    start = max(current.updated_ticks, now_ticks - policy.window_ticks)
    window = tuple(
        item
        for item in observations
        if item.actor_id == current.actor_id
        and item.trait == current.trait
        and start <= item.at_ticks <= now_ticks
    )
    if len(window) < policy.minimum_observations:
        raise ContractError("persona adaptation requires a multi-event evidence window")
    event_times = [item.at_ticks for item in window]
    if max(event_times) - min(event_times) < policy.minimum_span_ticks:
        raise ContractError("persona adaptation evidence window is too short")
    total_strength = sum(item.strength for item in window)
    signed_strength = sum(
        item.strength if item.direction == "increase" else -item.strength for item in window
    )
    ratio = signed_strength / total_strength
    change = round(policy.maximum_abs_change * ratio, 6)
    after = round(max(-1.0, min(1.0, current.value + change)), 6)
    if after == current.value:
        raise ContractError("persona evidence does not support a change")
    refs = tuple(sorted({item.event_ref for item in window}))
    merged_provenance = EvolutionProvenance(
        origin_ref=provenance.origin_ref,
        source_refs=provenance.source_refs,
        event_refs=tuple(sorted(set(provenance.event_refs + refs))),
        producer=provenance.producer,
    )
    delta = PersonaDelta(
        actor_id=current.actor_id,
        trait=current.trait,
        from_value=f"{current.value:.6f}",
        to_value=f"{after:.6f}",
        rationale=f"windowed:{proposal_id}",
        evidence_refs=refs,
        delta_id=f"persona_{proposal_id}",
        provenance=merged_provenance,
    )
    return PersonaAdaptationProposal(
        proposal_id=proposal_id,
        actor_id=current.actor_id,
        trait=current.trait,
        window_start=start,
        window_end=now_ticks,
        before=current.value,
        after=after,
        evidence_refs=refs,
        rationale=f"{len(window)} observations across {max(event_times) - min(event_times)} ticks",
        persona_delta=delta,
    )


def review_persona_adaptation(
    proposal: PersonaAdaptationProposal,
    *,
    reviewer: str,
    approved: bool,
    policy: PersonaAdaptationPolicy = _DEFAULT_PERSONA_POLICY,
) -> PersonaAdaptationProposal:
    """Record an explicit immutable review decision; no world mutation occurs."""
    if reviewer not in policy.reviewers:
        raise PermissionDenied(f"persona reviewer {reviewer!r} is not authorized")
    return replace(
        proposal,
        review_required=not approved,
        status="approved" if approved else "rejected",
        rationale=(
            f"{proposal.rationale}; reviewed:{reviewer}:"
            f"{'approved' if approved else 'rejected'}"
        ),
    )
