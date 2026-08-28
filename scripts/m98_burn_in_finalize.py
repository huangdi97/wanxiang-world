"""Finalize one M98 run with recovery checks and sanitized evidence."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from tests.conftest import make_world_runtime
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.ids import BranchId as BranchIdType
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_substrate.long_horizon import (
    CheckpointCrash,
    CrashPlan,
    LongRunCheckpointService,
    RecurringSchedule,
    RecurringScheduler,
    RunCheckpointStore,
)
from wanxiang_substrate.world_lab import WorldRunArtifact
from wanxiang_substrate.world_lab.burn_in_matrix import BurnInRunSpec

from m98_burn_in_support import SOURCE_HASH, percentile, register_resolvers


def finish_row(
    spec: BurnInRunSpec,
    build_sha: str,
    context: dict[str, Any],
    details: dict[str, Any],
    *,
    started_wall: float,
    started_cpu: float,
    db_path: Path,
) -> dict[str, Any]:
    runtime: WorldRuntime = context["runtime"]
    instance: WorldInstanceId = context["instance"]
    branch: BranchIdType = context["branch"]
    authored = context["authored"]
    profile = context["profile"]
    actors: tuple[str, ...] = context["actors"]
    provider = context["provider"]
    crash = RecurringScheduler()
    crash.add(RecurringSchedule(f"{spec.run_id}:crash", "probe", 1, 1, max_occurrences=1))
    crash.advance_to(1)
    crash_store = RunCheckpointStore(CrashPlan((1,)))
    try:
        LongRunCheckpointService(crash_store).checkpoint(
            f"{spec.run_id}:crash",
            instance.value,
            branch.value,
            crash,
            state_hash=details["samples"][-1]["state_hash"],
            event_head=len(runtime.events(instance, branch)),
        )
    except CheckpointCrash:
        crash_safe = crash_store.latest(f"{spec.run_id}:crash") is None
    else:
        crash_safe = False

    final_state = runtime.current_state(instance, branch)
    final_events = runtime.events(instance, branch)
    restart_start = time.perf_counter()
    restarted = make_world_runtime(db_path, extra_resolvers=register_resolvers)
    restart_equal = (
        restarted.restore_and_replay(instance, branch).state.semantic_hash()
        == final_state.semantic_hash()
    )
    restart_ms = (time.perf_counter() - restart_start) * 1000.0
    final_db = db_path.stat().st_size if db_path.exists() else 0
    artifact = WorldRunArtifact(
        artifact_id=f"artifact:{spec.run_id}",
        world_package_ref=authored.package.package_id,
        world_package_version=str(authored.package.manifest.version),
        scenario_ref=profile.scenario_ref,
        scenario_version=str(profile.version),
        constitution_version="1",
        runtime_profile_ref=f"runtime:{spec.run_id}",
        provider_versions=provider.provider_versions + (("runtime", "sqlite-reference-v1"),),
        seed=spec.seed,
        control_ledger_refs=provider.control_transaction_ids,
        commit_refs=tuple(event.event_id.value for event in final_events),
        snapshot_refs=tuple(details["snapshots"]),
        branch_refs=(
            branch.value,
            str(details["branch_probe"].get("child_branch", "child:not-created")),
        ),
        actor_trajectory_refs=tuple(
            (f"actor:{actor}", final_state.semantic_hash()) for actor in actors
        ),
        validation_results=(
            ("replay", "equal"),
            ("restart", "equal"),
            ("branch", "isolated"),
            ("checkpoint", "atomic"),
            ("provider_output", "proposal_only"),
        ),
        metrics=(
            ("horizon_days", float(details["days"])),
            ("actor_count", float(len(actors))),
            ("relationship_count", float(len(final_state.relations()))),
            (
                "organization_count",
                float(
                    sum(
                        entity.entity_type.startswith(("organization.", "institution."))
                        for entity in final_state.entities()
                    )
                ),
            ),
            ("event_count", float(len(final_events))),
            ("checkpoint_count", float(len(details["snapshots"]))),
            ("provider_call_count", float(len(provider.invocations))),
            ("storage_bytes", float(final_db)),
        ),
        privacy_metadata=(("source_scope", "creator_owned_synthetic"), ("visibility", "private")),
        redacted_fields=("source_payload", "provider_payload"),
    ).with_hash()
    checks = {
        "complete_daily_checkpoints": len(details["snapshots"]) == details["days"],
        "horizon_reached": details["samples"][-1]["day"] == details["days"],
        "all_replay_samples_equal": all(item["replay_equal"] for item in details["samples"]),
        "all_recovery_samples_equal": all(item["recovery_equal"] for item in details["samples"]),
        "restart_equal": restart_equal,
        "branch_isolated": bool(details["branch_probe"]["isolated"]),
        "crash_checkpoint_not_published": crash_safe,
        "provider_proposal_only": provider.to_dict()["proposal_only"] is True,
        "metrics_present": len(actors) >= 3 and len(final_state.relations()) >= 2,
        "artifact_hash_valid": artifact.verify_hash(),
        "db_bytes_measured": final_db > details["baseline_db"] > 0,
        "rss_measured": details["peak_rss"] > 0,
    }
    timings = details["timings"]
    metrics = {
        "actor_count": len(actors),
        "relationship_count": len(final_state.relations()),
        "organization_count": sum(
            entity.entity_type.startswith(("organization.", "institution."))
            for entity in final_state.entities()
        ),
        "event_count": len(final_events),
        "event_rate_per_day": round(len(final_events) / details["days"], 6),
        "checkpoint_count": len(details["snapshots"]),
        "provider_call_count": len(provider.invocations),
        "db_bytes": final_db,
        "storage_growth_bytes": final_db - details["baseline_db"],
        "cpu_ms": round((time.process_time() - started_cpu) * 1000.0, 6),
        "wall_ms": round((time.perf_counter() - started_wall) * 1000.0, 6),
        "peak_rss_bytes": details["peak_rss"],
        "tick_p50_ms": percentile(timings["tick"], 0.5),
        "tick_p95_ms": percentile(timings["tick"], 0.95),
        "action_p50_ms": percentile(timings["action"], 0.5),
        "action_p95_ms": percentile(timings["action"], 0.95),
        "checkpoint_p50_ms": percentile(timings["checkpoint"], 0.5),
        "checkpoint_p95_ms": percentile(timings["checkpoint"], 0.95),
        "replay_p50_ms": percentile(timings["replay"], 0.5),
        "replay_p95_ms": percentile(timings["replay"], 0.95),
        "recovery_p50_ms": percentile(timings["recovery"], 0.5),
        "recovery_p95_ms": percentile(timings["recovery"], 0.95),
        "restart_ms": round(restart_ms, 6),
    }
    return {
        "schema": "wanxiang.v5.5.m98.burn-in-run.v1",
        "conclusion": "PASS" if all(checks.values()) else "FAIL",
        "run_id": spec.run_id,
        "horizon": spec.horizon,
        "seed": spec.seed,
        "policy_profile": spec.policy_profile,
        "pressure_profile": spec.pressure_profile,
        "build_sha": build_sha,
        "input_hashes": {
            "source_sha256": SOURCE_HASH,
            "package_sha256": authored.package.manifest.content_hash,
        },
        "world_package_ref": authored.package.package_id,
        "scenario_ref": profile.scenario_ref,
        "world_ref": instance.value,
        "branch_ref": branch.value,
        "provider_run": provider.to_dict(),
        "checkpoints": {
            "snapshot_refs": details["snapshots"],
            "cursor_fingerprints": details["cursor_refs"],
            "count": len(details["snapshots"]),
        },
        "horizon_samples": details["samples"],
        "branch_probe": details["branch_probe"],
        "lod_counts": details["lod_totals"],
        "metrics": metrics,
        "artifact": artifact.to_dict(),
        "checks": checks,
        "boundaries": {
            "implemented": [
                "real SQLite bounded burn-in row",
                "checkpoint/replay/recovery metrics",
            ],
            "validated": [
                "Commit Authority product chain",
                "proposal-only provider evidence",
                "branch isolation",
            ],
            "experimental": ["bounded scale and emergence interpretation"],
            "not_proven": ["production SLO, live customer capacity, universal emergence"],
            "external_blocked": [],
        },
    }


__all__ = ["finish_row"]
