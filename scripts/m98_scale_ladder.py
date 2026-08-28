"""Execute the real SQLite 10-to-1000 actor scale ladder (G101E/G101F)."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime  # noqa: E402
from wanxiang_application.world_runtime import WorldRuntime  # noqa: E402
from wanxiang_domain.ids import BranchId, WorldInstanceId  # noqa: E402
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion  # noqa: E402
from wanxiang_runtime.replay import ReplayEngine  # noqa: E402
from wanxiang_substrate.authoring.one_click import OneClickAuthoring  # noqa: E402
from wanxiang_substrate.playable import PlayableService  # noqa: E402

from m98_burn_in_support import (  # noqa: E402
    commit,
    db_bytes,
    register_resolvers,
    rss_bytes,
)
from m98_scale_reporting import record_results  # noqa: E402
from m98_scale_support import (  # noqa: E402
    SCALE_TEMPLATE,
    SCALE_TEMPLATE_HASH,
    actor_name,
    lod_measure,
    provider_run,
    standard_source,
)

TIERS = (10, 50, 100, 500, 1000)
REPETITIONS = 3
ARTIFACT = ROOT / "artifacts" / "v55_stable" / "m98" / "scale_curve.json"
REPORT = ROOT / "reports" / "M98_G101E_SCALE_LADDER.md"


def _head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def _percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    index = min(len(ordered) - 1, max(0, int(len(ordered) * fraction + 0.999999) - 1))
    return round(ordered[index], 6)


def _run_one(actor_count: int, repetition: int, seed: int, build_sha: str) -> dict[str, Any]:
    run_id = f"m98-scale-{actor_count}-r{repetition}"
    db_path = fresh_db_path()
    started_wall = time.perf_counter()
    started_cpu = time.process_time()
    try:
        runtime: WorldRuntime = make_world_runtime(db_path, extra_resolvers=register_resolvers)
        playable = PlayableService(runtime)
        source_record = standard_source(actor_count)
        author_start = time.perf_counter()
        authored = OneClickAuthoring().run(f"job_{run_id}", (source_record,), profile="book")
        author_ms = (time.perf_counter() - author_start) * 1000.0
        owner = f"owner_{run_id}"
        profile = playable.register_package(authored.package, owner_id=owner, visibility="private")
        avatar = playable.entry.create_character(
            owner,
            actor_name(1),
            compatible_profile_ids=(profile.experience_package_ref,),
            character_id=f"ent_{run_id}_avatar",
        )
        instantiate_start = time.perf_counter()
        entered = playable.enter(
            profile.profile_id,
            viewer_id=owner,
            mode="embodiment",
            session_id=f"session_{run_id}",
            character_id=avatar.character_id,
        )
        instantiate_ms = (time.perf_counter() - instantiate_start) * 1000.0
        instance_data = cast(dict[str, object], entered["instance"])
        instance = WorldInstanceId(str(instance_data["instance_id"]))
        branch = BranchId(playable.store.get_instance(instance.value).branch_id)
        names = {actor_name(index): None for index in range(1, actor_count + 1)}
        discovered = cast(dict[str, str], {})
        for entity_name, entity_id in _actor_ids(runtime, instance, branch).items():
            if entity_name in names:
                discovered[entity_name] = entity_id
        if len(discovered) != actor_count:
            raise RuntimeError(
                f"scale tier expected {actor_count} actors but discovered {len(discovered)}"
            )
        actors = tuple(discovered[actor_name(index)] for index in range(1, actor_count + 1))
        provider = provider_run(run_id, source_record, authored.package, profile, actors, seed)
        baseline_db = db_bytes(db_path)
        tick_start = time.perf_counter()
        commit(
            runtime,
            instance,
            branch,
            command_id=f"{run_id}:calendar",
            action_type="temporal.instantiate",
            payload={"fixture": "calendar", "version": 1},
            world_time=0,
        )
        commit(
            runtime,
            instance,
            branch,
            command_id=f"{run_id}:tick",
            action_type="temporal.advance_to",
            payload={"ticks": 1000},
            world_time=1000,
        )
        tick_ms = (time.perf_counter() - tick_start) * 1000.0
        action_times: list[float] = []
        for index in range(5):
            action_start = time.perf_counter()
            playable.action(
                instance.value,
                viewer_id=owner,
                action_type="set_status",
                payload={"entity_id": actors[0], "status": f"scale_{repetition}_{index}"},
            )
            action_times.append((time.perf_counter() - action_start) * 1000.0)
        checkpoint_before = db_bytes(db_path)
        checkpoint_start = time.perf_counter()
        snapshot = runtime.create_checkpoint(instance, branch)
        checkpoint_ms = (time.perf_counter() - checkpoint_start) * 1000.0
        checkpoint_size = max(0, db_bytes(db_path) - checkpoint_before)
        events = runtime.events(instance, branch)
        final_state = runtime.current_state(instance, branch)
        replay_start = time.perf_counter()
        replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
        replay_ms = (time.perf_counter() - replay_start) * 1000.0
        recovery_start = time.perf_counter()
        recovered = runtime.restore_and_replay(instance, branch)
        recovery_ms = (time.perf_counter() - recovery_start) * 1000.0
        lod = lod_measure(actors, seed)
        final_db = db_bytes(db_path)
        checks = {
            "actor_count_exact": len(actors) == actor_count,
            "checkpoint_created": bool(snapshot.snapshot_id.value),
            "replay_equal": replayed.semantic_hash() == final_state.semantic_hash(),
            "recovery_equal": recovered.state.semantic_hash() == final_state.semantic_hash(),
            "provider_proposal_only": provider.to_dict()["proposal_only"] is True,
            "lod_count_exact": sum(cast(dict[str, int], lod["lod_counts"]).values()) == actor_count,
            "db_measured": final_db > baseline_db > 0,
            "rss_measured": rss_bytes() > 0,
        }
        return {
            "schema": "wanxiang.v5.5.m98.scale-row.v1",
            "conclusion": "PASS" if all(checks.values()) else "FAIL",
            "run_id": run_id,
            "tier": actor_count,
            "repetition": repetition,
            "seed": seed,
            "build_sha": build_sha,
            "template": SCALE_TEMPLATE,
            "template_hash": SCALE_TEMPLATE_HASH,
            "source_sha256": source_record.content_hash,
            "package_sha256": authored.package.manifest.content_hash,
            "world_package_ref": authored.package.package_id,
            "scenario_ref": profile.scenario_ref,
            "world_ref": instance.value,
            "branch_ref": branch.value,
            "snapshot_ref": snapshot.snapshot_id.value,
            "metrics": {
                **lod,
                "event_count": len(events),
                "event_rate_per_tick": len(events) / 1000.0,
                "provider_call_count": len(provider.invocations),
                "provider_cost_units": len(provider.invocations),
                "provider_cost_usd": 0.0,
                "provider_cost_basis": "local_reference_provider_no_monetary_charge",
                "db_bytes": final_db,
                "storage_growth_bytes": final_db - baseline_db,
                "authoring_ms": round(author_ms, 6),
                "instantiation_ms": round(instantiate_ms, 6),
                "cpu_ms": round((time.process_time() - started_cpu) * 1000.0, 6),
                "wall_ms": round((time.perf_counter() - started_wall) * 1000.0, 6),
                "peak_rss_bytes": rss_bytes(),
                "tick_p50_ms": round(tick_ms, 6),
                "tick_p95_ms": round(tick_ms, 6),
                "action_p50_ms": _percentile(action_times, 0.5),
                "action_p95_ms": _percentile(action_times, 0.95),
                "checkpoint_duration_ms": round(checkpoint_ms, 6),
                "checkpoint_size_bytes": checkpoint_size,
                "replay_duration_ms": round(replay_ms, 6),
                "recovery_duration_ms": round(recovery_ms, 6),
            },
            "checks": checks,
            "boundaries": {
                "implemented": [
                    "real Playable/SQLite standard fixture scale tier",
                    "SimulationLOD policy measurement",
                    "provider/runtime/storage/timing measurement",
                ],
                "validated": ["this exact tier/repetition only"],
                "experimental": ["bounded scale interpretation"],
                "not_proven": ["10k/100k extrapolation", "universal capacity"],
                "external_blocked": [],
            },
        }
    except Exception as exc:
        return {
            "schema": "wanxiang.v5.5.m98.scale-row.v1",
            "conclusion": "FAIL",
            "run_id": run_id,
            "tier": actor_count,
            "repetition": repetition,
            "seed": seed,
            "build_sha": build_sha,
            "failure": f"{type(exc).__name__}: {str(exc)[:512]}",
            "boundaries": {
                "implemented": [],
                "validated": [],
                "experimental": ["bounded scale interpretation"],
                "not_proven": ["this tier did not complete"],
                "external_blocked": [],
            },
        }
    finally:
        cleanup_db_file(db_path)


def _actor_ids(
    runtime: WorldRuntime, instance: WorldInstanceId, branch: BranchId
) -> dict[str, str]:
    result: dict[str, str] = {}
    for entity in runtime.current_state(instance, branch).entities():
        for component in entity.components.values():
            if component.component_type == "profile":
                display_name = component.fields.get("display_name")
                if isinstance(display_name, str):
                    result[display_name] = entity.entity_id.value
    return result


def run() -> dict[str, Any]:
    build_sha = _head()
    rows: list[dict[str, Any]] = []
    for tier in TIERS:
        tier_rows = [
            _run_one(tier, repetition, 10100 + tier * 10 + repetition, build_sha)
            for repetition in range(1, REPETITIONS + 1)
        ]
        rows.extend(tier_rows)
    return record_results(rows, build_sha)


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
