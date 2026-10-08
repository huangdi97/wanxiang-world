"""G92F resource/cost budget and graceful backpressure tests."""

from __future__ import annotations

import pytest
from wanxiang_substrate.long_horizon import (
    BackpressurePolicy,
    BudgetKey,
    CostBudgetLedger,
    CostLimit,
    CostUsage,
)
from wanxiang_substrate.recovery.budget import BudgetTracker, ResourceBudget


def _ledger() -> tuple[CostBudgetLedger, tuple[BudgetKey, ...]]:
    ledger = CostBudgetLedger(
        backpressure=BackpressurePolicy(soft_queue_limit=2, hard_queue_limit=4)
    )
    keys = (
        BudgetKey("world", "world-1"),
        BudgetKey("actor", "actor-1"),
        BudgetKey("provider", "provider-1"),
    )
    for key in keys:
        ledger.register(
            key, CostLimit(max_calls=4, max_tokens=10, max_time_ms=100, max_storage_bytes=100)
        )
    return ledger, keys


def test_atomic_multi_scope_admission_and_alerts() -> None:
    ledger, keys = _ledger()
    accepted = ledger.admit(
        keys,
        CostUsage(calls=1, tokens=8, time_ms=10, storage_bytes=10),
        requested_lod="L0",
    )
    assert accepted.status == "accepted"
    assert {alert.metric for alert in accepted.alerts} == {"tokens"}
    assert all(ledger.usage(key).tokens == 8 for key in keys)


def test_exhaustion_degrades_without_partial_charge_and_backpressure_is_graceful() -> None:
    ledger, keys = _ledger()
    ledger.admit(keys, CostUsage(tokens=8), requested_lod="L0")
    degraded = ledger.admit(
        keys,
        CostUsage(tokens=3),
        requested_lod="L0",
    )
    assert degraded.status == "degraded"
    assert degraded.recommended_lod == "L1"
    assert all(ledger.usage(key).tokens == 8 for key in keys)
    deferred = ledger.admit(keys, CostUsage(calls=1), requested_lod="L1", queue_depth=2)
    rejected = ledger.admit(keys, CostUsage(calls=1), requested_lod="L1", queue_depth=4)
    assert deferred.status == "deferred"
    assert rejected.status == "rejected"


def test_resource_tracker_rejects_negative_consumption() -> None:
    tracker = BudgetTracker(ResourceBudget(max_commands=2, max_ticks=2))
    with pytest.raises(ValueError, match="cannot be negative"):
        tracker.consume(commands=-1)
    assert tracker.remaining() == {"commands": 2, "ticks": 2, "model_calls": 0}
