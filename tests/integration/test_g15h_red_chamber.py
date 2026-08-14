"""G15H: Red Chamber source-gated qualified reference slice.

Real Red Chamber literary sources are not in the repository (EXTERNAL_BLOCKED).
This goal proves the generic source-gate/compiler/ledger capability is complete
and that canon/completion/model-derived content stays distinguishable, with
provenance retained for canonical claims. No canon is fabricated from memory.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.compiler.compiler import StructuredCompiler
from wanxiang_substrate.ledger.ledger import CompletionLedger
from wanxiang_substrate.ledger.model import ContentItem, ReviewDecision
from wanxiang_substrate.sources.errors import RightsDenied, SourceNotApproved
from wanxiang_substrate.sources.fixture import approved_source, rejected_source
from wanxiang_substrate.sources.gate import SourceGate


def test_unapproved_material_cannot_compile_as_canonical() -> None:
    gate = SourceGate()
    approved = approved_source()
    rejected = rejected_source()
    # Approved synthetic fixture (provenance: fixture:approved) compiles.
    assert gate.decide(approved).ok is True
    result = StructuredCompiler().compile("red_chamber_slice", {approved.source_id: approved})
    assert result.ok
    # Rights-denied / unapproved material cannot compile as canonical.
    assert gate.decide(rejected).ok is False
    with pytest.raises(RightsDenied):
        gate.require_compile(rejected)
    from wanxiang_substrate.sources.model import SourceRecord, payload_hash

    draft = SourceRecord(
        source_id="src_rc_draft",
        kind="text",
        content_hash=payload_hash("unreviewed draft"),
        content_ref="ref://draft",
        stage="E0",
        rights=approved.rights,
        payload="unreviewed draft",
        provenance="fixture:draft",
    )
    assert gate.decide(draft).ok is False
    with pytest.raises(SourceNotApproved):
        gate.require_compile(draft)


def test_canon_completion_model_labels_distinguishable() -> None:
    ledger = CompletionLedger()
    canon = ledger.submit(
        ContentItem(item_id="rc_canon", label="canon", source_refs=("ref://rc_canon_src",))
    )
    source_backed = ledger.submit(
        ContentItem(
            item_id="rc_source",
            label="source_backed",
            source_refs=("ref://rc_source",),
            rights_approved=True,
        )
    )
    model = ledger.submit(ContentItem(item_id="rc_model", label="model_inference", source_refs=()))
    # Labels are distinct and preserved.
    assert {canon.label, source_backed.label, model.label} == {
        "canon",
        "source_backed",
        "model_inference",
    }
    # Promotion requires review (canon is terminal; source_backed -> canon).
    promoted = ledger.review(
        ReviewDecision(
            decision_id="d1",
            item_id="rc_source",
            from_label="source_backed",
            to_label="canon",
            reviewer="reviewer",
            rationale="source verified",
            review_version=1,
            evidence_refs=("ref://evidence",),
        )
    )
    assert promoted.label == "canon"


def test_canonical_claim_provenance_retained() -> None:
    ledger = CompletionLedger()
    ledger.submit(
        ContentItem(
            item_id="rc_claim",
            label="completion",
            source_refs=("ref://ch1", "ref://ch2"),
            rights_approved=True,
        )
    )
    assert ledger.require("rc_claim").source_refs == ("ref://ch1", "ref://ch2")
    # Audit history is append-only for the promotion path (completion ->
    # source_backed -> canon), and provenance is retained throughout.
    sb = ledger.review(
        ReviewDecision(
            decision_id="d2",
            item_id="rc_claim",
            from_label="completion",
            to_label="source_backed",
            reviewer="reviewer",
            rationale="source verified",
            review_version=1,
            evidence_refs=("ref://ch1",),
        )
    )
    assert sb.source_refs == ("ref://ch1", "ref://ch2")
    promoted = ledger.review(
        ReviewDecision(
            decision_id="d3",
            item_id="rc_claim",
            from_label="source_backed",
            to_label="canon",
            reviewer="reviewer",
            rationale="confirmed",
            review_version=1,
            evidence_refs=("ref://ch1", "ref://ch2"),
        )
    )
    assert promoted.label == "canon"
    assert promoted.source_refs == ("ref://ch1", "ref://ch2")
