"""Pure capability & learning value objects (G03G).

Capability is a separate concept from knowledge (epistemic) and persona:
a bounded measurement of what an actor can do, changed only by evidence-backed
CapabilityDeltas.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

CAPABILITY_MIN_LEVEL = 0
CAPABILITY_MAX_LEVEL = 10
MASTERY_MIN = 0.0
MASTERY_MAX = 1.0
CONFIDENCE_MIN = 0.0
CONFIDENCE_MAX = 1.0

SUPPORTED_ASSESSMENT_TYPES = ("practical", "theoretical", "performance")
ASSESSMENT_OUTCOMES = ("pass", "fail")


def validate_capability_name(name: str) -> None:
    if not name or len(name) > 64 or not all(c.isalnum() or c in "_-" for c in name):
        raise ContractError(f"invalid capability name: {name!r}")


@dataclass(frozen=True, slots=True)
class CapabilityState:
    """Bounded measurement of an actor capability, with evidence provenance."""

    actor_id: EntityId
    capability: str
    level: int
    mastery: float
    confidence: float
    evidence_refs: tuple[str, ...] = ()
    updated_revision: int = 0

    def __post_init__(self) -> None:
        validate_capability_name(self.capability)
        if not (CAPABILITY_MIN_LEVEL <= self.level <= CAPABILITY_MAX_LEVEL):
            raise ContractError(
                f"capability level {self.level} outside "
                f"[{CAPABILITY_MIN_LEVEL},{CAPABILITY_MAX_LEVEL}]"
            )
        if not (MASTERY_MIN <= self.mastery <= MASTERY_MAX):
            raise ContractError(f"mastery {self.mastery} outside [0,1]")
        if not (CONFIDENCE_MIN <= self.confidence <= CONFIDENCE_MAX):
            raise ContractError(f"confidence {self.confidence} outside [0,1]")


@dataclass(frozen=True, slots=True)
class PracticeRecord:
    record_id: EntityId
    actor_id: EntityId
    capability: str
    practice_count: int
    evidence_ref: str

    def __post_init__(self) -> None:
        validate_capability_name(self.capability)
        if self.practice_count <= 0:
            raise ContractError("practice_count must be positive")
        if not self.evidence_ref:
            raise ContractError("practice record requires an evidence ref")


@dataclass(frozen=True, slots=True)
class AssessmentEvidence:
    assessment_id: EntityId
    actor_id: EntityId
    capability: str
    assessment_type: str
    outcome: str
    evidence_ref: str

    def __post_init__(self) -> None:
        validate_capability_name(self.capability)
        if self.assessment_type not in SUPPORTED_ASSESSMENT_TYPES:
            raise ContractError(f"unsupported assessment type {self.assessment_type!r}")
        if self.outcome not in ASSESSMENT_OUTCOMES:
            raise ContractError(f"unsupported assessment outcome {self.outcome!r}")
        if not self.evidence_ref:
            raise ContractError("assessment requires an evidence ref")


@dataclass(frozen=True, slots=True)
class CapabilityDelta:
    """Evidence-backed bounded change to a capability."""

    actor_id: EntityId
    capability: str
    level_delta: int
    mastery_delta: float
    confidence_delta: float
    reason: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        validate_capability_name(self.capability)
        if not self.reason:
            raise ContractError("capability delta requires a reason")
        if self.level_delta == 0 and self.mastery_delta == 0.0 and self.confidence_delta == 0.0:
            raise ContractError("capability delta must change something")


@dataclass(frozen=True, slots=True)
class LearnerState:
    """Read-model aggregate of an actor's learning biography."""

    actor_id: EntityId
    capabilities: tuple[CapabilityState, ...]
    practice_records: int
    assessment_records: int
    biography: tuple[str, ...]

    def capability(self, name: str) -> CapabilityState | None:
        for state in self.capabilities:
            if state.capability == name:
                return state
        return None
