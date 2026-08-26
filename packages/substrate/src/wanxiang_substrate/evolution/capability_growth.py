"""Evidence-bound capability growth from practice, outcomes, and composition."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.capability.errors import CapabilityPrerequisiteError, EvidenceRequired
from wanxiang_substrate.capability.model import (
    AssessmentEvidence,
    CapabilityDelta,
    CapabilityState,
    PracticeRecord,
    validate_capability_name,
)
from wanxiang_substrate.capability.policy import (
    CONFIDENCE_GAIN_PER_PRACTICE,
    MASTERY_GAIN_PER_PRACTICE,
    PRACTICE_PER_LEVEL,
    LearningPolicy,
)
from wanxiang_substrate.evolution.delta import (
    CapabilityEvolutionDelta,
    EvolutionProvenance,
)

CandidateStatus = Literal["proposed", "validated", "rejected", "promoted"]
_apply_learning = LearningPolicy.apply


@dataclass(frozen=True, slots=True)
class CapabilityPrerequisite:
    """A domain-supported capability required before growth can be proposed."""

    capability: str
    minimum_level: int = 1

    def __post_init__(self) -> None:
        validate_capability_name(self.capability)
        if type(self.minimum_level) is not int or not 0 <= self.minimum_level <= 10:
            raise ContractError("capability prerequisite level must be in [0, 10]")


@dataclass(frozen=True, slots=True)
class CapabilityCandidate:
    """A typed, actor-local growth candidate; it is not an actor skill yet."""

    candidate_id: str
    actor_id: EntityId
    capability: str
    domain_ref: str
    practice_refs: tuple[str, ...]
    assessment_refs: tuple[str, ...]
    composition_refs: tuple[str, ...]
    practice_count: int
    success_count: int
    failure_count: int
    current_level: int
    proposed_level: int
    current_mastery: float
    proposed_mastery: float
    current_confidence: float
    proposed_confidence: float
    provenance: EvolutionProvenance
    status: CandidateStatus = "proposed"

    def __post_init__(self) -> None:
        if not self.candidate_id.strip() or not self.domain_ref.strip():
            raise ContractError("capability candidate requires id and domain ref")
        validate_capability_name(self.capability)
        for field_name, value in (
            ("practice_count", self.practice_count),
            ("success_count", self.success_count),
            ("failure_count", self.failure_count),
        ):
            if type(value) is not int or value < 0:
                raise ContractError(f"{field_name} must be non-negative")
        if self.success_count + self.failure_count > len(self.assessment_refs):
            raise ContractError("assessment outcome counts exceed assessment evidence")
        for field_name, value in (
            ("current_mastery", self.current_mastery),
            ("proposed_mastery", self.proposed_mastery),
            ("current_confidence", self.current_confidence),
            ("proposed_confidence", self.proposed_confidence),
        ):
            if not 0.0 <= value <= 1.0:
                raise ContractError(f"{field_name} must be within [0, 1]")
        if not 0 <= self.current_level <= 10 or not 0 <= self.proposed_level <= 10:
            raise ContractError("capability candidate levels must be in [0, 10]")
        if self.status not in ("proposed", "validated", "rejected", "promoted"):
            raise ContractError(f"invalid capability candidate status {self.status!r}")

    @property
    def evidence_refs(self) -> tuple[str, ...]:
        return tuple(sorted(set(self.practice_refs + self.assessment_refs)))


@dataclass(frozen=True, slots=True)
class CapabilityValidation:
    """Deterministic validation result retained beside the candidate."""

    candidate_id: str
    valid: bool
    success_rate: float
    reasons: tuple[str, ...]
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.candidate_id.strip() or not 0.0 <= self.success_rate <= 1.0:
            raise ContractError("invalid capability validation result")


@dataclass(frozen=True, slots=True)
class CapabilityPromotionProposal:
    """Proposal that can be submitted through the existing capability resolver."""

    candidate: CapabilityCandidate
    validation: CapabilityValidation
    evolution_delta: CapabilityEvolutionDelta
    runtime_delta: CapabilityDelta

    def action_payload(self) -> dict[str, object]:
        """Return typed resolver input; this method does not submit or commit it."""
        return {
            "actor_id": self.runtime_delta.actor_id.value,
            "capability": self.runtime_delta.capability,
            "level_delta": self.runtime_delta.level_delta,
            "mastery_delta": self.runtime_delta.mastery_delta,
            "confidence_delta": self.runtime_delta.confidence_delta,
            "reason": self.runtime_delta.reason,
            "evidence_refs": json.dumps(list(self.runtime_delta.evidence_refs), sort_keys=True),
        }


def create_capability_candidate(
    *,
    candidate_id: str,
    actor_id: EntityId,
    capability: str,
    domain_ref: str,
    domain_capabilities: tuple[str, ...],
    current_capabilities: tuple[CapabilityState, ...],
    practice_records: tuple[PracticeRecord, ...],
    assessments: tuple[AssessmentEvidence, ...],
    provenance: EvolutionProvenance,
    prerequisites: tuple[CapabilityPrerequisite, ...] = (),
    composed_from: tuple[str, ...] = (),
) -> CapabilityCandidate:
    """Build a candidate only when the target and its prerequisites are domain-supported."""
    validate_capability_name(capability)
    supported = set(domain_capabilities)
    if capability not in supported:
        raise CapabilityPrerequisiteError(
            f"capability {capability!r} is not supported by domain {domain_ref!r}"
        )
    current = {item.capability: item for item in current_capabilities if item.actor_id == actor_id}
    for prerequisite in prerequisites:
        if prerequisite.capability not in supported:
            raise CapabilityPrerequisiteError(
                f"prerequisite {prerequisite.capability!r} is outside domain support"
            )
        state = current.get(prerequisite.capability)
        if state is None or state.level < prerequisite.minimum_level:
            raise CapabilityPrerequisiteError(
                f"actor lacks prerequisite {prerequisite.capability!r} at "
                f"level {prerequisite.minimum_level}"
            )
    for name in composed_from:
        validate_capability_name(name)
        if name not in supported or name not in current:
            raise CapabilityPrerequisiteError(f"composition capability {name!r} is unavailable")
    matching_practice = tuple(
        item
        for item in practice_records
        if item.actor_id == actor_id and item.capability == capability
    )
    matching_assessments = tuple(
        item
        for item in assessments
        if item.actor_id == actor_id and item.capability == capability
    )
    if not matching_practice and not composed_from:
        raise EvidenceRequired("capability candidate requires practice or composition evidence")
    projected = current.get(capability)
    if matching_practice:
        practice_count = sum(item.practice_count for item in matching_practice)
        projected = _apply_learning(
            CapabilityDelta(
                actor_id=actor_id,
                capability=capability,
                level_delta=practice_count // PRACTICE_PER_LEVEL,
                mastery_delta=round(MASTERY_GAIN_PER_PRACTICE * practice_count, 6),
                confidence_delta=round(CONFIDENCE_GAIN_PER_PRACTICE * practice_count, 6),
                reason=f"practice:{candidate_id}",
                evidence_refs=tuple(item.evidence_ref for item in matching_practice),
            ),
            projected,
        )
    for evidence in sorted(matching_assessments, key=lambda item: item.assessment_id.value):
        projected = _apply_learning(LearningPolicy.assessment_delta(evidence), projected)
    if projected is None:
        raise ContractError("capability projection could not be computed")
    baseline = current.get(capability)
    return CapabilityCandidate(
        candidate_id=candidate_id,
        actor_id=actor_id,
        capability=capability,
        domain_ref=domain_ref,
        practice_refs=tuple(sorted(item.evidence_ref for item in matching_practice)),
        assessment_refs=tuple(sorted(item.evidence_ref for item in matching_assessments)),
        composition_refs=tuple(sorted(composed_from)),
        practice_count=sum(item.practice_count for item in matching_practice),
        success_count=sum(item.outcome == "pass" for item in matching_assessments),
        failure_count=sum(item.outcome == "fail" for item in matching_assessments),
        current_level=baseline.level if baseline else 0,
        proposed_level=projected.level,
        current_mastery=baseline.mastery if baseline else 0.0,
        proposed_mastery=projected.mastery,
        current_confidence=baseline.confidence if baseline else 0.0,
        proposed_confidence=projected.confidence,
        provenance=provenance,
    )


def validate_capability_candidate(candidate: CapabilityCandidate) -> CapabilityValidation:
    """Require repeated practice and at least one successful validation outcome."""
    reasons: list[str] = []
    if candidate.practice_count < 3:
        reasons.append("practice_count_below_validation_floor")
    if not candidate.assessment_refs:
        reasons.append("assessment_evidence_missing")
    if candidate.success_count == 0:
        reasons.append("successful_assessment_missing")
    if candidate.failure_count > candidate.success_count:
        reasons.append("failures_exceed_successes")
    total = candidate.success_count + candidate.failure_count
    success_rate = candidate.success_count / total if total else 0.0
    return CapabilityValidation(
        candidate_id=candidate.candidate_id,
        valid=not reasons,
        success_rate=round(success_rate, 6),
        reasons=tuple(reasons),
        evidence_refs=candidate.evidence_refs,
    )


def promote_capability_candidate(
    candidate: CapabilityCandidate,
    validation: CapabilityValidation,
) -> CapabilityPromotionProposal:
    """Create a proposal for the existing actor-skill resolver after validation."""
    if validation.candidate_id != candidate.candidate_id:
        raise ContractError("capability validation does not match candidate")
    if not validation.valid:
        raise CapabilityPrerequisiteError(
            f"capability candidate is not promotable: {', '.join(validation.reasons)}"
        )
    evolution_delta = CapabilityEvolutionDelta(
        delta_id=f"growth_{candidate.candidate_id}",
        actor_id=candidate.actor_id,
        capability=candidate.capability,
        level_before=candidate.current_level,
        level_after=candidate.proposed_level,
        mastery_before=candidate.current_mastery,
        mastery_after=candidate.proposed_mastery,
        confidence_before=candidate.current_confidence,
        confidence_after=candidate.proposed_confidence,
        reason=f"validated:{candidate.candidate_id}",
        provenance=candidate.provenance,
    )
    runtime_delta = CapabilityDelta(
        actor_id=candidate.actor_id,
        capability=candidate.capability,
        level_delta=candidate.proposed_level - candidate.current_level,
        mastery_delta=round(candidate.proposed_mastery - candidate.current_mastery, 6),
        confidence_delta=round(candidate.proposed_confidence - candidate.current_confidence, 6),
        reason=f"promotion:{candidate.candidate_id}",
        evidence_refs=candidate.evidence_refs,
    )
    return CapabilityPromotionProposal(candidate, validation, evolution_delta, runtime_delta)
