"""G35H: completion records with support refs / confidence / review (mechanism).

Synthetic completion records only - no real《红楼梦》canon content.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from wanxiang_substrate.ledger.completion import (
    CompletionDecision,
    CompletionRecord,
    CompletionReviewLedger,
    CompletionStudio,
    apply_batch_review,
)
from wanxiang_substrate.ledger.errors import InvalidPromotion, ReviewRequired


def _record(
    completion_id: str, description: str, support: tuple[str, ...], confidence: float
) -> CompletionRecord:
    return CompletionRecord(
        completion_id=completion_id,
        description=description,
        support_refs=support,
        confidence=confidence,
    )


def _approve(completion_id: str, decision_id: str = "d") -> CompletionDecision:
    return CompletionDecision(
        decision_id=decision_id,
        completion_id=completion_id,
        decision="approve",
        reviewer="human",
        rationale="evidence-backed completion",
        evidence_refs=("loc://chapter_2",),
    )


@pytest.mark.unit
def test_can_enter_canon_defaults_false_and_requires_evidence_review() -> None:
    ledger = CompletionReviewLedger()
    record = _record("c1", "潇湘馆内部庭院布局 (Completion)", ("loc://chapter_1",), 0.9)
    ledger.submit(record)
    assert record.can_enter_canon is False
    assert record.stage == "E0-E2"
    # Approval without evidence refs is refused.
    with pytest.raises(ReviewRequired):
        ledger.review(
            CompletionDecision(
                decision_id="d1",
                completion_id="c1",
                decision="approve",
                reviewer="human",
                rationale="no evidence",
                evidence_refs=(),
            )
        )
    # Approval with evidence + authorized reviewer lifts can_enter_canon.
    approved = ledger.review(_approve("c1", "d2"))
    assert approved.review_status == "approved"
    assert approved.stage == "E3"
    assert approved.can_enter_canon is True
    assert len(ledger.history("c1")) == 1


@pytest.mark.unit
def test_e4_rejected_never_auto_upgrades_to_e0() -> None:
    ledger = CompletionReviewLedger()
    ledger.submit(_record("c1", "a", ("loc://1",), 0.9))
    rejected = ledger.review(
        CompletionDecision(
            decision_id="d1",
            completion_id="c1",
            decision="reject",
            reviewer="human",
            rationale="unsupported",
        )
    )
    assert rejected.review_status == "rejected"
    assert rejected.stage == "E4"
    assert rejected.can_enter_canon is False
    # Terminal E4: no automatic or explicit re-review back to E0/E3.
    with pytest.raises(InvalidPromotion):
        ledger.review(_approve("c1", "d2"))
    with pytest.raises(InvalidPromotion):
        ledger.submit(_record("c1", "a", ("loc://1",), 0.9))  # id reuse refused


@pytest.mark.unit
def test_e5_superseded_never_auto_upgrades_to_e0() -> None:
    ledger = CompletionReviewLedger()
    ledger.submit(_record("c1", "a", ("loc://1",), 0.9))
    ledger.review(_approve("c1"))
    superseded = ledger.supersede(
        "c1", reviewer="human", rationale="superseded by newer source claim"
    )
    assert superseded.review_status == "superseded"
    assert superseded.stage == "E5"
    assert superseded.can_enter_canon is False
    with pytest.raises(InvalidPromotion):
        ledger.review(_approve("c1", "d2"))


@pytest.mark.unit
def test_conflicting_claims_preserved() -> None:
    ledger = CompletionReviewLedger()
    ledger.submit(_record("c1", "庭院布局 (Completion)", ("loc://chapter_1",), 0.8))
    ledger.submit(_record("c2", "庭院布局 (Completion)", ("loc://chapter_5",), 0.6))
    # Both conflicting claims coexist; neither overwrites the other.
    assert ledger.get("c1") is not None
    assert ledger.get("c2") is not None
    assert ledger.conflicts() == (("c1", "c2"),)
    assert len(ledger.all()) == 2


@pytest.mark.unit
def test_confidence_below_threshold_refuses_approval() -> None:
    ledger = CompletionReviewLedger()
    ledger.submit(_record("c1", "a", ("loc://1",), 0.5))
    with pytest.raises(ReviewRequired):
        ledger.review(_approve("c1"))


@pytest.mark.unit
def test_unauthorized_reviewer_rejected() -> None:
    ledger = CompletionReviewLedger()
    ledger.submit(_record("c1", "a", ("loc://1",), 0.9))
    with pytest.raises(ReviewRequired):
        ledger.review(
            CompletionDecision(
                decision_id="d1",
                completion_id="c1",
                decision="approve",
                reviewer="system",
                rationale="auto",
                evidence_refs=("loc://1",),
            )
        )


@pytest.mark.unit
def test_batch_review_cli_use_case(workspace_tmp_path: Path) -> None:
    tmp_path = workspace_tmp_path
    from scripts.completion_review import main

    manifest = {
        "records": [
            {
                "completion_id": "c1",
                "description": "布局 (Completion)",
                "support_refs": ["loc://1"],
                "confidence": 0.9,
            },
        ],
        "decisions": [
            {
                "decision_id": "d1",
                "completion_id": "c1",
                "decision": "approve",
                "reviewer": "human",
                "rationale": "ok",
                "evidence_refs": ["loc://1"],
            },
        ],
    }
    manifest_path = tmp_path / "manifest.json"
    report_path = tmp_path / "report.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    assert main([str(manifest_path), str(report_path)]) == 0
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["reviewed"] == ["c1"]
    assert report["can_enter_canon"] == ["c1"]
    assert report["stage_summary"]["approved"] == 1


@pytest.mark.unit
def test_studio_queries() -> None:
    ledger = CompletionReviewLedger()
    ledger.submit(_record("c1", "a", ("loc://1",), 0.9))
    ledger.submit(_record("c2", "b", ("loc://2",), 0.9))
    ledger.review(_approve("c1"))
    studio = CompletionStudio(ledger)
    assert {r.completion_id for r in studio.pending_review()} == {"c2"}
    assert {r.completion_id for r in studio.canon_candidates()} == {"c1"}
    assert studio.stage_summary() == {"pending": 1, "approved": 1, "rejected": 0, "superseded": 0}


@pytest.mark.unit
def test_apply_batch_review_order_is_deterministic() -> None:
    ledger = CompletionReviewLedger()
    ledger.submit(_record("c1", "a", ("loc://1",), 0.9))
    ledger.submit(_record("c2", "b", ("loc://2",), 0.9))
    decisions = (_approve("c1", "d1"), _approve("c2", "d2"))
    updated = apply_batch_review(ledger, decisions)
    assert [r.completion_id for r in updated] == ["c1", "c2"]
    assert all(r.can_enter_canon for r in updated)
