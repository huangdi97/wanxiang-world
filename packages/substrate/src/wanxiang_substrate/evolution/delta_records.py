"""The six explicit payloads in the evolution Delta taxonomy."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.actor_continuity.relationship_model import RelationshipDimensions
from wanxiang_substrate.capability.model import validate_capability_name
from wanxiang_substrate.evolution.delta_common import (
    EVOLUTION_DELTA_SCHEMA_VERSION,
    BeliefOperation,
    BeliefStance,
    DeltaRecord,
    EvolutionDeltaKind,
    EvolutionProvenance,
    OrganizationLifecycle,
    PrimitiveValue,
    common_checks,
    level,
    refs,
    text,
)


@dataclass(frozen=True, slots=True)
class StateDelta(DeltaRecord):
    """A bounded scalar state change for a world/entity projection."""

    delta_id: str
    subject_id: EntityId
    field: str
    before: PrimitiveValue
    after: PrimitiveValue
    reason: str
    provenance: EvolutionProvenance
    schema_version: int = EVOLUTION_DELTA_SCHEMA_VERSION
    version: int = 1
    kind: ClassVar[EvolutionDeltaKind] = "state"

    def __post_init__(self) -> None:
        common_checks(self.delta_id, self.schema_version, self.version, self.provenance)
        text(self.field, "field")
        text(self.reason, "reason")
        if self.before == self.after:
            raise ContractError("state delta must change the value")
        if any(
            not isinstance(value, (str, int, float, bool)) and value is not None
            for value in (self.before, self.after)
        ):
            raise ContractError("state delta values must be scalar")


@dataclass(frozen=True, slots=True)
class BeliefDelta(DeltaRecord):
    """A belief-projection revision, never a World Truth mutation."""

    delta_id: str
    actor_id: EntityId
    belief_id: EntityId
    operation: BeliefOperation
    confidence_before: float
    confidence_after: float
    stance_before: BeliefStance
    stance_after: BeliefStance
    reason: str
    provenance: EvolutionProvenance
    schema_version: int = EVOLUTION_DELTA_SCHEMA_VERSION
    version: int = 1
    kind: ClassVar[EvolutionDeltaKind] = "belief"

    def __post_init__(self) -> None:
        common_checks(self.delta_id, self.schema_version, self.version, self.provenance)
        level(self.confidence_before, "confidence_before")
        level(self.confidence_after, "confidence_after")
        if self.operation not in ("support", "contradict", "refine", "unknown"):
            raise ContractError(f"invalid belief operation {self.operation!r}")
        valid_stances = ("supported", "contested", "unknown")
        if self.stance_before not in valid_stances or self.stance_after not in valid_stances:
            raise ContractError("invalid belief stance")
        text(self.reason, "reason")
        if (
            self.confidence_before == self.confidence_after
            and self.stance_before == self.stance_after
        ):
            raise ContractError("belief delta must change confidence or stance")


@dataclass(frozen=True, slots=True)
class RelationshipDelta(DeltaRecord):
    """One bounded relationship dimension revision."""

    delta_id: str
    relationship_id: str
    source_actor_id: EntityId
    target_actor_id: EntityId
    dimension: str
    before: float
    after: float
    reason: str
    provenance: EvolutionProvenance
    schema_version: int = EVOLUTION_DELTA_SCHEMA_VERSION
    version: int = 1
    kind: ClassVar[EvolutionDeltaKind] = "relationship"

    def __post_init__(self) -> None:
        common_checks(self.delta_id, self.schema_version, self.version, self.provenance)
        text(self.relationship_id, "relationship_id")
        text(self.dimension, "dimension")
        level(self.before, "before", low=-1.0)
        level(self.after, "after", low=-1.0)
        if self.dimension not in RelationshipDimensions().to_dict():
            raise ContractError(f"unsupported relationship dimension {self.dimension!r}")
        if self.source_actor_id == self.target_actor_id:
            raise ContractError("relationship delta cannot target the same actor")
        text(self.reason, "reason")
        if self.before == self.after:
            raise ContractError("relationship delta must change the value")


@dataclass(frozen=True, slots=True)
class CapabilityEvolutionDelta(DeltaRecord):
    """Evidence-backed capability change with bounded before/after values."""

    delta_id: str
    actor_id: EntityId
    capability: str
    level_before: int
    level_after: int
    mastery_before: float
    mastery_after: float
    confidence_before: float
    confidence_after: float
    reason: str
    provenance: EvolutionProvenance
    schema_version: int = EVOLUTION_DELTA_SCHEMA_VERSION
    version: int = 1
    kind: ClassVar[EvolutionDeltaKind] = "capability"

    def __post_init__(self) -> None:
        common_checks(self.delta_id, self.schema_version, self.version, self.provenance)
        validate_capability_name(self.capability)
        if any(
            type(value) is not int or not 0 <= value <= 10
            for value in (self.level_before, self.level_after)
        ):
            raise ContractError("capability levels must be integers in [0, 10]")
        for field_name, value in (
            ("mastery_before", self.mastery_before),
            ("mastery_after", self.mastery_after),
            ("confidence_before", self.confidence_before),
            ("confidence_after", self.confidence_after),
        ):
            level(value, field_name)
        text(self.reason, "reason")
        if (
            self.level_before,
            self.mastery_before,
            self.confidence_before,
        ) == (self.level_after, self.mastery_after, self.confidence_after):
            raise ContractError("capability delta must change something")


@dataclass(frozen=True, slots=True)
class PersonaDelta(DeltaRecord):
    """Explicit persona change; capability gain never creates this record."""

    actor_id: EntityId
    trait: str
    to_value: str
    rationale: str
    evidence_refs: tuple[str, ...] = ()
    from_value: str | None = None
    delta_id: str = ""
    provenance: EvolutionProvenance = field(
        default_factory=lambda: EvolutionProvenance(origin_ref="persona:legacy")
    )
    schema_version: int = EVOLUTION_DELTA_SCHEMA_VERSION
    version: int = 1
    kind: ClassVar[EvolutionDeltaKind] = "persona"

    def __post_init__(self) -> None:
        resolved_id = self.delta_id or f"persona_{self.actor_id.value}_{self.trait}_{self.to_value}"
        object.__setattr__(self, "delta_id", resolved_id)
        object.__setattr__(
            self,
            "provenance",
            EvolutionProvenance(
                origin_ref=(
                    f"persona:{resolved_id}"
                    if self.provenance.origin_ref == "persona:legacy"
                    else self.provenance.origin_ref
                ),
                source_refs=self.provenance.source_refs,
                event_refs=self.provenance.event_refs or self.evidence_refs,
                producer=self.provenance.producer,
            ),
        )
        common_checks(self.delta_id, self.schema_version, self.version, self.provenance)
        text(self.trait, "trait")
        text(self.to_value, "to_value")
        text(self.rationale, "rationale")
        refs(self.evidence_refs, "evidence_refs")
        if self.from_value == self.to_value:
            raise ContractError("persona delta must change the value")


@dataclass(frozen=True, slots=True)
class OrganizationDelta(DeltaRecord):
    """Explicit organization lifecycle or role change."""

    delta_id: str
    organization_id: EntityId
    lifecycle: OrganizationLifecycle
    actor_id: EntityId | None
    from_role: str | None
    to_role: str | None
    reason: str
    provenance: EvolutionProvenance
    schema_version: int = EVOLUTION_DELTA_SCHEMA_VERSION
    version: int = 1
    kind: ClassVar[EvolutionDeltaKind] = "organization"

    def __post_init__(self) -> None:
        common_checks(self.delta_id, self.schema_version, self.version, self.provenance)
        if self.lifecycle not in (
            "formed",
            "joined",
            "left",
            "role_changed",
            "permission_changed",
            "dissolved",
            "split",
        ):
            raise ContractError(f"invalid organization lifecycle {self.lifecycle!r}")
        text(self.reason, "reason")
        if self.lifecycle == "role_changed" and self.from_role == self.to_role:
            raise ContractError("organization role change must change the role")
        if (
            self.lifecycle
            in (
                "joined",
                "left",
                "role_changed",
                "permission_changed",
                "split",
            )
            and self.actor_id is None
        ):
            raise ContractError("organization membership lifecycle requires actor_id")


type EvolutionDelta = (
    StateDelta
    | BeliefDelta
    | RelationshipDelta
    | CapabilityEvolutionDelta
    | PersonaDelta
    | OrganizationDelta
)
