"""Shared measurements and proposal-side helpers for M98 burn-in runs."""

from __future__ import annotations

import ctypes
import json
import math
import os
import pathlib
from ctypes import wintypes
from typing import Any

try:
    import resource as _resource
except ImportError:  # pragma: no cover - Windows has no resource module
    _resource: Any = None

from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.ids import ActorId, BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.providers import ProviderCapability, ReferenceProvider
from wanxiang_substrate.capability.runtime_control import RuntimeControlLedger
from wanxiang_substrate.epistemic.resolver import register_epistemic_resolvers
from wanxiang_substrate.long_horizon import (
    ActorActivityInput,
    ActorAvailability,
    AvailabilityWindow,
    LODState,
    RecurringSchedule,
    RecurringScheduler,
    SimulationLODRuntime,
)
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers
from wanxiang_substrate.world_lab import (
    MultiProviderWorldlineRunner,
    ProviderAssignmentPolicy,
    ProviderRunInput,
)
from wanxiang_substrate.world_lab.burn_in_matrix import BurnInRunSpec

DAY = 100
SOURCE_CONTENT = (
    "# M98 creator-owned synthetic qualification\n"
    "Character: Alice\nCharacter: Bob\nCharacter: Carol\n"
    "Alice and Bob maintain a shared harbor ledger.\n"
    "relationship: Alice -> Bob\n"
    "rule: reviewed evidence remains proposal-only.\n"
)
SOURCE_REF = "memory://m98/creator-owned-synthetic-source"
SOURCE_HASH = payload_hash(SOURCE_CONTENT)


def source() -> SourceRecord:
    return SourceRecord(
        source_id="m98_creator_owned_synthetic_source",
        kind="text",
        content_hash=SOURCE_HASH,
        content_ref=SOURCE_REF,
        stage="E3",
        rights=RightsEnvelope(
            owner="m98-creator",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=False,
            training_allowed=False,
        ),
        payload=SOURCE_CONTENT,
        provenance="creator_owned_synthetic_m98",
        access="private",
    )


def register_resolvers(registry: ResolverRegistry) -> None:
    register_preview_resolvers(registry)
    register_temporal_resolvers(registry)
    register_epistemic_resolvers(registry)


def actor_ids(state: InMemoryCanonicalState) -> dict[str, str]:
    result: dict[str, str] = {}
    for entity in state.entities():
        for component in entity.components.values():
            if component.component_type == "profile":
                display_name = component.fields.get("display_name")
                if isinstance(display_name, str):
                    result[display_name] = entity.entity_id.value
    return result


def commit(
    runtime: WorldRuntime,
    instance: WorldInstanceId,
    branch: BranchId,
    *,
    command_id: str,
    action_type: str,
    payload: dict[str, FieldValue],
    world_time: int,
    actor_id: str | None = None,
) -> Any:
    current = runtime.current_state(instance, branch)
    # The burn-in trace uses colon-separated logical labels, while the domain
    # CommandId contract permits only lowercase letters, digits, ``_`` and
    # ``-``. Keep the logical label deterministic and map it at the boundary.
    normalized_command_id = command_id.replace(":", "_")
    return runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId(normalized_command_id),
            instance_id=instance,
            branch_id=branch,
            expected_revision=current.revision,
            action_type=action_type,
            payload=payload,
            actor_id=ActorId(actor_id) if actor_id else None,
            world_time=WorldTime(world_time),
        )
    )


def provider_run(spec: BurnInRunSpec, package: Any, profile: Any, actors: tuple[str, ...]) -> Any:
    provider_id = "provider:m98:reference-semantic"
    capability = ProviderCapability(provider_id, "semantic", "1.0.0", True, 1, True, True)
    runner = MultiProviderWorldlineRunner(
        {provider_id: ReferenceProvider(capability)}, RuntimeControlLedger()
    )
    run_input = ProviderRunInput(
        run_id=spec.run_id,
        world_package_ref=package.package_id,
        world_package_version=str(package.manifest.version),
        scenario_ref=profile.scenario_ref,
        scenario_version=str(profile.version),
        source_refs=(SOURCE_REF,),
        population_refs=tuple(f"actor:{actor}" for actor in actors),
        seed=spec.seed,
        parameters=(
            ("policy_profile", spec.policy_profile),
            ("pressure_profile", spec.pressure_profile),
        ),
        payload=SOURCE_CONTENT,
        private_source=True,
        control_timestamp="2026-08-28T00:00:00Z",
    )
    policy = ProviderAssignmentPolicy(
        policy_id=f"policy:m98:{spec.policy_profile}",
        version=1,
        mode="homogeneous",
        provider_ids=(provider_id,),
    )
    return runner.execute(run_input, policy)


