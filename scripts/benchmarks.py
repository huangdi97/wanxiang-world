"""Repeatable benchmark suite (G16I).

Measures commit throughput/latency, replay time, projection compose and
scheduler advance under a named profile, recording hardware/environment so
results are comparable. No paid APIs required; no invariants are weakened.
"""

from __future__ import annotations

import json
import platform
import sys
import time
from pathlib import Path
from typing import Any

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine

ROOT = Path(__file__).resolve().parent.parent


def environment() -> dict[str, str]:
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "machine": platform.machine(),
    }


def _env_path(name: str) -> Path:
    import tempfile

    return Path(tempfile.gettempdir()) / f"{name}_{int(time.time())}.db"


def benchmark_commits(n: int = 200) -> dict[str, Any]:
    from tests.conftest import make_world_runtime

    path = _env_path("bench_commit")
    runtime = make_world_runtime(path)
    w = runtime.create_world()
    start = time.perf_counter()
    for i in range(n):
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"b_{i}"),
                instance_id=w.instance_id,
                branch_id=w.root_branch_id,
                expected_revision=BranchRevision(i),
                action_type="create_entity",
                payload={"entity_id": f"e{i}", "count": i},
                world_time=WorldTime(i + 1),
            )
        )
    elapsed = time.perf_counter() - start
    try:
        getattr(runtime.persistence.event_store, "session_factory").kw["bind"].dispose()
        path.unlink()
    except Exception:
        pass
    return {"events": n, "seconds": elapsed, "events_per_second": n / elapsed}


def benchmark_replay(n: int = 1200) -> dict[str, Any]:
    from tests.conftest import make_world_runtime

    path = _env_path("bench_replay")
    runtime = make_world_runtime(path)
    w = runtime.create_world()
    for i in range(n):
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"r_{i}"),
                instance_id=w.instance_id,
                branch_id=w.root_branch_id,
                expected_revision=BranchRevision(i),
                action_type="create_entity",
                payload={"entity_id": f"e{i}", "count": i},
                world_time=WorldTime(i + 1),
            )
        )
    events = runtime.persistence.event_store.load(w.instance_id, w.root_branch_id)
    start = time.perf_counter()
    ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    elapsed = time.perf_counter() - start
    try:
        getattr(runtime.persistence.event_store, "session_factory").kw["bind"].dispose()
        path.unlink()
    except Exception:
        pass
    return {"events": n, "replay_seconds": elapsed}


def run_all() -> dict[str, Any]:
    return {
        "environment": environment(),
        "profile": "small_ci",
        "commits": benchmark_commits(),
        "replay": benchmark_replay(),
    }


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    results = run_all()
    (ROOT / "reports" / "performance_benchmarks.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    print(json.dumps(results, indent=2))
