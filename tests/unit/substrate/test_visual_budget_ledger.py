"""Durable per-world visual budget counts survive a restart on one filesystem."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time
from typing import cast

import pytest
from wanxiang_substrate.assets.book_scene_budget import VisualBudgetLedger

_WORKER = """
import json
import pathlib
import sys
import time

from wanxiang_substrate.assets.book_scene_budget import VisualBudgetLedger

root = pathlib.Path(sys.argv[1])
ledger = VisualBudgetLedger(root / "budget.json")
(root / f"ready-{sys.argv[2]}").touch()
while not (root / "go").exists():
    time.sleep(0.01)
for _ in range(20):
    ledger.record("world-shared", 1)
print(json.dumps({"done": True}))
"""


_RESERVE_WORKER = """
import json
import pathlib
import sys
import time

from wanxiang_substrate.assets.book_scene_budget import VisualBudgetLedger

root = pathlib.Path(sys.argv[1])
worker_id = sys.argv[2]
ledger = VisualBudgetLedger(root / "reserve-budget.json")
(root / f"reserve-ready-{worker_id}").touch()
while not (root / "reserve-go").exists():
    time.sleep(0.01)
try:
    reserved = ledger.reserve("world-shared", f"scene-{worker_id}", 1)
    result = {"reserved": reserved}
except ValueError as exc:
    result = {"reserved": False, "error": str(exc)}
print(json.dumps(result))
"""


def test_budget_ledger_persists_counts_per_world(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "budget.json"
    first = VisualBudgetLedger(path)
    first.record("world-a", 2)
    first.record("world-b", 1)

    restarted = VisualBudgetLedger(path)

    assert restarted.used("world-a") == 2
    assert restarted.used("world-b") == 1
    assert restarted.used("world-c") == 0


def test_budget_ledger_corruption_fails_closed_instead_of_resetting_spend(
    tmp_path: pathlib.Path,
) -> None:
    path = tmp_path / "budget.json"
    path.write_text("{not-json", encoding="utf-8")

    with pytest.raises(ValueError, match="unreadable"):
        VisualBudgetLedger(path)


def test_concurrent_processes_do_not_lose_budget_counts(tmp_path: pathlib.Path) -> None:
    workers = 4
    processes: list[subprocess.Popen[str]] = []
    try:
        for worker_id in range(workers):
            processes.append(
                subprocess.Popen(
                    [sys.executable, "-c", _WORKER, str(tmp_path), str(worker_id)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            )
        deadline = time.monotonic() + 30
        while not all((tmp_path / f"ready-{i}").exists() for i in range(workers)):
            assert time.monotonic() < deadline, "budget ledger worker startup timed out"
            assert all(p.poll() is None for p in processes), "budget worker exited early"
            time.sleep(0.02)
        (tmp_path / "go").write_text("go", encoding="utf-8")
        for process in processes:
            out, err = process.communicate(timeout=60)
            assert process.returncode == 0, err
            decoded: object = json.loads(out)
            assert isinstance(decoded, dict)
            assert cast(dict[str, object], decoded).get("done") is True
        assert VisualBudgetLedger(tmp_path / "budget.json").used("world-shared") == workers * 20
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=10)


def test_budget_reservation_is_idempotent_and_enforces_world_limit(
    tmp_path: pathlib.Path,
) -> None:
    ledger = VisualBudgetLedger(tmp_path / "budget.json")

    assert ledger.reserve("world-a", "scene-a@provider-v1", 2) is True
    assert ledger.reserve("world-a", "scene-a@provider-v1", 2) is False
    assert ledger.used("world-a") == 1
    assert ledger.reserve("world-a", "scene-b@provider-v1", 2) is True
    assert ledger.used("world-a") == 2
    with pytest.raises(ValueError, match=r"budget exhausted \(2/2\)"):
        ledger.reserve("world-a", "scene-c@provider-v1", 2)


def test_budget_ledger_migrates_legacy_flat_counts_without_resetting_usage(
    tmp_path: pathlib.Path,
) -> None:
    path = tmp_path / "budget.json"
    path.write_text('{"world-a":2}', encoding="utf-8")

    ledger = VisualBudgetLedger(path)

    assert ledger.used("world-a") == 2
    assert ledger.reserve("world-a", "scene-c@provider-v1", 3) is True
    assert VisualBudgetLedger(path).used("world-a") == 3


def test_concurrent_processes_cannot_race_through_visual_limit(
    tmp_path: pathlib.Path,
) -> None:
    workers = 4
    processes: list[subprocess.Popen[str]] = []
    try:
        for worker_id in range(workers):
            processes.append(
                subprocess.Popen(
                    [sys.executable, "-c", _RESERVE_WORKER, str(tmp_path), str(worker_id)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            )
        deadline = time.monotonic() + 30
        while not all((tmp_path / f"reserve-ready-{i}").exists() for i in range(workers)):
            assert time.monotonic() < deadline, "reservation worker startup timed out"
            assert all(p.poll() is None for p in processes), "reservation worker exited early"
            time.sleep(0.02)
        (tmp_path / "reserve-go").write_text("go", encoding="utf-8")
        outcomes: list[dict[str, object]] = []
        for process in processes:
            out, err = process.communicate(timeout=60)
            assert process.returncode == 0, err
            decoded: object = json.loads(out)
            assert isinstance(decoded, dict)
            outcomes.append(cast(dict[str, object], decoded))
        assert sum(row.get("reserved") is True for row in outcomes) == 1
        assert VisualBudgetLedger(tmp_path / "reserve-budget.json").used("world-shared") == 1
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=10)
