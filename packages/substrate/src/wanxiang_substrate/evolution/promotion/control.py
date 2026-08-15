"""Promotion control ledger ? replayable & revocable (G33C).

Every promotion decision is written to an append-only control ledger (auditable,
replayable). A cancel/withdraw only changes the derived definition's
installability/registry status; it NEVER deletes or rewrites source history.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

PromotionStatus = Literal["active", "withdrawn"]


@dataclass(frozen=True, slots=True)
class PromotionRecord:
    """One promotion decision (append-only)."""

    record_id: str
    derived_definition_id: str
    source_worldline_ref: str
    parent_definition_ref: str
    status: PromotionStatus = "active"
    rationale: str = ""
    created_at: str = ""


class PromotionControlLedger:
    """Append-only promotion control ledger (replayable; withdrawal is a status)."""

    def __init__(self) -> None:
        self._records: dict[str, PromotionRecord] = {}

    def record(self, record: PromotionRecord) -> PromotionRecord:
        if record.record_id in self._records:
            raise ValueError(f"promotion record {record.record_id!r} already exists")
        self._records[record.record_id] = record
        return record

    def withdraw(self, record_id: str, rationale: str = "withdrawn") -> PromotionRecord:
        """Withdraw a promotion: only installability/registry status changes."""
        current = self._records.get(record_id)
        if current is None:
            raise ValueError(f"promotion record {record_id!r} not found")
        if current.status == "withdrawn":
            raise ValueError(f"promotion {record_id!r} is already withdrawn")
        updated = replace(current, status="withdrawn", rationale=rationale)
        self._records[record_id] = updated
        return updated

    def status(self, record_id: str) -> PromotionStatus:
        record = self._records.get(record_id)
        if record is None:
            raise ValueError(f"promotion record {record_id!r} not found")
        return record.status

    def records(self) -> tuple[PromotionRecord, ...]:
        return tuple(sorted(self._records.values(), key=lambda r: r.record_id))

    def count(self) -> int:
        return len(self._records)
