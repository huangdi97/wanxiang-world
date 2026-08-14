"""Runtime Control Ledger (G30F).

Runtime capability/provider changes (activate, deactivate, install, uninstall)
are RuntimeControlTransactions: ADD-only records in the Runtime Control Ledger.
They are NEVER World Commits ? they never enter the canonical event stream and
never touch Commit Authority.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeControlTransaction:
    """An append-only record of a runtime capability change."""

    transaction_id: str
    operation: str  # activate | deactivate | install | uninstall
    provider_id: str
    capability_name: str
    version: str
    rationale: str
    created_at: str

    def __post_init__(self) -> None:
        if self.operation not in ("activate", "deactivate", "install", "uninstall"):
            raise ValueError(f"unknown runtime control operation {self.operation!r}")
        if not self.transaction_id or not self.provider_id or not self.capability_name:
            raise ValueError("runtime control transaction requires ids and capability name")


class RuntimeControlLedger:
    """Append-only in-memory runtime control ledger (never a World Commit)."""

    def __init__(self) -> None:
        self._entries: list[RuntimeControlTransaction] = []

    def record(self, transaction: RuntimeControlTransaction) -> RuntimeControlTransaction:
        self._entries.append(transaction)
        return transaction

    def entries(self) -> tuple[RuntimeControlTransaction, ...]:
        return tuple(self._entries)
