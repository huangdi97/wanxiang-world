"""G94E: structured institution candidates require an explicit review."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_substrate.evolution.institution_candidate import (
    create_institution_candidate,
    review_institution_candidate,
)
from wanxiang_substrate.evolution.norm_candidate_model import NormCandidate


def _norm() -> NormCandidate:
    return NormCandidate(
        candidate_id="norm_g94e",
        pattern_key="shared:gate-duty",
        detection_id="detection_g94e",
        scope="local",
        scope_ref="world:g94e",
        population_refs=("alice", "bob"),
        source_event_refs=("evt_g94e_1", "evt_g94e_2", "evt_g94e_3"),
        exception_event_refs=(),
        occurrence_count=3,
        observed_window_count=3,
        support_ratio=1.0,
        exception_rate=0.0,
        confidence=0.9,
        sanction_count=1,
        reward_count=1,
        outcome_correlation=1.0,
        created_at=300,
    )


@pytest.mark.unit
def test_institution_candidate_contains_structure_and_review_is_pure() -> None:
    candidate = create_institution_candidate(
        _norm(),
        candidate_id="institution_g94e_gate",
        role_refs=("role:watcher", "role:reviewer"),
        resource_refs=("resource:ledger",),
        process_refs=("process:gate-duty",),
    )
    assert candidate.rule == "shared:gate-duty"
    assert candidate.role_refs == ("role:reviewer", "role:watcher")
    assert candidate.resource_refs == ("resource:ledger",)
    assert candidate.process_refs == ("process:gate-duty",)
    assert candidate.evidence == ("evt_g94e_1", "evt_g94e_2", "evt_g94e_3")
    assert candidate.provenance_refs[0] == "detection_g94e"
    assert candidate.approved is False
    reviewed = review_institution_candidate(candidate, reviewer="reviewer", approved=True)
    assert reviewed.approved is True
    assert reviewed.reviewed_by == "reviewer"
    assert candidate.approved is False


@pytest.mark.unit
def test_institution_candidate_has_no_auto_commit_and_requires_structure_review() -> None:
    with pytest.raises(ContractError, match="requires unique role"):
        create_institution_candidate(
            _norm(),
            candidate_id="institution_incomplete",
            role_refs=(),
            resource_refs=("resource:ledger",),
            process_refs=("process:gate-duty",),
        )
    candidate = create_institution_candidate(
        _norm(),
        candidate_id="institution_review",
        role_refs=("role:watcher",),
        resource_refs=("resource:ledger",),
        process_refs=("process:gate-duty",),
    )
    with pytest.raises(PermissionDenied):
        review_institution_candidate(candidate, reviewer="manager", approved=True)
