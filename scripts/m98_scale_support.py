"""Frozen standard fixture, provider accounting, and LOD measurements for G101E."""

from __future__ import annotations

from typing import Any

from wanxiang_domain.hashing import semantic_sha256
from wanxiang_substrate.authoring.providers import ProviderCapability, ReferenceProvider
from wanxiang_substrate.capability.runtime_control import RuntimeControlLedger
from wanxiang_substrate.long_horizon import (
    ActorActivityInput,
    LODState,
    SimulationLODRuntime,
)
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import (
    MultiProviderWorldlineRunner,
    ProviderAssignmentPolicy,
    ProviderRunInput,
)

SCALE_TEMPLATE = "m98-standard-scale-template-v1"
SCALE_HEADER = (
    "# M98 creator-owned standard scale fixture\n"
    "rule: all actor policies remain proposal-only and bounded\n"
)
SCALE_TEMPLATE_HASH = semantic_sha256(
    {"template": SCALE_TEMPLATE, "profile": "book", "header": SCALE_HEADER}
)


def actor_name(index: int) -> str:
    if index < 1:
        raise ValueError("scale actor index must be positive")
    value = index
    suffix: list[str] = []
    while value:
        value, remainder = divmod(value - 1, 26)
        suffix.append(chr(ord("A") + remainder))
    return "Actor" + "".join(reversed(suffix))


def standard_source(actor_count: int) -> SourceRecord:
    if actor_count < 1:
        raise ValueError("scale fixture requires at least one actor")
    content = SCALE_HEADER + "".join(
        f"Character: {actor_name(index)}\n" for index in range(1, actor_count + 1)
    )
    return SourceRecord(
        source_id=f"m98_standard_scale_{actor_count}",
        kind="text",
        content_hash=payload_hash(content),
        content_ref=f"memory://m98/standard-scale/{actor_count}",
        stage="E3",
        rights=RightsEnvelope(
            owner="m98-creator",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=False,
            training_allowed=False,
        ),
        payload=content,
        provenance=f"creator_owned_synthetic:{SCALE_TEMPLATE}",
        access="private",
    )


def provider_run(
    run_id: str,
    source_record: SourceRecord,
    package: Any,
    profile: Any,
    actors: tuple[str, ...],
    seed: int,
) -> Any:
    provider_id = "provider:m98:reference-semantic"
    capability = ProviderCapability(provider_id, "semantic", "1.0.0", True, 1, True, True)
    runner = MultiProviderWorldlineRunner(
        {provider_id: ReferenceProvider(capability)}, RuntimeControlLedger()
    )
    run_input = ProviderRunInput(
        run_id=run_id,
        world_package_ref=package.package_id,
        world_package_version=str(package.manifest.version),
        scenario_ref=profile.scenario_ref,
        scenario_version=str(profile.version),
        source_refs=(source_record.content_ref,),
        population_refs=tuple(f"actor:{actor}" for actor in actors),
        seed=seed,
        parameters=(("scale_template", SCALE_TEMPLATE), ("actor_count", str(len(actors)))),
        payload=source_record.payload,
        private_source=True,
        control_timestamp="2026-08-28T00:00:00Z",
    )
    policy = ProviderAssignmentPolicy(
        policy_id="policy:m98:scale-baseline",
        version=1,
        mode="homogeneous",
        provider_ids=(provider_id,),
    )
    return runner.execute(run_input, policy)


def lod_measure(actors: tuple[str, ...], seed: int) -> dict[str, object]:
    runtime = SimulationLODRuntime()
    current_tick = 1000
    counts: dict[str, int] = dict.fromkeys(("L0", "L1", "L2", "L3", "L4"), 0)
    active_floor = max(2, min(20, max(2, len(actors) // 10)))
    for index, actor in enumerate(actors):
        if index == 0:
            goal, interaction, proximity, last_active = 1.0, 1.0, 1.0, current_tick
        elif index < active_floor:
            goal, interaction, proximity, last_active = 0.7, 0.6, 0.3, current_tick
        elif index % 7 == 0:
            goal, interaction, proximity, last_active = 0.2, 0.2, 0.1, 0
        elif index % 3 == 0:
            goal, interaction, proximity, last_active = 0.2, 0.1, 0.0, current_tick
        elif index % 2 == 0:
            goal, interaction, proximity, last_active = 0.05, 0.1, 0.0, current_tick
        else:
            goal, interaction, proximity, last_active = 0.0, 0.0, 0.0, 0
        activity = ActorActivityInput(
            actor_id=actor,
            current_tick=current_tick,
            last_active_tick=last_active,
            goal_urgency=goal,
            interaction_rate=interaction,
            proximity=proximity,
        )
        score = runtime.score(activity)
        state = LODState(
            actor,
            "L0",
            f"state:m98-scale:{seed}:{actor}",
            f"memory:m98-scale:{seed}:{actor}:summary",
        )
        transition = runtime.transition(state, score)
        counts[transition.to_level] += 1
    return {
        "lod_counts": counts,
        "active_actor_count": counts["L0"] + counts["L1"],
        "full_policy_actor_count": len(actors),
        "population_count": len(actors),
        "lod_policy": {
            "l0_threshold": runtime.policy.l0_threshold,
            "l1_threshold": runtime.policy.l1_threshold,
            "l2_threshold": runtime.policy.l2_threshold,
            "l3_threshold": runtime.policy.l3_threshold,
        },
    }


__all__ = [
    "SCALE_TEMPLATE",
    "SCALE_TEMPLATE_HASH",
    "actor_name",
    "lod_measure",
    "provider_run",
    "standard_source",
]
