"""Claim conflict sets (G58B).

Conflicting claims coexist; never last-write-wins. A ConflictSet records the
conflicting claims, the source refs on each side, and an optional review
status; resolving a conflict is a review decision, not a data overwrite.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

ConflictStatus = Literal["open", "reviewing", "resolved"]
VALID_CONFLICT_STATUSES = ("open", "reviewing", "resolved")


@dataclass(frozen=True, slots=True)
class ConflictSet:
    """A set of mutually conflicting claims (all preserved)."""

    conflict_id: str
    claim_ids: tuple[str, ...]
    source_refs: tuple[str, ...]
    description: str
    status: ConflictStatus = "open"

    def __post_init__(self) -> None:
        if not self.conflict_id:
            raise ContractError("conflict requires an id")
        if len(self.claim_ids) < 2:
            raise ContractError("conflict requires at least 2 claims")
        if self.status not in VALID_CONFLICT_STATUSES:
            raise ContractError(f"invalid conflict status {self.status!r}")


class ConflictLedger:
    """Append-only conflict register; claims are never overwritten."""

    def __init__(self) -> None:
        self._conflicts: dict[str, ConflictSet] = {}
        self._by_claim: dict[str, tuple[str, ...]] = {}

    def register(self, conflict: ConflictSet) -> ConflictSet:
        if conflict.conflict_id not in self._conflicts:
            self._conflicts[conflict.conflict_id] = conflict
            for claim_id in conflict.claim_ids:
                self._by_claim[claim_id] = self._by_claim.get(claim_id, ()) + (
                    conflict.conflict_id,
                )
        return self._conflicts[conflict.conflict_id]

    def get(self, conflict_id: str) -> ConflictSet | None:
        return self._conflicts.get(conflict_id)

    def conflicts_for_claim(self, claim_id: str) -> tuple[ConflictSet, ...]:
        return tuple(
            self._conflicts[cid]
            for cid in self._by_claim.get(claim_id, ())
            if cid in self._conflicts
        )

    def all(self) -> tuple[ConflictSet, ...]:
        return tuple(self._conflicts.values())
