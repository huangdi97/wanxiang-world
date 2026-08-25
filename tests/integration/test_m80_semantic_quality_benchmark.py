"""M80 Gold Set protocol and semantic quality metrics."""

from __future__ import annotations

import pytest
from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.quality.semantic_benchmark import sample_candidates
from wanxiang_substrate.quality.semantic_metrics import evaluate_gold_set
from wanxiang_substrate.quality.semantic_models import GoldAssertion, GoldSet


def _candidate(
    candidate_id: str, kind: str, payload: dict[str, str], ref: str, confidence: float = 0.9
) -> CandidateEnvelope:
    return CandidateEnvelope(
        candidate_id=candidate_id,
        kind=kind,  # type: ignore[arg-type]
        origin_pass="m80_anonymized_fixture",
        payload=tuple(sorted(payload.items())),
        confidence=confidence,
        source_refs=(ref,),
        distiller_version=1,
    )


def _fixture() -> tuple[tuple[CandidateEnvelope, ...], GoldSet]:
    candidates = (
        _candidate("id_ada", "identity", {"key": "ada", "display_name": "Ada"}, "book#p/1"),
        _candidate("alias_ada", "alias", {"identity_key": "ada", "alias": "A"}, "book#p/2"),
        _candidate(
            "event_departure",
            "event",
            {"event_type": "departure", "date": "1980", "participants": "ada"},
            "book#p/3",
        ),
        _candidate(
            "event_return",
            "event",
            {"event_type": "return", "date": "1990", "participants": "ada"},
            "book#p/4",
        ),
        _candidate(
            "event_unknown",
            "event",
            {
                "event_type": "meeting",
                "date": "unknown",
                "uncertain": "true",
                "participants": "ada",
            },
            "book#p/5",
            0.45,
        ),
        _candidate(
            "relation_ada_bob",
            "relation",
            {"source_key": "ada", "target_key": "bob", "relation_type": "friend"},
            "book#p/6",
        ),
        _candidate("place_harbor", "place", {"name": "Harbor"}, "book#p/7"),
        _candidate("org_guild", "organization", {"name": "Guild"}, "book#p/8"),
        _candidate(
            "boundary_ada",
            "knowledge_boundary",
            {"subject_key": "ada", "boundary": "observed_only"},
            "book#p/9",
        ),
    )
    sampled, manifest = sample_candidates(candidates, sample_size=12, seed=83)
    assert {item.candidate_id for item in sampled} == {item.candidate_id for item in candidates}
    assertions = (
        GoldAssertion("id_ada", "identity", True, (("key", "ada"),), ("book#p/1",)),
        GoldAssertion(
            "alias_ada",
            "alias",
            True,
            (("alias", "A"),),
            ("book#p/2",),
            expected_merge_target="ada",
        ),
        GoldAssertion(
            "event_departure",
            "event",
            True,
            (("event_type", "departure"), ("date", "1980"), ("participants", "ada")),
            ("book#p/3",),
            expected_order=1,
        ),
        GoldAssertion(
            "event_return",
            "event",
            True,
            (("event_type", "return"), ("date", "1990"), ("participants", "ada")),
            ("book#p/4",),
            expected_order=2,
        ),
        GoldAssertion(
            "event_unknown",
            "event",
            True,
            (("event_type", "meeting"), ("date", "unknown")),
            ("book#p/5",),
            expected_uncertain=True,
        ),
        GoldAssertion(
            "relation_ada_bob",
            "relation",
            True,
            (("source_key", "ada"), ("target_key", "bob"), ("relation_type", "friend")),
            ("book#p/6",),
        ),
        GoldAssertion("place_harbor", "place", True, (("name", "Harbor"),), ("book#p/7",)),
        GoldAssertion("org_guild", "organization", True, (("name", "Guild"),), ("book#p/8",)),
        GoldAssertion(
            "boundary_ada",
            "knowledge_boundary",
            True,
            (("subject_key", "ada"), ("boundary", "observed_only")),
            ("book#p/9",),
        ),
    )
    return candidates, GoldSet("m80-v1", assertions, manifest)


@pytest.mark.integration
def test_gold_sampling_is_stratified_and_deterministic() -> None:
    candidates, gold = _fixture()
    _, repeat = sample_candidates(candidates, sample_size=12, seed=83)
    assert gold.sampling == repeat
    assert {name for name, _ids in gold.sampling.strata} >= {
        "random",
        "high_impact",
        "low_confidence",
        "conflict_merge",
    }


@pytest.mark.integration
def test_semantic_quality_report_measures_quality_not_candidate_count() -> None:
    candidates, gold = _fixture()
    report = evaluate_gold_set(candidates, gold)
    values = {item.name: item.value for item in report.metrics}
    assert report.passed is True
    assert values["identity_precision"] == 1.0
    assert values["alias_merge_precision"] == 1.0
    assert values["false_merge_rate"] == 0.0
    assert values["temporal_ordering"] == 1.0
    assert values["uncertainty_honesty"] == 1.0
    assert values["evidence_traceability"] == 1.0
