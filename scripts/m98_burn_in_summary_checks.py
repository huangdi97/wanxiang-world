"""Machine predicates for the G101G/M98 evidence summary."""

from __future__ import annotations

from typing import Any


def _all_checks(rows: list[dict[str, Any]]) -> bool:
    return all(all(bool(value) for value in row.get("checks", {}).values()) for row in rows)


def matrix_shape(matrix: dict[str, Any]) -> dict[str, Any]:
    rows = matrix["rows"]
    expected_30 = {
        (seed, policy, pressure)
        for seed in (9801, 9802, 9803)
        for policy in ("baseline", "conservative")
        for pressure in ("low", "high")
    }
    expected_90 = {
        (seed, pressure) for seed in (9811, 9812, 9813) for pressure in ("baseline", "stress")
    }
    observed_30 = {
        (row["seed"], row["policy_profile"], row["pressure_profile"])
        for row in rows
        if row["horizon"] == "30d"
    }
    observed_90 = {
        (row["seed"], row["pressure_profile"]) for row in rows if row["horizon"] == "90d"
    }
    shape_ok = (
        len(rows) == 18
        and matrix["declared_counts"] == {"30d": 12, "90d": 6, "total": 18}
        and observed_30 == expected_30
        and observed_90 == expected_90
        and matrix["content_hash"]
    )
    return {
        "status": "PASS" if shape_ok else "FAIL",
        "declared_rows": len(rows),
        "expected_rows": 18,
        "content_hash": matrix["content_hash"],
        "30d_shape": len(observed_30) == 12,
        "90d_shape": len(observed_90) == 6,
    }


def burn_gate(artifact: dict[str, Any], expected_rows: int, matrix_hash: str) -> dict[str, Any]:
    rows = artifact["rows"]
    checks_ok = _all_checks(rows)
    complete = (
        artifact["conclusion"] == "PASS"
        and artifact["declared_rows"] == expected_rows
        and artifact["completed_rows"] == expected_rows
        and artifact["failed_rows"] == 0
        and artifact["aggregation_complete"] is True
        and len(rows) == expected_rows
        and all(row["conclusion"] == "PASS" for row in rows)
        and artifact["matrix_hash"] == matrix_hash
        and checks_ok
    )
    return {
        "status": "PASS" if complete else "FAIL",
        "declared_rows": artifact["declared_rows"],
        "completed_rows": artifact["completed_rows"],
        "failed_rows": artifact["failed_rows"],
        "aggregation_complete": artifact["aggregation_complete"],
        "all_row_checks": checks_ok,
        "build_sha": artifact["build_sha"],
        "matrix_hash": artifact["matrix_hash"],
        "run_refs": [row["run_id"] for row in rows],
    }


def emergence_gate(artifact: dict[str, Any]) -> dict[str, Any]:
    positive = artifact["positive_world"]
    control = artifact["null_control"]
    detections = positive["candidate_evidence"]["pattern_detections"]
    safety = artifact["safety"]
    checks_ok = all(bool(value) for value in artifact["checks"].values())
    safety_ok = (
        safety["candidate_layer_only"] is True
        and safety["ontology_law_institution_auto_commit"] is False
        and safety["canonical_state_and_history_unchanged_by_candidate_derivation"] is True
        and safety["promotion_boundary_invoked"] is False
    )
    qualified = len(detections) >= 3 and all(
        detection["qualified"] is True for detection in detections
    )
    control_ok = (
        control["evidence"]["detection"]["qualified"] is False
        and control["evidence"]["norm_candidate_rejected"] is True
    )
    complete = (
        artifact["conclusion"] == "PASS" and checks_ok and safety_ok and qualified and control_ok
    )
    return {
        "status": "PASS" if complete else "FAIL",
        "build_sha": artifact["build_sha"],
        "seed": artifact["seed"],
        "positive_world_ref": positive["world_ref"],
        "positive_branch_ref": positive["branch_ref"],
        "positive_event_count": positive["event_count"],
        "qualified_detection_count": len(detections),
        "null_world_ref": control["world_ref"],
        "null_branch_ref": control["branch_ref"],
        "null_event_count": control["event_count"],
        "all_checks": checks_ok,
        "safety_boundary_ok": safety_ok,
        "control_rejected": control_ok,
    }


