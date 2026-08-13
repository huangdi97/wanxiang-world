"""Content truth/status taxonomy and ledger value objects (G04D).

Truth labels keep canon, source-backed facts, completion, model inference,
reconstruction and user fiction strictly separate; only reviewed evidence can
promote an item toward canon.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

TruthLabel = Literal[
    "canon",
    "source_backed",
    "completion",
    "model_inference",
    "reconstruction",
    "user_fiction",
]

TRUTH_LABELS: tuple[TruthLabel, ...] = (
    "canon",
    "source_backed",
    "completion",
    "model_inference",
    "reconstruction",
    "user_fiction",
)

# Promotion table: allowed next labels per current label (deterministic).
_ALLOWED_PROMOTIONS: dict[TruthLabel, tuple[TruthLabel, ...]] = {
    "user_fiction": ("completion",),
    "model_inference": ("completion", "reconstruction"),
    "completion": ("source_backed",),
    "reconstruction": ("source_backed",),
    "source_backed": ("canon",),
    "canon": (),
}

# Canon promotion additionally requires review + evidence; model inference and
# user fiction can never jump straight to canon.
_CANON_REQUIRES_REVIEW = {"model_inference", "user_fiction", "reconstruction", "completion"}


def allowed_promotions(label: TruthLabel) -> tuple[TruthLabel, ...]:
    return _ALLOWED_PROMOTIONS[label]


def requires_review_for_canon(current: TruthLabel) -> bool:
    return current in _CANON_REQUIRES_REVIEW


@dataclass(frozen=True, slots=True)
class ContentItem:
    """A ledger item with a truth label, provenance and lock state."""

    item_id: str
    label: TruthLabel
    source_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    rationale: str = ""
    reviewer: str = ""
    review_version: int = 0
    locked: bool = False
    rights_usage: str = "canonical"
    rights_approved: bool = False

    def __post_init__(self) -> None:
        if not self.item_id:
            raise ContractError("item_id must be non-empty")
        if self.label not in TRUTH_LABELS:
            raise ContractError(f"unknown truth label {self.label!r}")


@dataclass(frozen=True, slots=True)
class ReviewDecision:
    """Immutable review decision (append-only history)."""

    decision_id: str
    item_id: str
    from_label: TruthLabel
    to_label: TruthLabel
    reviewer: str
    rationale: str
    review_version: int
    evidence_refs: tuple[str, ...] = ()
    is_override: bool = False

    def __post_init__(self) -> None:
        if not self.decision_id or not self.item_id:
            raise ContractError("decision requires decision_id and item_id")
        if not self.reviewer:
            raise ContractError("review decision requires reviewer identity")
        if not self.rationale:
            raise ContractError("review decision requires a rationale")


@dataclass(frozen=True, slots=True)
class ItemDiff:
    """Diff between two package-version item sets."""

    added: tuple[str, ...]
    removed: tuple[str, ...]
    label_changed: tuple[tuple[str, TruthLabel, TruthLabel], ...]

    @property
    def empty(self) -> bool:
        return not self.added and not self.removed and not self.label_changed
