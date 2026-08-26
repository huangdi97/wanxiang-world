"""G95C: explicit fork provenance, append-only ledger, and resume evidence."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.world_lab import InterventionLedger, InterventionLedgerEntry


def _entry(status: str = "forked", sequence: int = 0) -> InterventionLedgerEntry:
    return InterventionLedgerEntry(
        entry_id=f"entry:g95c:{status}:{sequence}",
        run_id="run:g95c",
        provenance_id="provenance:g95c",
        branch_ref="br:g95c-child",
        intervention_id="intervention:g95c",
        status=status,  # type: ignore[arg-type]
        cursor_revision=3,
        replay_hash="" if status == "forked" else "a" * 64,
        sequence=sequence,
    )


def test_intervention_ledger_is_append_only_and_round_trips() -> None:
    ledger = InterventionLedger()
    first = ledger.append(_entry())
    second = ledger.append(_entry("resumed"))

    restored = InterventionLedger.from_dict(ledger.to_dict())

    assert first.sequence == 1
    assert second.sequence == 2
    assert restored.entries() == ledger.entries()
    with pytest.raises(ContractError, match="contiguous"):
        InterventionLedger.from_dict(
            {"schema_version": 1, "entries": [first.to_dict() | {"sequence": 2}]}
        )


def test_ledger_entry_is_immutable() -> None:
    entry = _entry()
    with pytest.raises(AttributeError):
        entry.status = "resumed"  # type: ignore[misc]
