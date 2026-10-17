"""Durable per-world visual budget counts survive a restart on one filesystem."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import pathlib

from wanxiang_substrate.assets.book_scene_budget import VisualBudgetLedger


def test_budget_ledger_persists_counts_per_world(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "budget.json"
    first = VisualBudgetLedger(path)
    first.record("world-a", 2)
    first.record("world-b", 1)

    restarted = VisualBudgetLedger(path)

    assert restarted.used("world-a") == 2
    assert restarted.used("world-b") == 1
    assert restarted.used("world-c") == 0


def test_budget_ledger_rejects_corrupt_files_without_losing_future_writes(
    tmp_path: pathlib.Path,
) -> None:
    path = tmp_path / "budget.json"
    path.write_text("{not-json", encoding="utf-8")

    ledger = VisualBudgetLedger(path)

    assert ledger.used("world-a") == 0
    ledger.record("world-a", 1)
    assert VisualBudgetLedger(path).used("world-a") == 1
