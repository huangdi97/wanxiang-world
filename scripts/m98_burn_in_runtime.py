"""Runtime setup and daily loop for one M98 burn-in row."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, cast

from tests.conftest import make_world_runtime
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.hierarchy import BranchId
from wanxiang_domain.ids import BranchId as BranchIdType
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.long_horizon import (
    BackgroundPolicy,
    BackgroundSimulation,
    LongRunCheckpointService,
    RunCheckpointStore,
)
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.models import RuntimeProfile
from wanxiang_substrate.world_lab.burn_in_matrix import BurnInRunSpec

from m98_burn_in_probes import branch_probe, sample
from m98_burn_in_support import (
    DAY,
    actor_ids,
    commit,
    db_bytes,
    lod_snapshot,
    memory_payload,
    provider_run,
    register_resolvers,
    rss_bytes,
    scheduler,
    source,
)


def setup_runtime(spec: BurnInRunSpec, db_path: Path) -> dict[str, Any]:
    authored = OneClickAuthoring().run(f"job_{spec.run_id}", (source(),), profile="book")
    runtime: WorldRuntime = make_world_runtime(db_path, extra_resolvers=register_resolvers)
    playable = PlayableService(runtime)
    owner = f"owner:{spec.run_id}"
    profile = playable.register_package(authored.package, owner_id=owner, visibility="private")
    character = playable.entry.create_character(
        owner,
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id=owner,
        mode="embodiment",
        session_id=f"session:{spec.run_id}",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    names = actor_ids(runtime.current_state(instance, branch))
    if {"Alice", "Bob", "Carol"} - set(names):
        raise RuntimeError("source qualification package did not produce three actors")
    actors = tuple(sorted(names.values()))
    provider = provider_run(spec, authored.package, profile, actors)
    commit(
        runtime,
        instance,
        branch,
        command_id=f"{spec.run_id}:calendar",
        action_type="temporal.instantiate",
        payload={"fixture": "calendar", "version": 1},
        world_time=0,
    )
    commit(
        runtime,
        instance,
        branch,
        command_id=f"{spec.run_id}:create-organization",
        action_type="preview.create_entity",
        payload={
            "entity_id": "ent_m98_harbor_guild",
            "entity_type": "organization.guild",
            "display_name": "Harbor Guild",
        },
        world_time=runtime.current_state(instance, branch).revision.value + 1,
    )
    commit(
        runtime,
        instance,
        branch,
        command_id=f"{spec.run_id}:create-membership",
        action_type="preview.create_relation",
        payload={
            "relation_id": "rel_m98_harbor_guild",
            "source_id": names["Alice"],
            "target_id": "ent_m98_harbor_guild",
            "relation_type": "member_of",
        },
        world_time=runtime.current_state(instance, branch).revision.value + 1,
    )
    return {
        "authored": authored,
        "runtime": runtime,
        "playable": playable,
        "owner": owner,
        "profile": profile,
        "instance": instance,
        "branch": branch,
        "actors": actors,
        "provider": provider,
    }


def run_days(spec: BurnInRunSpec, context: dict[str, Any], db_path: Path) -> dict[str, Any]:
    runtime: WorldRuntime = context["runtime"]
    playable: PlayableService = context["playable"]
    owner: str = context["owner"]
    instance: WorldInstanceId = context["instance"]
    branch: BranchIdType = context["branch"]
    actors: tuple[str, ...] = context["actors"]
    days = 30 if spec.horizon == "30d" else 90
    run_scheduler = scheduler(actors, days, spec.run_id)
    background = BackgroundSimulation(
        run_scheduler,
        BackgroundPolicy(
            RuntimeProfile(
                f"runtime:{spec.run_id}", time_scale=DAY, simulation_lod="L1", seed=spec.seed
            ),
            mode="accelerated",
        ),
        world_ref=instance.value,
        branch_ref=branch.value,
    )
    cursor = background.leave(f"detached:{spec.run_id}")
    checkpoints = RunCheckpointStore()
    checkpoint_service = LongRunCheckpointService(checkpoints)
    snapshots: list[str] = []
    cursor_refs: list[str] = []
    samples: list[dict[str, Any]] = []
    timings: dict[str, list[float]] = {
        name: [] for name in ("tick", "action", "checkpoint", "replay", "recovery")
    }
    lod_totals: dict[str, int] = dict.fromkeys(("L0", "L1", "L2", "L3", "L4"), 0)
    branch_result: dict[str, Any] = {"isolated": False}
    baseline_db = db_bytes(db_path)
    peak_rss = rss_bytes()
    for day in range(1, days + 1):
        tick = day * DAY
        start = time.perf_counter()
        offline = background.run_offline(cursor, elapsed_ticks=1)
        cursor = background.reenter(offline)
        if len(offline.occurrences) != len(actors) or not all(
            item.available and item.due_tick == tick for item in offline.occurrences
        ):
            raise RuntimeError(f"scheduler occurrence mismatch at day {day}")
        timings["tick"].append((time.perf_counter() - start) * 1000.0)
        for level, count in lod_snapshot(actors, tick, spec.run_id).items():
            lod_totals[level] += count
        commit(
            runtime,
            instance,
            branch,
            command_id=f"{spec.run_id}:clock:{day:03d}",
            action_type="temporal.advance_to",
            payload={"ticks": tick},
            world_time=tick,
        )
        for index, actor in enumerate(actors):
            start = time.perf_counter()
            status = f"{spec.policy_profile}-{spec.pressure_profile}-day-{day:03d}"
            if actor == actors[0]:
                playable.action(
                    instance.value,
                    viewer_id=owner,
                    action_type="set_status",
                    payload={"entity_id": actor, "status": status},
                )
            else:
                commit(
                    runtime,
                    instance,
                    branch,
                    command_id=f"{spec.run_id}:status:{day:03d}:{index}",
                    action_type="set_status",
                    payload={"entity_id": actor, "status": status},
                    world_time=tick,
                    actor_id=actor,
                )
            commit(
                runtime,
                instance,
                branch,
                command_id=f"{spec.run_id}:memory:{day:03d}:{index}",
                action_type="epistemic.record_observation",
                payload=memory_payload(spec.run_id, actor, day, tick),
                world_time=tick,
                actor_id=actor,
            )
            if spec.pressure_profile in ("high", "stress") and index == 0:
                commit(
                    runtime,
                    instance,
                    branch,
                    command_id=f"{spec.run_id}:pressure:{day:03d}",
                    action_type="set_status",
                    payload={"entity_id": actor, "status": f"pressure-{day:03d}"},
                    world_time=tick,
                    actor_id=actor,
                )
            timings["action"].append((time.perf_counter() - start) * 1000.0)
        start = time.perf_counter()
        snapshot = runtime.create_checkpoint(instance, branch)
        snapshots.append(snapshot.snapshot_id.value)
        saved = checkpoint_service.checkpoint(
            spec.run_id,
            instance.value,
            branch.value,
            run_scheduler,
            state_hash=runtime.current_state(instance, branch).semantic_hash(),
            event_head=len(runtime.events(instance, branch)),
        )
        cursor_refs.append(saved.fingerprint)
        timings["checkpoint"].append((time.perf_counter() - start) * 1000.0)
        if day in (1, 7, 30, days):
            item, replay_ms, recovery_ms = sample(runtime, instance, branch, day, tick, db_path)
            samples.append(item)
            timings["replay"].append(replay_ms)
            timings["recovery"].append(recovery_ms)
        if day == max(2, days // 2):
            branch_result = branch_probe(runtime, instance, branch, actors[0], tick, spec.run_id)
        peak_rss = max(peak_rss, rss_bytes())
    return {
        "snapshots": snapshots,
        "cursor_refs": cursor_refs,
        "samples": samples,
        "timings": timings,
        "lod_totals": lod_totals,
        "branch_probe": branch_result,
        "baseline_db": baseline_db,
        "peak_rss": peak_rss,
        "days": days,
    }


__all__ = ["run_days", "setup_runtime"]
