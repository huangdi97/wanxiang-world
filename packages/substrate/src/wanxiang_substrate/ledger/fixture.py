"""Synthetic ledger fixtures: conflicts and revised decisions (G04D)."""

from __future__ import annotations

from wanxiang_substrate.ledger.model import ContentItem


def inference_item() -> ContentItem:
    return ContentItem(
        item_id="item_bridge_year",
        label="model_inference",
        source_refs=(),
        rationale="model guessed the year",
        rights_usage="canonical",
        rights_approved=True,
    )


def reviewed_source_item() -> ContentItem:
    return ContentItem(
        item_id="item_bridge_year",
        label="source_backed",
        source_refs=("src_bridge_a", "src_bridge_b"),
        evidence_refs=("evid://bridge_a", "evid://bridge_b"),
        rationale="two conflicting archive records",
        reviewer="reviewer-1",
        review_version=1,
        rights_usage="canonical",
        rights_approved=True,
    )


def canon_item() -> ContentItem:
    return ContentItem(
        item_id="item_bridge_year",
        label="canon",
        source_refs=("src_bridge_a",),
        evidence_refs=("evid://bridge_a",),
        rationale="approved by review",
        reviewer="reviewer-2",
        review_version=2,
        locked=True,
        rights_usage="canonical",
        rights_approved=True,
    )


def rights_denied_item() -> ContentItem:
    return ContentItem(
        item_id="item_private_letter",
        label="source_backed",
        source_refs=("src_private",),
        evidence_refs=("evid://private",),
        rationale="no redistribution rights",
        rights_usage="private",
        rights_approved=False,
    )
