"""Completion ledger & review workflow (G04D).

Canon is earned: model inference and user fiction can never jump straight to
canon; every promotion is an immutable decision with reviewer + rationale;
canon items are locked and only an explicit override (on a branch) may change
them without erasing history.
"""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_substrate.ledger.errors import (
    CanonLocked,
    InvalidPromotion,
    ItemNotFound,
    ReviewRequired,
    RightsBlocked,
)
from wanxiang_substrate.ledger.model import (
    ContentItem,
    ItemDiff,
    ReviewDecision,
    TruthLabel,
    allowed_promotions,
    requires_review_for_canon,
)


class CompletionLedger:
    """In-memory ledger with append-only decision history per item."""

    def __init__(self) -> None:
        self._items: dict[str, ContentItem] = {}
        self._history: dict[str, tuple[ReviewDecision, ...]] = {}

    def submit(self, item: ContentItem) -> ContentItem:
        self._items[item.item_id] = item
        self._history.setdefault(item.item_id, ())
        return item

    def get(self, item_id: str) -> ContentItem | None:
        return self._items.get(item_id)

    def require(self, item_id: str) -> ContentItem:
        item = self.get(item_id)
        if item is None:
            raise ItemNotFound(f"ledger item {item_id!r} not found")
        return item

    def review(self, decision: ReviewDecision) -> ContentItem:
        item = self.require(decision.item_id)
        if item.label == decision.to_label:
            raise InvalidPromotion(f"item {item.item_id!r} already labeled {decision.to_label}")
        if item.locked and not decision.is_override:
            raise CanonLocked(f"item {item.item_id!r} is canon-locked; override required")
        if not item.rights_approved:
            raise RightsBlocked(f"item {item.item_id!r} has no approved rights")
        if decision.to_label not in allowed_promotions(item.label) and not decision.is_override:
            raise InvalidPromotion(
                f"cannot promote {item.label!r} directly to {decision.to_label!r}"
            )
        if decision.to_label == "canon":
            if requires_review_for_canon(item.label) and not decision.evidence_refs:
                raise ReviewRequired(
                    f"canon promotion of {item.label!r} requires evidence and review"
                )
            if not decision.evidence_refs:
                raise ReviewRequired("canon promotion requires evidence refs")
        updated = ContentItem(
            item_id=item.item_id,
            label=decision.to_label,
            source_refs=item.source_refs,
            evidence_refs=tuple(sorted(set(item.evidence_refs) | set(decision.evidence_refs))),
            rationale=decision.rationale,
            reviewer=decision.reviewer,
            review_version=decision.review_version,
            locked=item.locked or decision.to_label == "canon",
            rights_usage=item.rights_usage,
            rights_approved=item.rights_approved,
        )
        self._items[item.item_id] = updated
        self._history[item.item_id] = self._history[item.item_id] + (decision,)
        return updated

    def history(self, item_id: str) -> tuple[ReviewDecision, ...]:
        self.require(item_id)
        return self._history.get(item_id, ())

    def lock(self, item_id: str) -> ContentItem:
        item = self.require(item_id)
        if item.label != "canon":
            raise InvalidPromotion(f"only canon items can be locked ({item.item_id!r})")
        updated = ContentItem(
            item_id=item.item_id,
            label=item.label,
            source_refs=item.source_refs,
            evidence_refs=item.evidence_refs,
            rationale=item.rationale,
            reviewer=item.reviewer,
            review_version=item.review_version,
            locked=True,
            rights_usage=item.rights_usage,
            rights_approved=item.rights_approved,
        )
        self._items[item.item_id] = updated
        return updated

    def diff(
        self,
        before: Mapping[str, TruthLabel],
        after: Mapping[str, TruthLabel],
    ) -> ItemDiff:
        added = tuple(sorted(set(after) - set(before)))
        removed = tuple(sorted(set(before) - set(after)))
        changed: list[tuple[str, TruthLabel, TruthLabel]] = []
        for item_id in sorted(set(before) & set(after)):
            if before[item_id] != after[item_id]:
                changed.append((item_id, before[item_id], after[item_id]))
        return ItemDiff(added=added, removed=removed, label_changed=tuple(changed))

    def snapshot_labels(self) -> dict[str, TruthLabel]:
        return {item_id: item.label for item_id, item in sorted(self._items.items())}
