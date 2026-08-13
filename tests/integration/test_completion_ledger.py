"""G04D: completion ledger & review workflow.

Covers the truth-label taxonomy, promotion rules, canon locks, immutable
history, rights gates and version diffs.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.ledger.errors import (
    CanonLocked,
    InvalidPromotion,
    ReviewRequired,
    RightsBlocked,
)
from wanxiang_substrate.ledger.fixture import (
    canon_item,
    inference_item,
    reviewed_source_item,
    rights_denied_item,
)
from wanxiang_substrate.ledger.ledger import CompletionLedger
from wanxiang_substrate.ledger.model import (
    ReviewDecision,
    TruthLabel,
    allowed_promotions,
    requires_review_for_canon,
)


def _decision(
    item_id: str,
    to_label: str,
    reviewer: str = "reviewer-1",
    rationale: str = "reviewed",
    evidence: tuple[str, ...] = ("evid://x",),
    override: bool = False,
) -> ReviewDecision:
    return ReviewDecision(
        decision_id=f"dec_{item_id}_{to_label}",
        item_id=item_id,
        from_label="completion",
        to_label=to_label,  # type: ignore[arg-type]
        reviewer=reviewer,
        rationale=rationale,
        review_version=1,
        evidence_refs=evidence,
        is_override=override,
    )


@pytest.mark.unit
def test_label_taxonomy_and_transition_rules() -> None:
    assert allowed_promotions("model_inference") == ("completion", "reconstruction")
    assert allowed_promotions("completion") == ("source_backed",)
    assert allowed_promotions("source_backed") == ("canon",)
    assert allowed_promotions("canon") == ()
    assert requires_review_for_canon("model_inference") is True
    assert requires_review_for_canon("source_backed") is False


@pytest.mark.unit
def test_model_inference_cannot_become_canon_without_review() -> None:
    ledger = CompletionLedger()
    ledger.submit(inference_item())
    with pytest.raises(InvalidPromotion):
        ledger.review(_decision("item_bridge_year", "canon", evidence=()))
    # Even with evidence, model inference cannot jump straight to canon.
    with pytest.raises(InvalidPromotion):
        ledger.review(_decision("item_bridge_year", "canon", evidence=("evid://x",)))


@pytest.mark.unit
def test_promotion_path_to_canon_requires_evidence() -> None:
    ledger = CompletionLedger()
    ledger.submit(inference_item())
    # inference -> completion -> source_backed -> canon
    ledger.review(_decision("item_bridge_year", "completion", evidence=("evid://m",)))
    ledger.review(_decision("item_bridge_year", "source_backed", evidence=("evid://s",)))
    with pytest.raises(ReviewRequired):
        ledger.review(_decision("item_bridge_year", "canon", evidence=()))
    canon = ledger.review(_decision("item_bridge_year", "canon", evidence=("evid://c",)))
    assert canon.label == "canon"
    assert canon.locked is True
    assert "evid://m" in canon.evidence_refs


@pytest.mark.unit
def test_canon_lock_requires_override() -> None:
    ledger = CompletionLedger()
    ledger.submit(canon_item())
    with pytest.raises(CanonLocked):
        ledger.review(_decision("item_bridge_year", "source_backed"))
    # Override decision (branch rule) changes it but preserves history.
    updated = ledger.review(
        _decision("item_bridge_year", "source_backed", override=True, reviewer="reviewer-3")
    )
    assert updated.label == "source_backed"
    history = ledger.history("item_bridge_year")
    assert len(history) == 1
    assert history[0].is_override is True


@pytest.mark.unit
def test_reversal_preserves_old_decision() -> None:
    ledger = CompletionLedger()
    ledger.submit(reviewed_source_item())
    first = ledger.review(_decision("item_bridge_year", "canon", evidence=("evid://c",)))
    assert first.label == "canon"
    # Reverse back to source_backed via override; both decisions retained.
    ledger.review(
        _decision("item_bridge_year", "source_backed", override=True, reviewer="reviewer-9")
    )
    history = ledger.history("item_bridge_year")
    assert len(history) == 2
    assert history[0].to_label == "canon"
    assert history[1].to_label == "source_backed"


@pytest.mark.unit
def test_review_cannot_approve_disallowed_redistribution() -> None:
    ledger = CompletionLedger()
    ledger.submit(rights_denied_item())
    with pytest.raises(RightsBlocked):
        ledger.review(_decision("item_private_letter", "canon"))


@pytest.mark.unit
def test_every_item_exposes_truth_label() -> None:
    ledger = CompletionLedger()
    ledger.submit(inference_item())
    ledger.submit(reviewed_source_item())
    snapshot = ledger.snapshot_labels()
    assert snapshot["item_bridge_year"] == "source_backed"
    for label in snapshot.values():
        assert label in (
            "canon",
            "source_backed",
            "completion",
            "model_inference",
            "reconstruction",
            "user_fiction",
        )


@pytest.mark.unit
def test_diff_between_package_versions() -> None:
    ledger = CompletionLedger()
    before: dict[str, TruthLabel] = {
        "a": "completion",
        "b": "source_backed",
        "c": "canon",
    }
    after: dict[str, TruthLabel] = {
        "a": "source_backed",
        "c": "canon",
        "d": "model_inference",
    }
    diff = ledger.diff(before, after)
    assert diff.added == ("d",)
    assert diff.removed == ("b",)
    assert diff.label_changed == (("a", "completion", "source_backed"),)
    assert diff.empty is False


@pytest.mark.unit
def test_audit_exposes_reviewer_and_rationale() -> None:
    ledger = CompletionLedger()
    ledger.submit(inference_item())
    ledger.review(
        _decision("item_bridge_year", "completion", reviewer="alice", rationale="checked")
    )
    item = ledger.require("item_bridge_year")
    assert item.reviewer == "alice"
    assert item.rationale == "checked"
    assert item.review_version == 1
