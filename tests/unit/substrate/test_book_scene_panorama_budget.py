"""T2 panorama budgets remain cumulative, idempotent, and restart safe."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import pathlib

import pytest
from wanxiang_substrate.assets.book_scene_panorama_budget import (
    _LocalJson_PanoramaBudgetLedger,
    _PanoramaBudgetLedger,
)


def test_in_memory_panorama_budget_reserves_once_and_exhausts() -> None:
    ledger = _PanoramaBudgetLedger()

    first = ledger.reserve("world-a", "scene-a", 3, 5)
    repeated = ledger.reserve("world-a", "scene-a", 3, 5)

    assert first == repeated
    assert first.reserved == 3
    assert first.remaining == 2
    assert first.reservations == 1
    assert ledger.has_reservation("world-a", "scene-a") is True
    assert ledger.reservation_cost("world-a", "scene-a") == 3
    assert ledger.has_reservation("world-a", "missing") is False
    assert ledger.reservation_cost("world-a", "missing") is None
    with pytest.raises(ValueError, match="budget is exhausted"):
        ledger.reserve("world-a", "scene-b", 3, 5)


def test_local_panorama_budget_survives_restart(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "panorama-budget.json"
    first = _LocalJson_PanoramaBudgetLedger(path)
    first.reserve("world-a", "scene-a", 4, 10)

    restarted = _LocalJson_PanoramaBudgetLedger(path)
    usage = restarted.usage("world-a", 10)
    assert usage.reserved == 4
    assert usage.remaining == 6
    assert restarted.has_reservation("world-a", "scene-a") is True
    assert restarted.reservation_cost("world-a", "scene-a") == 4
    assert restarted.has_reservation("world-a", "missing") is False
    assert restarted.reservation_cost("world-a", "missing") is None
    assert restarted.reserve("world-a", "scene-a", 4, 10).reservations == 1

    second = restarted.reserve("world-a", "scene-b", 4, 10)
    assert second.reserved == 8
    assert second.remaining == 2


def test_local_panorama_budget_corruption_fails_closed(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "panorama-budget.json"
    path.write_text("{not-json", encoding="utf-8")
    ledger = _LocalJson_PanoramaBudgetLedger(path)

    with pytest.raises(ValueError, match="unreadable"):
        ledger.usage("world-a", 10)
    with pytest.raises(ValueError, match="unreadable"):
        ledger.reserve("world-a", "scene-a", 3, 10)


@pytest.mark.parametrize("ledger_kind", ["memory", "local"])
def test_panorama_budget_reconciles_provider_overrun_conservatively(
    tmp_path: pathlib.Path,
    ledger_kind: str,
) -> None:
    ledger = (
        _PanoramaBudgetLedger()
        if ledger_kind == "memory"
        else _LocalJson_PanoramaBudgetLedger(tmp_path / "panorama-overrun.json")
    )
    ledger.reserve("world-a", "scene-a", 4, 10)

    usage = ledger.reconcile("world-a", "scene-a", 13, 10)

    assert usage.reserved == 13
    assert usage.remaining == 0
    assert usage.reservations == 1
    assert ledger.reservation_cost("world-a", "scene-a") == 13
    # A later lower report cannot erase already observed spend.
    again = ledger.reconcile("world-a", "scene-a", 5, 10)
    assert again.reserved == 13
