"""Queryable explanations for typed evolution deltas and actor trajectories (G93G)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.evolution.actor_evolution import ActorEvolutionState, TrajectoryEntry
from wanxiang_substrate.evolution.delta import (
    EvolutionCommitPolicy,
    EvolutionDelta,
    OrganizationDelta,
    PersonaDelta,
    RelationshipDelta,
    StateDelta,
)

ExplainableSubjectKind = Literal["actor", "entity", "relationship", "organization"]


def _subject(delta: EvolutionDelta) -> tuple[ExplainableSubjectKind, str]:
    if isinstance(delta, StateDelta):
        return "entity", delta.subject_id.value
    if isinstance(delta, RelationshipDelta):
        return "relationship", delta.relationship_id
    if isinstance(delta, OrganizationDelta):
        return "organization", delta.organization_id.value
    return "actor", delta.actor_id.value


def _actor_refs(delta: EvolutionDelta) -> tuple[str, ...]:
    if isinstance(delta, RelationshipDelta):
        return (delta.source_actor_id.value, delta.target_actor_id.value)
    if isinstance(delta, OrganizationDelta):
        return (delta.actor_id.value,) if delta.actor_id is not None else ()
    if isinstance(delta, StateDelta):
        return (delta.subject_id.value,)
    return (delta.actor_id.value,)


def _reason(delta: EvolutionDelta) -> str:
    if isinstance(delta, PersonaDelta):
        return delta.rationale
    return delta.reason


@dataclass(frozen=True, slots=True)
class EvolutionExplanation:
    """Read-only explanation derived from one typed delta and its provenance."""

    explanation_id: str
    delta: EvolutionDelta
    projection_ref: str
    at_ticks: int
    trajectory_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.explanation_id.strip() or not self.projection_ref.strip():
            raise ContractError("evolution explanation requires ids")
        if self.at_ticks < 0:
            raise ContractError("evolution explanation time cannot be negative")
        if len(set(self.trajectory_refs)) != len(self.trajectory_refs) or any(
            not ref.strip() for ref in self.trajectory_refs
        ):
            raise ContractError("trajectory explanation refs must be unique and non-blank")
        EvolutionCommitPolicy.validate_proposal(self.delta)

    @property
    def delta_id(self) -> str:
        return self.delta.delta_id

    @property
    def delta_kind(self) -> str:
        return self.delta.kind

    @property
    def subject_kind(self) -> ExplainableSubjectKind:
        return _subject(self.delta)[0]

    @property
    def subject_ref(self) -> str:
        return _subject(self.delta)[1]

    @property
    def actor_refs(self) -> tuple[str, ...]:
        return _actor_refs(self.delta)

    @property
    def reason(self) -> str:
        return _reason(self.delta)

    @property
    def source_refs(self) -> tuple[str, ...]:
        return self.delta.provenance.source_refs

    @property
    def event_refs(self) -> tuple[str, ...]:
        return self.delta.provenance.event_refs

    @property
    def delta_fingerprint(self) -> str:
        return self.delta.fingerprint()

    def to_dict(self) -> dict[str, object]:
        return {
            "explanation_id": self.explanation_id,
            "delta_id": self.delta_id,
            "delta_kind": self.delta_kind,
            "subject_kind": self.subject_kind,
            "subject_ref": self.subject_ref,
            "projection_ref": self.projection_ref,
            "at_ticks": self.at_ticks,
            "reason": self.reason,
            "source_refs": list(self.source_refs),
            "event_refs": list(self.event_refs),
            "trajectory_refs": list(self.trajectory_refs),
            "delta_fingerprint": self.delta_fingerprint,
            "delta": self.delta.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class TrajectoryExplanationLink:
    """Explicit link from an existing ActorEvolution trajectory entry."""

    explanation_id: str
    actor_id: EntityId
    trajectory_seq: int
    trajectory_kind: str
    detail: str
    provenance_ref: str

    def __post_init__(self) -> None:
        if (
            not self.explanation_id.strip()
            or not self.trajectory_kind.strip()
            or not self.detail.strip()
            or not self.provenance_ref.strip()
        ):
            raise ContractError("trajectory explanation link is incomplete")
        if self.trajectory_seq < 1:
            raise ContractError("trajectory explanation sequence must be positive")


@dataclass(frozen=True, slots=True)
class EvolutionExplainabilityProjection:
    """Immutable query projection; it is neither canonical state nor an event store."""

    explanations: tuple[EvolutionExplanation, ...] = ()
    trajectory_links: tuple[TrajectoryExplanationLink, ...] = ()

    def __post_init__(self) -> None:
        explanation_ids = tuple(item.explanation_id for item in self.explanations)
        delta_ids = tuple(item.delta_id for item in self.explanations)
        if len(set(explanation_ids)) != len(explanation_ids):
            raise ContractError("explanation ids must be unique")
        if len(set(delta_ids)) != len(delta_ids):
            raise ContractError("each delta may have one explanation")
        known = set(explanation_ids)
        if any(item.explanation_id not in known for item in self.trajectory_links):
            raise ContractError("trajectory link references an unknown explanation")

    def by_delta(self, delta_id: str) -> EvolutionExplanation | None:
        return next((item for item in self.explanations if item.delta_id == delta_id), None)

    def for_subject(self, subject_ref: str) -> tuple[EvolutionExplanation, ...]:
        return tuple(item for item in self.explanations if item.subject_ref == subject_ref)

    def for_projection(self, projection_ref: str) -> tuple[EvolutionExplanation, ...]:
        return tuple(item for item in self.explanations if item.projection_ref == projection_ref)

    def links_for(self, actor_id: EntityId) -> tuple[TrajectoryExplanationLink, ...]:
        return tuple(item for item in self.trajectory_links if item.actor_id == actor_id)


def explain_delta(
    delta: EvolutionDelta,
    *,
    explanation_id: str,
    projection_ref: str,
    at_ticks: int,
    trajectory_refs: tuple[str, ...] = (),
) -> EvolutionExplanation:
    """Build a deterministic explanation from delta reason and evidence lineage."""
    return EvolutionExplanation(
        explanation_id=explanation_id,
        delta=delta,
        projection_ref=projection_ref,
        at_ticks=at_ticks,
        trajectory_refs=trajectory_refs,
    )


def link_actor_trajectory(
    state: ActorEvolutionState,
    explanation: EvolutionExplanation,
    *,
    trajectory_seq: int,
) -> TrajectoryExplanationLink:
    """Link an existing actor trajectory entry through an explicit provenance ref."""
    if state.actor_id.value not in explanation.actor_refs:
        raise ContractError("explanation does not target actor trajectory")
    entry = next((item for item in state.trajectory if item.seq == trajectory_seq), None)
    if entry is None:
        raise ContractError("trajectory sequence is missing")
    if entry.provenance_ref not in explanation.trajectory_refs:
        raise ContractError("trajectory link requires explicit explanation provenance")
    return _trajectory_link(explanation.explanation_id, state.actor_id, entry)


def _trajectory_link(
    explanation_id: str, actor_id: EntityId, entry: TrajectoryEntry
) -> TrajectoryExplanationLink:
    return TrajectoryExplanationLink(
        explanation_id=explanation_id,
        actor_id=actor_id,
        trajectory_seq=entry.seq,
        trajectory_kind=entry.kind,
        detail=entry.detail,
        provenance_ref=entry.provenance_ref,
    )


def advance_explainability_projection(
    projection: EvolutionExplainabilityProjection,
    explanation: EvolutionExplanation,
    *,
    trajectory_links: tuple[TrajectoryExplanationLink, ...] = (),
) -> EvolutionExplainabilityProjection:
    """Append one explanation and explicit trajectory links to the read model."""
    if projection.by_delta(explanation.delta_id) is not None:
        raise ContractError("delta explanation already exists")
    if any(link.explanation_id != explanation.explanation_id for link in trajectory_links):
        raise ContractError("trajectory link explanation identity does not match")
    return EvolutionExplainabilityProjection(
        explanations=projection.explanations + (explanation,),
        trajectory_links=projection.trajectory_links + trajectory_links,
    )
