"""Runtime Control Ledger acceptance: persistence, timeline and rollback semantics."""

from __future__ import annotations

from pathlib import Path

import pytest
from wanxiang_substrate.capability.runtime_control import (
    RuntimeControlLedger,
    RuntimeControlTransaction,
)


def _tx(
    transaction_id: str,
    *,
    operation: str = "activate",
    version: str = "1.0.0",
    status: str = "applied",
    world_revision: int | None = 0,
    event_ref: str = "",
) -> RuntimeControlTransaction:
    return RuntimeControlTransaction(
        transaction_id=transaction_id,
        operation=operation,  # type: ignore[arg-type]
        provider_id="provider.model",
        capability_name="model",
        version=version,
        rationale="qualification",
        created_at="2026-10-07T00:00:00Z",
        status=status,  # type: ignore[arg-type]
        worldline_id="wl-1",
        effective_world_revision=world_revision,
        world_event_ref=event_ref,
        profile_ref="world.reference@1.0.0",
        permissions=("model.invoke",),
        parameters=(("temperature", "0"),),
        artifact_hash=f"sha:{transaction_id}",
    )


def test_activation_reload_rollback_and_failed_transaction_timeline(tmp_path: Path) -> None:
    path = tmp_path / "runtime-control.jsonl"
    ledger = RuntimeControlLedger(path)

    first = ledger.record(_tx("tx-1", version="1.0.0", world_revision=0))
    failed = ledger.record(
        _tx("tx-2", operation="reload", version="2.0.0", status="failed", world_revision=2)
    )
    rollback = ledger.record(
        _tx("tx-3", operation="rollback", version="1.0.0", world_revision=3)
    )

    assert (first.runtime_revision, failed.runtime_revision, rollback.runtime_revision) == (1, 2, 3)
    assert ledger.active_at(worldline_id="wl-1", world_revision=2)["model"].version == "1.0.0"
    assert ledger.active_at(worldline_id="wl-1", world_revision=3)["model"].version == "1.0.0"

    restored = RuntimeControlLedger(path)
    assert restored.entries() == ledger.entries()
    restored_active = restored.active_at(worldline_id="wl-1", world_revision=3)
    assert restored_active["model"].transaction_id == "tx-3"


def test_deactivation_removes_capability_and_event_query_is_explicit() -> None:
    ledger = RuntimeControlLedger()
    ledger.record(_tx("tx-1", event_ref="evt-1"))
    ledger.record(_tx("tx-2", operation="deactivate", world_revision=4, event_ref="evt-4"))

    assert ledger.active_at(worldline_id="wl-1", world_revision=3)["model"].version == "1.0.0"
    assert "model" not in ledger.active_at(worldline_id="wl-1", world_revision=4)
    event_transactions = ledger.configuration_for_event("evt-1")
    assert tuple(item.transaction_id for item in event_transactions) == ("tx-1",)


def test_runtime_control_is_not_a_world_commit_surface() -> None:
    ledger = RuntimeControlLedger()
    assert not hasattr(ledger, "commit")
    assert not hasattr(ledger, "append_world_event")


def test_runtime_control_rejects_secret_bearing_parameters() -> None:
    with pytest.raises(ValueError, match="secret-bearing"):
        RuntimeControlTransaction(
            transaction_id="tx-secret",
            operation="activate",
            provider_id="provider.model",
            capability_name="model",
            version="1.0.0",
            rationale="qualification",
            created_at="2026-10-07T00:00:00Z",
            parameters=(("api_key", "must-not-land-in-ledger"),),
        )
