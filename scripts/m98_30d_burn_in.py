"""Execute all declared 30d M98 rows (G101B)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from wanxiang_substrate.world_lab import stable_m98_matrix

from m98_burn_in_execution import run_worldline
from m98_burn_in_support import write_json

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "artifacts" / "v55_stable" / "m98" / "30d_burn_in.json"
REPORT = ROOT / "reports" / "M98_G101B_30D_BURN_IN.md"


def _head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def run() -> dict[str, object]:
    matrix = stable_m98_matrix()
    rows = tuple(row for row in matrix.rows if row.horizon == "30d")
    build_sha = _head()
    results = tuple(run_worldline(row, build_sha=build_sha) for row in rows)
    completed = sum(item["conclusion"] == "PASS" for item in results)
    payload: dict[str, object] = {
        "schema": "wanxiang.v5.5.m98.30d-burn-in.v1",
        "conclusion": "PASS" if completed == len(rows) else "FAIL",
        "build_sha": build_sha,
        "matrix_id": matrix.matrix_id,
        "matrix_hash": matrix.content_hash,
        "declared_rows": len(rows),
        "completed_rows": completed,
        "failed_rows": len(rows) - completed,
        "aggregation_complete": completed == len(rows),
        "rows": list(results),
        "boundaries": {
            "implemented": ["30d SQLite matrix execution and per-row WorldRunArtifact"],
            "validated": ["full 12-row coverage only when every row completes"],
            "experimental": ["bounded burn-in interpretation"],
            "not_proven": ["90d qualification, production capacity, universal emergence"],
            "external_blocked": [],
        },
    }
    write_json(ARTIFACT, payload)
    report = f"""# M98 G101B 30d Burn-in

**Conclusion:** `{payload["conclusion"]}` — `{completed}/{len(rows)}` declared rows completed.

The runner executed each row independently on a migrated SQLite WorldRuntime
through OneClickAuthoring, WorldPackage, PlayableService, Commit Authority,
daily accelerated world time, memory observations, checkpoints, replay,
restart recovery, and branch isolation. Each completed row has a sanitized
WorldRunArtifact, provider control/proposal evidence, actor/relationship/
organization metrics, and measured storage/timing fields. Partial aggregation
is not accepted as a complete Gate 73 result.

Build SHA: `{build_sha}`. Matrix hash: `{matrix.content_hash}`.

The source fixture is creator-owned synthetic qualification content; its raw
text is not exported. This is bounded engineering/lab evidence, not a live
customer, production-capacity, scientific, or universal-emergence claim.

Machine-readable evidence: `artifacts/v55_stable/m98/30d_burn_in.json`.
"""
    REPORT.write_text(report, encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = run()
    print(
        json.dumps(
            {
                key: result[key]
                for key in ("conclusion", "declared_rows", "completed_rows", "failed_rows")
            },
            indent=2,
        )
    )
    raise SystemExit(0 if result["conclusion"] == "PASS" else 1)
