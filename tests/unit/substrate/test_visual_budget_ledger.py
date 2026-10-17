"""Durable per-world visual budget counts survive a restart on one filesystem."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time
from typing import cast

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
