"""Learn / Challenge service (G18G).

Integrated world-based learning: challenge discovery via the Opportunity/
Challenge runtime, evidence-backed assessment producing capability deltas,
a longitudinal learning biography, and challenge actions routed through the
normal command path. Capability changes NEVER mutate persona.
"""

from __future__ import annotations

from typing import Any

from wanxiang_substrate.capability.model import (
    AssessmentEvidence,
    CapabilityState,
    LearnerState,
    PracticeRecord,
)
from wanxiang_substrate.capability.policy import LearningPolicy
from wanxiang_substrate.reality.challenge import ChallengeCompiler, Opportunity


class LearnService:
    def __init__(self, policy: LearningPolicy | None = None) -> None:
        self._policy = policy or LearningPolicy()
        self._compiler = ChallengeCompiler()

    def discover(self, world_state: dict[str, bool], at_ticks: int) -> tuple[Opportunity, ...]:
        return self._compiler.detect(world_state, at_ticks)

    def practice(self, learner: LearnerState, record: PracticeRecord) -> LearnerState:
        delta = self._policy.practice_delta(record)
        return self._apply(learner, delta, record.evidence_ref, kind="practice")

    def assess(self, learner: LearnerState, evidence: AssessmentEvidence) -> LearnerState:
        delta = self._policy.assessment_delta(evidence)
        return self._apply(learner, delta, evidence.evidence_ref, kind="assessment")

    def _apply(
        self,
        learner: LearnerState,
        delta: Any,
        evidence_ref: str,
        *,
        kind: str,
    ) -> LearnerState:
        existing = learner.capability(delta.capability)
        base_level = existing.level if existing else 0
        base_mastery = existing.mastery if existing else 0.0
        base_confidence = existing.confidence if existing else 0.0
        merged = CapabilityState(
            actor_id=learner.actor_id,
            capability=delta.capability,
            level=min(10, max(0, base_level + delta.level_delta)),
            mastery=min(1.0, max(0.0, base_mastery + delta.mastery_delta)),
            confidence=min(1.0, max(0.0, base_confidence + delta.confidence_delta)),
            evidence_refs=tuple(
                dict.fromkeys((existing.evidence_refs if existing else ()) + (evidence_ref,))
            ),
        )
        capabilities = tuple(
            merged if c.capability == delta.capability else c for c in learner.capabilities
        )
        if existing is None:
            capabilities = capabilities + (merged,)
        return LearnerState(
            actor_id=learner.actor_id,
            capabilities=capabilities,
            practice_records=learner.practice_records + (1 if kind == "practice" else 0),
            assessment_records=learner.assessment_records + (1 if kind == "assessment" else 0),
            biography=learner.biography + (f"capability:{delta.capability}=level{merged.level}",),
        )
