"""T2 panorama budgets remain cumulative, idempotent, and restart safe."""

from __future__ import annotations

import pathlib

import pytest
from wanxiang_substrate.assets.book_scene_panorama_budget import (
    LocalJsonPanoramaBudgetLedger,
    PanoramaBudgetLedger,
)


def test_in_memory_panorama_budget_reserves_once_and_exhausts() -> None:
    ledger = PanoramaBudgetLedger()

    first = ledger.reserve("world-a", "scene-a", 3, 5)
    repeated = ledger.reserve("world-a", "scene-a", 3, 5)

    assert first == repeated
    assert first.reserved == 3
    assert first.remaining == 2
    assert first.reservations == 1
    with pytest.raises(ValueError, match="budget is exhausted"):
        ledger.reserve("world-a", "scene-b", 3, 5)


def test_local_panorama_budget_survives_restart(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "panorama-budget.json"
    first = LocalJsonPanoramaBudgetLedger(path)
    first.reserve("world-a", "scene-a", 4, 10)

    restarted = LocalJsonPanoramaBudgetLedger(path)
    usage = restarted.usage("world-a", 10)
    assert usage.reserved == 4
    assert usage.remaining == 6
    assert restarted.reserve("world-a", "scene-a", 4, 10).reservations == 1

    second = restarted.reserve("world-a", "scene-b", 4, 10)
    assert second.reserved == 8
    assert second.remaining == 2


def test_local_panorama_budget_corruption_fails_closed(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "panorama-budget.json"
    path.write_text("{not-json", encoding="utf-8")
    ledger = LocalJsonPanoramaBudgetLedger(path)

    with pytest.raises(ValueError, match="unreadable"):
        ledger.usage("world-a", 10)
    with pytest.raises(ValueError, match="unreadable"):
        ledger.reserve("world-a", "scene-a", 3, 10)
