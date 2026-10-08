"""Execute one M98 row on a real migrated SQLite runtime."""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.conftest import cleanup_db_file, fresh_db_path  # noqa: E402
from wanxiang_substrate.world_lab.burn_in_matrix import BurnInRunSpec  # noqa: E402

from m98_burn_in_finalize import finish_row  # noqa: E402
from m98_burn_in_runtime import run_days, setup_runtime  # noqa: E402


def run_worldline(spec: BurnInRunSpec, *, build_sha: str) -> dict[str, Any]:
    db_path = fresh_db_path()
    started_wall = time.perf_counter()
    started_cpu = time.process_time()
    try:
        context = setup_runtime(spec, db_path)
        details = run_days(spec, context, db_path)
        return finish_row(
            spec,
            build_sha,
            context,
            details,
            started_wall=started_wall,
            started_cpu=started_cpu,
            db_path=db_path,
        )
    except Exception as exc:
        return {
            "schema": "wanxiang.v5.5.m98.burn-in-run.v1",
            "conclusion": "FAIL",
            "run_id": spec.run_id,
            "horizon": spec.horizon,
            "seed": spec.seed,
            "policy_profile": spec.policy_profile,
            "pressure_profile": spec.pressure_profile,
            "build_sha": build_sha,
            "failure": f"{type(exc).__name__}: {str(exc)[:512]}",
            "boundaries": {
                "implemented": [],
                "validated": [],
                "experimental": ["bounded burn-in"],
                "not_proven": ["this row did not complete"],
                "external_blocked": [],
            },
        }
    finally:
        cleanup_db_file(db_path)


__all__ = ["run_worldline"]
