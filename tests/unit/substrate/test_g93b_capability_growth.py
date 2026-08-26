"""G93B: evidence-bound capability candidates and promotion proposals."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.capability.errors import CapabilityPrerequisiteError
from wanxiang_substrate.capability.model import (
    AssessmentEvidence,
    CapabilityState,
    PracticeRecord,
)
from wanxiang_substrate.evolution.capability_growth import (
    CapabilityCandidate,
    CapabilityPrerequisite,
    create_capability_candidate,
    promote_capability_candidate,
    validate_capability_candidate,
)
from wanxiang_substrate.evolution.delta import EvolutionProvenance

ACTOR = EntityId("actor_growth")
PROVENANCE = EvolutionProvenance(
    origin_ref="run:g93b",
    source_refs=("source:g93b",),
    event_refs=("event:g93b:1",),
    producer="runtime_projection",
)


def _practice(count: int = 1) -> tuple[PracticeRecord, ...]:
    return tuple(
        PracticeRecord(
            record_id=EntityId(f"practice_g93b_{index}"),
            actor_id=ACTOR,
            capability="watchkeeping",
            practice_count=count,
            evidence_ref=f"practice-event:{index}",
        )
        for index in range(1, 4)
    )


def _assessments(*outcomes: str) -> tuple[AssessmentEvidence, ...]:
    return tuple(
        AssessmentEvidence(
            assessment_id=EntityId(f"assessment_g93b_{index}"),
            actor_id=ACTOR,
            capability="watchkeeping",
            assessment_type="practical",
            outcome=outcome,
            evidence_ref=f"assessment-event:{index}",
        )
        for index, outcome in enumerate(outcomes, start=1)
    )


def _candidate(
    *,
    assessments: tuple[AssessmentEvidence, ...] = (),
    composed_from: tuple[str, ...] = ("navigation",),
) -> CapabilityCandidate:
    return create_capability_candidate(
        candidate_id="candidate_watchkeeping",
        actor_id=ACTOR,
        capability="watchkeeping",
        domain_ref="domain:gate",
        domain_capabilities=("navigation", "watchkeeping"),
        current_capabilities=(CapabilityState(ACTOR, "navigation", 1, 0.4, 0.8),),
        practice_records=_practice(),
        assessments=assessments,
        provenance=PROVENANCE,
        prerequisites=(CapabilityPrerequisite("navigation", minimum_level=1),),
        composed_from=composed_from,
    )


def test_practice_and_successful_assessment_create_promotable_candidate() -> None:
    candidate = _candidate(assessments=_assessments("pass", "fail"))
    validation = validate_capability_candidate(candidate)
    assert validation.valid is True
    assert validation.success_rate == 0.5
    promotion = promote_capability_candidate(candidate, validation)
    assert promotion.evolution_delta.kind == "capability"
    assert promotion.runtime_delta.level_delta == 1
    assert promotion.action_payload()["capability"] == "watchkeeping"
    assert "assessment-event:1" in promotion.runtime_delta.evidence_refs


def test_impossible_capability_without_domain_support_is_rejected() -> None:
    with pytest.raises(CapabilityPrerequisiteError, match="not supported"):
        create_capability_candidate(
            candidate_id="candidate_impossible",
            actor_id=ACTOR,
            capability="teleportation",
            domain_ref="domain:gate",
            domain_capabilities=("navigation", "watchkeeping"),
            current_capabilities=(),
            practice_records=(),
            assessments=(),
            provenance=PROVENANCE,
        )


def test_missing_prerequisite_or_composition_is_rejected() -> None:
    with pytest.raises(CapabilityPrerequisiteError, match="lacks prerequisite"):
        create_capability_candidate(
            candidate_id="candidate_missing_prereq",
            actor_id=ACTOR,
            capability="watchkeeping",
            domain_ref="domain:gate",
            domain_capabilities=("navigation", "watchkeeping"),
            current_capabilities=(),
            practice_records=_practice(),
            assessments=_assessments("pass"),
            provenance=PROVENANCE,
            prerequisites=(CapabilityPrerequisite("navigation", minimum_level=1),),
        )
    with pytest.raises(CapabilityPrerequisiteError, match="composition"):
        _candidate(composed_from=("navigation", "missing_skill"))


def test_failure_dominant_candidate_is_not_silently_promoted() -> None:
    candidate = _candidate(assessments=_assessments("fail", "fail", "pass"))
    validation = validate_capability_candidate(candidate)
    assert validation.valid is False
    assert "failures_exceed_successes" in validation.reasons
    with pytest.raises(CapabilityPrerequisiteError, match="not promotable"):
        promote_capability_candidate(candidate, validation)


def test_candidate_rejects_same_validation_identity() -> None:
    candidate = _candidate(assessments=_assessments("pass"))
    validation = validate_capability_candidate(candidate)
    with pytest.raises(ContractError, match="does not match"):
        promote_capability_candidate(
            candidate,
            validation.__class__("other", validation.valid, validation.success_rate, (), ()),
        )