def scale_gate(artifact: dict[str, Any]) -> dict[str, Any]:
    expected_tiers = (10, 50, 100, 500, 1000)
    rows = artifact["rows"]
    tier_counts = {tier: sum(row["tier"] == tier for row in rows) for tier in expected_tiers}
    exact_population = all(
        row["metrics"]["population_count"] == row["tier"]
        and row["metrics"]["full_policy_actor_count"] == row["tier"]
        for row in rows
    )
    complete = (
        artifact["conclusion"] == "PASS"
        and artifact["tiers"] == list(expected_tiers)
        and artifact["repetitions_per_tier"] == 3
        and artifact["declared_rows"] == 15
        and artifact["completed_rows"] == 15
        and artifact["failed_rows"] == 0
        and artifact["aggregation_complete"] is True
        and len(rows) == 15
        and all(count == 3 for count in tier_counts.values())
        and all(bool(row["checks"]["actor_count_exact"]) for row in rows)
        and _all_checks(rows)
        and exact_population
    )
    return {
        "status": "PASS" if complete else "FAIL",
        "build_sha": artifact["build_sha"],
        "template": artifact["template"],
        "template_hash": artifact["template_hash"],
        "declared_rows": artifact["declared_rows"],
        "completed_rows": artifact["completed_rows"],
        "failed_rows": artifact["failed_rows"],
        "tier_counts": tier_counts,
        "exact_population_and_full_policy": exact_population,
        "active_counts_separate": artifact["capacity_interpretation"][
            "active_vs_full_policy_separated"
        ],
        "run_refs": [row["run_id"] for row in rows],
    }


def capacity_gate(artifact: dict[str, Any]) -> dict[str, Any]:
    required_metrics = (
        "cpu_ms",
        "peak_rss_bytes",
        "db_bytes",
        "event_count",
        "event_rate_per_tick",
        "provider_call_count",
        "tick_p50_ms",
        "tick_p95_ms",
        "action_p50_ms",
        "action_p95_ms",
        "checkpoint_duration_ms",
        "checkpoint_size_bytes",
        "replay_duration_ms",
        "recovery_duration_ms",
        "storage_growth_bytes",
    )
    rows = artifact["rows"]
    missing = [
        f"{row['run_id']}:{metric}"
        for row in rows
        for metric in required_metrics
        if metric not in row["metrics"]
    ]
    interpretation = artifact["capacity_interpretation"]
    complete = (
        artifact["conclusion"] == "PASS"
        and artifact["declared_rows"] == 15
        and artifact["completed_rows"] == 15
        and artifact["failed_rows"] == 0
        and len(rows) == 15
        and not missing
        and _all_checks(rows)
        and interpretation["extrapolation_to_10k_or_100k"] == "forbidden"
        and interpretation["knee_evidence"] is not None
        and interpretation["provider_cost_usd"] == 0.0
    )
    return {
        "status": "PASS" if complete else "FAIL",
        "build_sha": artifact["build_sha"],
        "declared_rows": artifact["declared_rows"],
        "completed_rows": artifact["completed_rows"],
        "failed_rows": artifact["failed_rows"],
        "required_metric_missing": missing,
        "observed_knee": interpretation["observed_knee"],
        "knee_evidence": interpretation["knee_evidence"],
        "no_10k_100k_extrapolation": interpretation["extrapolation_to_10k_or_100k"],
        "provider_cost_usd": interpretation["provider_cost_usd"],
    }


__all__ = ["burn_gate", "capacity_gate", "emergence_gate", "matrix_shape", "scale_gate"]
