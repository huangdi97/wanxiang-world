"""Typed reputation events and immutable local/global projections (G93F)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

ReputationScope = Literal["local", "global"]
ReputationSignal = Literal[
    "kept_commitment",
    "provided_aid",
    "fulfilled_duty",
    "shared_resource",
    "violated_trust",
]
ReputationEvidenceKind = Literal["committed_event", "observation", "memory_observation"]
REPUTATION_SCOPES = ("local", "global")
REPUTATION_SIGNALS = (
    "kept_commitment",
    "provided_aid",
    "fulfilled_duty",
    "shared_resource",
    "violated_trust",
)
REPUTATION_EVIDENCE_KINDS = ("committed_event", "observation", "memory_observation")


@dataclass(frozen=True, slots=True)
class ReputationEvent:
    """An observer-visible social event; belief and rumor are not evidence kinds."""

    event_ref: str
    observer_id: EntityId
    subject_actor_id: EntityId
    dimension: str
    signal: ReputationSignal
    valence: float
    strength: float
    scope: ReputationScope
    scope_ref: str
    at_ticks: int
    evidence_ref: str
    evidence_kind: ReputationEvidenceKind = "committed_event"

    def __post_init__(self) -> None:
        if not self.event_ref.strip() or not self.evidence_ref.strip():
            raise ContractError("reputation event requires event and evidence refs")
        if self.observer_id == self.subject_actor_id:
            raise ContractError("reputation observer cannot be the subject")
        if not self.dimension.strip() or not self.scope_ref.strip():
            raise ContractError("reputation dimension and scope ref are required")
        if self.signal not in REPUTATION_SIGNALS:
            raise ContractError(f"invalid reputation signal {self.signal!r}")
        if self.evidence_kind not in REPUTATION_EVIDENCE_KINDS:
            raise ContractError("belief or rumor cannot update reputation")
        if not -1.0 <= self.valence <= 1.0 or not 0.0 <= self.strength <= 1.0:
            raise ContractError("reputation valence or strength is out of bounds")
        if self.scope not in REPUTATION_SCOPES or self.at_ticks < 0:
            raise ContractError("reputation scope or event time is invalid")


@dataclass(frozen=True, slots=True)
class ReputationState:
    """A non-canonical social reputation view with explicit scope and observer."""

    subject_actor_id: EntityId
    dimension: str
    scope: ReputationScope
    scope_ref: str
    score: float = 0.0
    observer_actor_id: EntityId | None = None
    updated_ticks: int = 0
    event_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if (
            not self.subject_actor_id.value
            or not self.dimension.strip()
            or not self.scope_ref.strip()
        ):
            raise ContractError("reputation state identity is incomplete")
        if self.scope not in REPUTATION_SCOPES or not -1.0 <= self.score <= 1.0:
            raise ContractError("reputation state scope or score is invalid")
        if self.observer_actor_id == self.subject_actor_id or self.updated_ticks < 0:
            raise ContractError("reputation observer or time is invalid")
        for field_name, refs in (
            ("event_refs", self.event_refs),
            ("evidence_refs", self.evidence_refs),
        ):
            if len(set(refs)) != len(refs) or any(not ref.strip() for ref in refs):
                raise ContractError(f"reputation {field_name} must be unique and non-blank")

    @property
    def key(self) -> tuple[EntityId, str, ReputationScope, str, EntityId | None]:
        return (
            self.subject_actor_id,
            self.dimension,
            self.scope,
            self.scope_ref,
            self.observer_actor_id,
        )

    @property
    def observer_specific(self) -> bool:
        return self.observer_actor_id is not None


@dataclass(frozen=True, slots=True)
class ReputationProjection:
    """Immutable collection of scoped reputation views; no canonical store."""

    states: tuple[ReputationState, ...] = ()

    def __post_init__(self) -> None:
        keys = tuple(item.key for item in self.states)
        if len(set(keys)) != len(keys):
            raise ContractError("reputation projection keys must be unique")

    def state(
        self,
        subject_actor_id: EntityId,
        dimension: str,
        scope: ReputationScope,
        scope_ref: str,
        observer_actor_id: EntityId | None = None,
    ) -> ReputationState | None:
        key = (subject_actor_id, dimension, scope, scope_ref, observer_actor_id)
        return next((item for item in self.states if item.key == key), None)

    def visible_to(self, viewer_actor_id: EntityId) -> tuple[ReputationState, ...]:
        return tuple(
            item
            for item in self.states
            if item.observer_actor_id is None or item.observer_actor_id == viewer_actor_id
        )
