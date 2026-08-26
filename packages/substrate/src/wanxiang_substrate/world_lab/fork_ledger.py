"""Append-only intervention evidence ledger (G95C)."""

from __future__ import annotations

from collections.abc import Mapping
from threading import RLock
from typing import cast

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.reality.errors import ExperimentError
from wanxiang_substrate.world_lab.fork_models import (
    FORK_SCHEMA_VERSION,
    InterventionLedgerEntry,
    LedgerStatus,
    count,
    digest,
    ref,
)


class InterventionLedger:
    """Thread-safe append-only evidence log, separate from canonical history."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._entries: list[InterventionLedgerEntry] = []

    def append(self, entry: InterventionLedgerEntry) -> InterventionLedgerEntry:
        with self._lock:
            if any(item.entry_id == entry.entry_id for item in self._entries):
                raise ExperimentError(f"intervention ledger entry {entry.entry_id!r} exists")
            stored = entry.__class__(
                entry_id=entry.entry_id,
                run_id=entry.run_id,
                provenance_id=entry.provenance_id,
                branch_ref=entry.branch_ref,
                intervention_id=entry.intervention_id,
                status=entry.status,
                cursor_revision=entry.cursor_revision,
                replay_hash=entry.replay_hash,
                sequence=len(self._entries) + 1,
                schema_version=entry.schema_version,
            )
            self._entries.append(stored)
            return stored

    def entries(self, run_id: str | None = None) -> tuple[InterventionLedgerEntry, ...]:
        with self._lock:
            values = tuple(self._entries)
        if run_id is not None:
            values = tuple(item for item in values if item.run_id == run_id)
        return values

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": FORK_SCHEMA_VERSION,
            "entries": [entry.to_dict() for entry in self.entries()],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> InterventionLedger:
        if count(data.get("schema_version"), "schema_version") != FORK_SCHEMA_VERSION:
            raise ContractError("unsupported intervention ledger schema")
        raw_entries = data.get("entries", ())
        if not isinstance(raw_entries, (list, tuple)):
            raise ContractError("intervention ledger entries must be a list")
        ledger = cls()
        for raw in cast(list[object] | tuple[object, ...], raw_entries):
            if not isinstance(raw, Mapping):
                raise ContractError("intervention ledger entry must be a mapping")
            entry = _entry_from_dict(cast(Mapping[str, object], raw))
            if entry.sequence != len(ledger._entries) + 1:
                raise ContractError("intervention ledger sequence is not contiguous")
            ledger._entries.append(entry)
        return ledger


def _entry_from_dict(data: Mapping[str, object]) -> InterventionLedgerEntry:
    status = data.get("status")
    if not isinstance(status, str) or status not in {"forked", "resumed"}:
        raise ContractError("invalid intervention ledger status")
    return InterventionLedgerEntry(
        entry_id=ref(data.get("entry_id"), "entry_id"),
        run_id=ref(data.get("run_id"), "run_id"),
        provenance_id=ref(data.get("provenance_id"), "provenance_id"),
        branch_ref=ref(data.get("branch_ref"), "branch_ref"),
        intervention_id=ref(data.get("intervention_id"), "intervention_id"),
        status=cast(LedgerStatus, status),
        cursor_revision=count(data.get("cursor_revision"), "cursor_revision"),
        replay_hash=digest(data.get("replay_hash", ""), "replay_hash", allow_empty=True),
        sequence=count(data.get("sequence"), "sequence"),
        schema_version=count(data.get("schema_version"), "schema_version"),
    )


__all__ = ["InterventionLedger"]
