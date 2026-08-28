"""Execute all declared 90d M98 rows (G101C)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from wanxiang_substrate.world_lab import stable_m98_matrix

from m98_burn_in_execution import run_worldline
from m98_burn_in_support import write_json

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "artifacts" / "v55_stable" / "m98" / "90d_burn_in.json"
REPORT = ROOT / "reports" / "M98_G101C_90D_BURN_IN.md"


def _head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def run() -> dict[str, object]:
    matrix = stable_m98_matrix()
    rows = tuple(row for row in matrix.rows if row.horizon == "90d")
    build_sha = _head()
    results = tuple(run_worldline(row, build_sha=build_sha) for row in rows)
    completed = sum(item["conclusion"] == "PASS" for item in results)
    payload: dict[str, object] = {
        "schema": "wanxiang.v5.5.m98.90d-burn-in.v1",
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
            "implemented": [
                "90d SQLite matrix execution",
                "checkpoint/replay/restart/branch probes per row",
            ],
            "validated": [
                "complete declared 90d subset only when every row completes",
                "no unreconciled checkpoint or replay corruption in completed rows",
            ],
            "experimental": ["bounded long-horizon interpretation"],
            "not_proven": [
                "production SLO",
                "live customer capacity",
                "universal emergence",
            ],
            "external_blocked": [],
        },
    }
    write_json(ARTIFACT, payload)
    report = f"""# M98 G101C 90d Burn-in

**Conclusion:** `{payload["conclusion"]}` — `{completed}/{len(rows)}` declared rows completed.

The runner executed the complete declared 90-day subset independently on
migrated SQLite WorldRuntime instances. Each completed row includes daily
checkpoints and cursor fingerprints, horizon replay/recovery samples, restart
reconstruction, branch isolation, crash-safe checkpoint probing, provider
proposal-only evidence, and measured event/storage/timing/RSS metrics. Partial
aggregation is not accepted as a complete Gate 74 result.

Build SHA: `{build_sha}`. Matrix hash: `{matrix.content_hash}`.

This is bounded local engineering evidence using creator-owned synthetic input;
it is not live-customer, production-capacity, scientific, or universal-emergence
evidence. No canonical history is rewritten by the runner.

Machine-readable evidence: `artifacts/v55_stable/m98/90d_burn_in.json`.
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
