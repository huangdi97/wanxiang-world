"""Deterministic reference capability learning policy (G03G).

Pure functions: practice/assessment evidence maps to a bounded CapabilityDelta;
`apply` clamps the result to the declared scale. No LLM, no randomness, no I/O.
"""

from __future__ import annotations

from wanxiang_substrate.capability.model import (
    CAPABILITY_MAX_LEVEL,
    CONFIDENCE_MAX,
    CONFIDENCE_MIN,
    MASTERY_MAX,
    MASTERY_MIN,
    AssessmentEvidence,
    CapabilityDelta,
    CapabilityState,
    PracticeRecord,
)

PRACTICE_PER_LEVEL = 3
MASTERY_GAIN_PER_PRACTICE = 0.05
CONFIDENCE_GAIN_PER_PRACTICE = 0.02
MASTERY_GAIN_PASS = 0.15
CONFIDENCE_GAIN_PASS = 0.10
MASTERY_REGRESS_FAIL = 0.10
CONFIDENCE_REGRESS_FAIL = 0.05


class LearningPolicy:
    """Bounded, deterministic updates from practice/assessment evidence."""

    @staticmethod
    def practice_delta(record: PracticeRecord) -> CapabilityDelta:
        return CapabilityDelta(
            actor_id=record.actor_id,
            capability=record.capability,
            level_delta=record.practice_count // PRACTICE_PER_LEVEL,
            mastery_delta=round(MASTERY_GAIN_PER_PRACTICE * record.practice_count, 6),
            confidence_delta=round(CONFIDENCE_GAIN_PER_PRACTICE * record.practice_count, 6),
            reason=f"practice:{record.record_id.value}",
            evidence_refs=(record.evidence_ref,),
        )

    @staticmethod
    def assessment_delta(evidence: AssessmentEvidence) -> CapabilityDelta:
        if evidence.outcome == "pass":
            mastery_delta = MASTERY_GAIN_PASS
            confidence_delta = CONFIDENCE_GAIN_PASS
        else:
            mastery_delta = -MASTERY_REGRESS_FAIL
            confidence_delta = -CONFIDENCE_REGRESS_FAIL
        return CapabilityDelta(
            actor_id=evidence.actor_id,
            capability=evidence.capability,
            level_delta=0,
            mastery_delta=mastery_delta,
            confidence_delta=confidence_delta,
            reason=f"assessment:{evidence.assessment_id.value}",
            evidence_refs=(evidence.evidence_ref,),
        )

    @staticmethod
    def apply(delta: CapabilityDelta, current: CapabilityState | None) -> CapabilityState:
        """Clamp the update to the bounded scale and merge evidence provenance."""
        base_level = current.level if current is not None else 0
        base_mastery = current.mastery if current is not None else 0.0
        base_confidence = current.confidence if current is not None else 0.0
        base_revision = current.updated_revision if current is not None else 0
        evidence: set[str] = set(current.evidence_refs) if current is not None else set()
        evidence.update(delta.evidence_refs)
        return CapabilityState(
            actor_id=delta.actor_id,
            capability=delta.capability,
            level=max(0, min(CAPABILITY_MAX_LEVEL, base_level + delta.level_delta)),
            mastery=round(
                max(MASTERY_MIN, min(MASTERY_MAX, base_mastery + delta.mastery_delta)), 6
            ),
            confidence=round(
                max(CONFIDENCE_MIN, min(CONFIDENCE_MAX, base_confidence + delta.confidence_delta)),
                6,
            ),
            evidence_refs=tuple(sorted(evidence)),
            updated_revision=base_revision + 1,
        )
