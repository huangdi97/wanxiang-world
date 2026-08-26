"""G94F: shared culture/ontology candidates need strict long-window evidence."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_domain.constitution import ROOT_CONSTITUTION, legacy_default_constitution
from wanxiang_domain.errors import ContractError, PermissionDenied
from wanxiang_substrate.evolution.norm_candidate_model import NormCandidate
from wanxiang_substrate.evolution.ontology_candidate import (
    OntologyCandidatePolicy,
    create_ontology_candidate,
    review_ontology_candidate,
)
from wanxiang_substrate.evolution.ontology_law import OntologyCandidate, OntologyLawEvolution


def _norm(index: int, *, support: float = 0.95) -> NormCandidate:
    return NormCandidate(
        candidate_id=f"norm_g94f_{index}",
        pattern_key="shared:gate-duty",
        detection_id=f"detection_g94f_{index}",
        scope="local",
        scope_ref="world:g94f",
        population_refs=("alice", "bob", "carol"),
        source_event_refs=(f"evt_g94f_{index}_1", f"evt_g94f_{index}_2"),
        exception_event_refs=(),
        occurrence_count=4,
        observed_window_count=2,
        support_ratio=support,
        exception_rate=0.05,
        confidence=0.95,
        sanction_count=1,
        reward_count=1,
        outcome_correlation=0.9,
        created_at=index * 100,
    )


def _candidate() -> tuple[OntologyCandidate, tuple[NormCandidate, ...]]:
    norms = (_norm(1), _norm(2), _norm(3))
    return (
        create_ontology_candidate(
            norms,
            candidate_id="ontology_g94f_duty",
            concept="shared:gate-duty",
            evidence_windows=((0, 100), (101, 200), (201, 300)),
        ),
        norms,
    )


@pytest.mark.unit
def test_ontology_candidate_requires_strict_cross_window_evidence_and_review() -> None:
    candidate, norms = _candidate()
    assert candidate.stability == pytest.approx(0.95)
    assert candidate.complexity == pytest.approx(1 / 3)
    assert candidate.interpretability == pytest.approx(1.0)
    assert candidate.norm_refs == tuple(norm.candidate_id for norm in norms)
    assert all(norm.detection_id in candidate.provenance_refs for norm in norms)
    assert candidate.evidence_windows == ((0, 100), (101, 200), (201, 300))
    assert candidate.approved is False
    with pytest.raises(PermissionDenied, match="requires explicit review"):
        OntologyLawEvolution.validate_ontology(candidate, legacy_default_constitution())

    reviewed = review_ontology_candidate(candidate, reviewer="reviewer", approved=True)
    assert reviewed.approved is True
    assert reviewed.reviewed_by == "reviewer"
    assert OntologyLawEvolution.validate_ontology(reviewed, legacy_default_constitution()) is True
    with pytest.raises(PermissionDenied, match="immutable layer"):
        OntologyLawEvolution.validate_ontology(reviewed, ROOT_CONSTITUTION)
    assert candidate.approved is False


@pytest.mark.unit
def test_ontology_candidate_rejects_weak_or_non_cross_window_evidence() -> None:
    with pytest.raises(ContractError, match="distinct windows"):
        create_ontology_candidate(
            (_norm(1), _norm(2), _norm(3)),
            candidate_id="ontology_g94f_short",
            concept="shared:gate-duty",
            evidence_windows=((0, 100), (101, 300)),
        )
    weak = (_norm(1), _norm(2), replace(_norm(3), support_ratio=0.8))
    with pytest.raises(ContractError, match="strict threshold"):
        create_ontology_candidate(
            weak,
            candidate_id="ontology_g94f_weak",
            concept="shared:gate-duty",
            evidence_windows=((0, 100), (101, 200), (201, 300)),
        )
    with pytest.raises(PermissionDenied, match="not authorized"):
        review_ontology_candidate(_candidate()[0], reviewer="manager", approved=True)


@pytest.mark.unit
def test_ontology_policy_defaults_are_high_and_serializable() -> None:
    policy = OntologyCandidatePolicy()
    assert policy.minimum_norm_candidates == 3
    assert policy.minimum_cross_windows == 3
    assert policy.minimum_support >= 0.9
    assert policy.minimum_confidence >= 0.9
    assert policy.maximum_exception_rate <= 0.1
