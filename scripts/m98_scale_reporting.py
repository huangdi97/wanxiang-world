"""Aggregate and publish G101E/G101F scale-ladder evidence."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from m98_burn_in_support import write_json
from m98_scale_support import SCALE_TEMPLATE, SCALE_TEMPLATE_HASH

ROOT = Path(__file__).resolve().parent.parent
TIERS = (10, 50, 100, 500, 1000)
REPETITIONS = 3
ARTIFACT = ROOT / "artifacts" / "v55_stable" / "m98" / "scale_curve.json"
REPORT = ROOT / "reports" / "M98_G101E_SCALE_LADDER.md"


def _tier_summary(rows: list[dict[str, Any]], actor_count: int) -> dict[str, Any]:
    complete = [row for row in rows if row["conclusion"] == "PASS"]
    metrics = [row["metrics"] for row in complete]
    if not metrics:
        return {
            "tier": actor_count,
            "repetitions": len(rows),
            "completed": 0,
            "failed": len(rows),
        }
    return {
        "tier": actor_count,
        "repetitions": len(rows),
        "completed": len(complete),
        "failed": len(rows) - len(complete),
        "active_actor_counts": sorted({item["active_actor_count"] for item in metrics}),
        "full_policy_actor_counts": sorted({item["full_policy_actor_count"] for item in metrics}),
        "mean_wall_ms": round(sum(item["wall_ms"] for item in metrics) / len(metrics), 6),
        "max_action_p95_ms": max(item["action_p95_ms"] for item in metrics),
        "max_replay_ms": max(item["replay_duration_ms"] for item in metrics),
        "max_recovery_ms": max(item["recovery_duration_ms"] for item in metrics),
        "max_db_bytes": max(item["db_bytes"] for item in metrics),
        "max_peak_rss_bytes": max(item["peak_rss_bytes"] for item in metrics),
        "mean_provider_calls": sum(item["provider_call_count"] for item in metrics) / len(metrics),
    }


def record_results(rows: list[dict[str, Any]], build_sha: str) -> dict[str, Any]:
    failed = [row for row in rows if row["conclusion"] != "PASS"]
    tier_summaries = [
        _tier_summary([row for row in rows if row["tier"] == tier], tier) for tier in TIERS
    ]
    payload: dict[str, Any] = {
        "schema": "wanxiang.v5.5.m98.scale-curve.v1",
        "conclusion": "PASS" if not failed and len(rows) == len(TIERS) * REPETITIONS else "FAIL",
        "build_sha": build_sha,
        "template": SCALE_TEMPLATE,
        "template_hash": SCALE_TEMPLATE_HASH,
        "tiers": list(TIERS),
        "repetitions_per_tier": REPETITIONS,
        "declared_rows": len(TIERS) * REPETITIONS,
        "completed_rows": len(rows) - len(failed),
        "failed_rows": len(failed),
        "aggregation_complete": len(rows) == len(TIERS) * REPETITIONS,
        "tier_summaries": tier_summaries,
        "rows": rows,
        "capacity_interpretation": {
            "observed_knee": "not_observed_within_1000_actor_tiers"
            if not failed
            else "see_failed_tiers",
            "extrapolation_to_10k_or_100k": "forbidden",
            "active_vs_full_policy_separated": True,
            "provider_cost_usd": 0.0,
            "provider_cost_basis": "local_reference_provider_no_monetary_charge",
        },
        "boundaries": {
            "implemented": [
                "10/50/100/500/1000 real SQLite tiers",
                "three independent repetitions per tier",
            ],
            "validated": ["only completed declared tiers and repetitions"],
            "experimental": ["bounded capacity/degradation interpretation"],
            "not_proven": ["10k/100k capacity", "universal production envelope"],
            "external_blocked": [],
        },
    }
    write_json(ARTIFACT, payload)
    completed = payload["completed_rows"]
    declared = payload["declared_rows"]
    REPORT.write_text(
        f"""# M98 G101E/G101F Scale Ladder and Capacity Measurements

**Conclusion:** `{payload["conclusion"]}` — `{completed}/{declared}` rows completed.

The runner used the frozen `{SCALE_TEMPLATE}` standard fixture template and
`book` profile through OneClickAuthoring, PlayableService, Commit Authority, and
real migrated SQLite runtimes. It measured 10, 50, 100, 500, and 1000 actor
tiers with three independent repetitions per tier. Population size, actual
full-policy actor count, and SimulationLOD L0/L1 active count are separate fields.

Each completed row records provider calls/cost basis, CPU, peak RSS, database
bytes and growth, event count/rate, tick/action p50/p95, checkpoint duration and
storage delta, replay/recovery durations, package/world/branch refs, and
replay/recovery/proposal-only/LOD checks. Build SHA: `{build_sha}`; template
hash: `{SCALE_TEMPLATE_HASH}`.

All results are bounded local engineering measurements. A passing 1000-actor
tier is not extrapolated to 10k/100k, and the local reference provider has no
monetary charge; no production capacity or universal-emergence claim is made.

Machine-readable evidence: `artifacts/v55_stable/m98/scale_curve.json`.
""",
        encoding="utf-8",
    )
    return payload


__all__ = ["REPETITIONS", "TIERS", "record_results"]