def scheduler(actors: tuple[str, ...], days: int, run_id: str) -> RecurringScheduler:
    availability = ActorAvailability(
        tuple(AvailabilityWindow(actor, DAY, days * DAY + 1) for actor in actors)
    )
    result = RecurringScheduler(availability=availability)
    for index, actor in enumerate(actors):
        result.add(
            RecurringSchedule(
                schedule_id=f"{run_id}:schedule:{index}",
                action="set_status",
                start_tick=DAY,
                interval_ticks=DAY,
                actor_id=actor,
                payload=tuple(sorted((("entity_id", actor), ("status", "active")))),
                max_occurrences=days,
            )
        )
    return result


def lod_snapshot(actors: tuple[str, ...], tick: int, run_id: str) -> dict[str, int]:
    lod = SimulationLODRuntime()
    counts: dict[str, int] = dict.fromkeys(("L0", "L1", "L2", "L3", "L4"), 0)
    for index, actor in enumerate(actors):
        activity = ActorActivityInput(
            actor_id=actor,
            current_tick=tick,
            last_active_tick=max(0, tick - DAY if index == 0 else 0),
            goal_urgency=0.9 if index == 0 else 0.0,
            interaction_rate=0.7 if index < 2 else 0.0,
            proximity=0.5 if index == 0 else 0.0,
        )
        score = lod.score(activity)
        state = LODState(actor, "L0", f"state:{run_id}:{actor}", f"memory:{run_id}:{actor}:summary")
        level = lod.transition(state, score).to_level
        counts[level] += 1
    return counts


def memory_payload(run_id: str, actor: str, day: int, tick: int) -> dict[str, FieldValue]:
    return {
        "memory_id": f"memory_{run_id}_{actor}_{day:03d}",
        "actor_id": actor,
        "content_ref": f"memory://m98/{run_id}/{actor}/{day:03d}",
        "at_ticks": tick,
        "salience": 0.5,
        "source_obs_ref": f"observation://m98/{run_id}/{actor}/{day:03d}",
    }


def db_bytes(path: pathlib.Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def rss_bytes() -> int:
    if os.name == "nt":

        class Counters(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]

        counters = Counters()
        counters.cb = ctypes.sizeof(Counters)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        current_process = kernel32.GetCurrentProcess
        current_process.argtypes = []
        current_process.restype = wintypes.HANDLE
        get_process_memory_info = psapi.GetProcessMemoryInfo
        get_process_memory_info.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(Counters),
            wintypes.DWORD,
        ]
        get_process_memory_info.restype = wintypes.BOOL
        ok = get_process_memory_info(current_process(), ctypes.byref(counters), counters.cb)
        return int(counters.PeakWorkingSetSize if ok else counters.WorkingSetSize)
    if _resource is not None:
        return int(_resource.getrusage(_resource.RUSAGE_SELF).ru_maxrss * 1024)
    return 0


def percentile(values: list[float], percentile_value: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(len(ordered) * percentile_value) - 1))
    return round(ordered[index], 6)


def write_json(path: pathlib.Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


__all__ = [
    "DAY",
    "SOURCE_CONTENT",
    "SOURCE_HASH",
    "SOURCE_REF",
    "actor_ids",
    "commit",
    "db_bytes",
    "lod_snapshot",
    "memory_payload",
    "percentile",
    "provider_run",
    "register_resolvers",
    "rss_bytes",
    "scheduler",
    "source",
    "write_json",
]
