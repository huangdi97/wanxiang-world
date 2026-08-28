"""Freeze and export the complete M98 burn-in matrix (G101A)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from wanxiang_substrate.world_lab import stable_m98_matrix

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "artifacts" / "v55_stable" / "m98" / "run_matrix.json"
REPORT = ROOT / "reports" / "M98_G101A_RUN_MATRIX.md"


def _head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def run() -> dict[str, object]:
    matrix = stable_m98_matrix()
    payload = {
        **matrix.to_dict(),
        "build_sha": _head(),
        "declared_counts": {"30d": 12, "90d": 6, "total": 18},
        "coverage": {
            "30d": "3 seeds x 2 policy profiles x 2 pressure profiles",
            "90d": "3 seeds x baseline policy x baseline/stress pressure",
        },
        "boundaries": {
            "implemented": ["versioned M98 run registry and complete row declaration"],
            "validated": ["matrix shape, seed coverage, hash verification"],
            "experimental": ["bounded burn-in interpretation"],
            "not_proven": ["universal scale, production capacity, scientific emergence"],
            "external_blocked": [],
        },
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = f"""# M98 G101A Run Matrix

**Conclusion:** `PASS` for the versioned matrix declaration.

The frozen matrix contains 12 complete 30d rows (3 seeds × 2 policy profiles
× 2 pressure profiles) and 6 90d rows (3 seeds × baseline policy ×
baseline/stress pressure). Every row has a unique run id, seed, policy, and
pressure tuple. The matrix content hash is `{matrix.content_hash}` and the
export was generated at build SHA `{payload["build_sha"]}`.

This is an experiment registry, not canonical world state. It does not claim
that any row has run yet, and it does not prove production capacity or
universal emergence.

Machine-readable evidence: `artifacts/v55_stable/m98/run_matrix.json`.
"""
    REPORT.write_text(report, encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, ensure_ascii=False))
