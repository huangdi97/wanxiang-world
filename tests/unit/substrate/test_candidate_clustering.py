"""G57H: Candidate clustering — merge/split suggestions, reversible decisions."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.candidates.cluster import (
    CandidateClusterer,
    ClusterDecision,
    ClusterSuggestion,
)
from wanxiang_substrate.candidates.envelope import CandidateEnvelope


def _candidate(cid: str, key: str, *, name: str = "") -> CandidateEnvelope:
    payload: list[tuple[str, str]] = [("identity_key", key)]
    if name:
        payload.append(("display_name", name))
    return CandidateEnvelope(
        candidate_id=cid,
        kind="identity",
        origin_pass="identity",
        payload=tuple(payload),
        confidence=0.8,
        source_refs=(f"ref://{cid}",),
        distiller_version=1,
    )


@pytest.mark.unit
def test_suggestion_validation() -> None:
    with pytest.raises(ContractError):
        ClusterSuggestion(suggestion_id="", kind="merge", candidate_ids=("a", "b"), basis="x")
    with pytest.raises(ContractError):
        ClusterSuggestion(suggestion_id="s", kind="merge", candidate_ids=("a",), basis="x")


@pytest.mark.unit
def test_merge_suggestions_for_shared_key() -> None:
    candidates = (
        _candidate("c1", "alice|zhang"),
        _candidate("c2", "alice|zhang"),
        _candidate("c3", "bob|li"),
    )
    suggestions = CandidateClusterer().suggest_merges(candidates)
    assert len(suggestions) == 1
    assert suggestions[0].kind == "merge"
    assert set(suggestions[0].candidate_ids) == {"c1", "c2"}
    assert suggestions[0].reversible is True


@pytest.mark.unit
def test_split_suggestions_for_conflicting_name() -> None:
    candidate = _candidate("c1", "x", name="Alice|Alicia")
    suggestions = CandidateClusterer().suggest_splits((candidate,))
    assert any(s.kind == "split" for s in suggestions)


@pytest.mark.unit
def test_decisions_are_reversible() -> None:
    clusterer = CandidateClusterer()
    decision = ClusterDecision(
        decision_id="d1", suggestion_id="s1", decision="approve", reviewer="human", rationale="ok"
    )
    clusterer.decide(decision)
    assert clusterer.decision_for("s1") == decision
    reversal = ClusterDecision(
        decision_id="d2", suggestion_id="s1", decision="reject", reviewer="human", rationale="undo"
    )
    clusterer.decide(reversal)
    assert clusterer.decision_for("s1") == reversal


@pytest.mark.unit
def test_no_merge_suggestion_without_shared_key() -> None:
    candidates = (_candidate("c1", "a"), _candidate("c2", "b"))
    assert CandidateClusterer().suggest_merges(candidates) == ()
