"""G16I: performance, capacity, cost & resource-budget qualification.

- Benchmark results include hardware/environment.
- No severe regression against loose absolute floors (SQLite durability profile).
- Resource budget violations are visible.
"""

from __future__ import annotations

import pytest
from scripts.benchmarks import benchmark_commits, benchmark_replay, environment


def test_benchmark_records_environment() -> None:
    env = environment()
    assert env["platform"]
    assert env["python"]
    assert env["machine"]


def test_commit_and_replay_within_operating_floor() -> None:
    commits = benchmark_commits(n=100)
    assert commits["events"] == 100
    assert commits["events_per_second"] > 5, "commit throughput regressed below floor"
    replay = benchmark_replay(n=1200)
    assert replay["events"] == 1200
    assert replay["replay_seconds"] < 30.0, "replay regressed below floor"


def test_resource_budgets_visible() -> None:
    from wanxiang_substrate.recovery.budget import BudgetTracker, ResourceBudget
    from wanxiang_substrate.recovery.errors import BudgetExceeded

    tracker = BudgetTracker(ResourceBudget(max_commands=10))
    for _ in range(10):
        tracker.consume(commands=1)
    with pytest.raises(BudgetExceeded):
        tracker.consume(commands=1)
    remaining = tracker.remaining()
    assert remaining["commands"] == 0
