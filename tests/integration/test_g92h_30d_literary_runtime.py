"""G92H: source-created literary world, accelerated through thirty days."""

from __future__ import annotations

import json
import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.ids import ActorId, BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.epistemic.query import EpistemicQuery
from wanxiang_substrate.epistemic.resolver import register_epistemic_resolvers
from wanxiang_substrate.long_horizon import (
    ActorActivityInput,
    ActorAvailability,
    AvailabilityWindow,
    BackgroundPolicy,
    BackgroundSimulation,
    BudgetKey,
    CheckpointCrash,
    CompactionPolicy,
    CompactionService,
    CostBudgetLedger,
    CostLimit,
    CostUsage,
    CrashPlan,
    HorizonQualification,
    HorizonSample,
    LODState,
    LongRunCheckpointService,
    RecurringSchedule,
    RecurringScheduler,
    RunCheckpointStore,
    SimulationLevel,
    SimulationLODRuntime,
    state_storage_bytes,
)
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.models import RuntimeProfile
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.temporal.query import TemporalQuery
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

DAY = 100
HORIZON_DAYS = 30
OWNER = "g92h_owner"


def _source() -> SourceRecord:
    content = (
        "# Literary Long Horizon\nCharacter: Alice\nCharacter: Bob\n"
        "Alice kept watch at the gate.\nBob carried the letter.\n"
        "relationship: Alice -> Bob\nrule: witnesses remember shared events\n"
    )
    return SourceRecord(
        source_id="g92h_literary_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g92h_literary_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="qualification",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g92h",
        access="private",
    )


def _register(registry: ResolverRegistry) -> None:
    register_preview_resolvers(registry)
    register_temporal_resolvers(registry)
    register_epistemic_resolvers(registry)


def _actor_ids(state: InMemoryCanonicalState) -> dict[str, str]:
    found: dict[str, str] = {}
    for entity in state.entities():
        for component in entity.components.values():
            if component.component_type != "profile":
                continue
            display_name = component.fields.get("display_name")
            if isinstance(display_name, str):
                found[display_name] = entity.entity_id.value
    return found


def _commit(
    runtime: WorldRuntime,
    instance: WorldInstanceId,
    branch: BranchId,
    *,
    command_id: str,
    action_type: str,
    payload: dict[str, FieldValue],
    world_time: int,
    actor_id: str | None = None,
) -> object:
    current = runtime.current_state(instance, branch)
    return runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=instance,
            branch_id=branch,
            expected_revision=current.revision,
            action_type=action_type,
            payload=payload,
            actor_id=ActorId(actor_id) if actor_id else None,
            world_time=WorldTime(world_time),
        )
    )


def _charge(
    ledger: CostBudgetLedger,
    runtime: WorldRuntime,
    instance: WorldInstanceId,
    branch: BranchId,
    *,
    before: int,
    keys: tuple[BudgetKey, ...],
    requested_lod: SimulationLevel,
) -> None:
    after = state_storage_bytes(runtime.current_state(instance, branch))
    delta = max(0, after - before)
    decision = ledger.admit(
        keys,
        CostUsage(calls=1, time_ms=1, storage_bytes=delta),
        requested_lod=requested_lod,
    )
    assert decision.status == "accepted"


@pytest.mark.integration
def test_source_created_literary_world_qualifies_for_accelerated_30d(
    persist_db_path: pathlib.Path,
) -> None:
    authored = OneClickAuthoring().run("job_g92h_literary", (_source(),), profile="book")
    assert authored.package.evidence_coverage > 0.0

    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(authored.package, owner_id=OWNER, visibility="private")
    character = playable.entry.create_character(
        OWNER,
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g92h_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id=OWNER,
        mode="embodiment",
        session_id="session_g92h_alice",
        character_id=character.character_id,
    )
    instance_payload = cast(dict[str, object], entered["instance"])
    instance = WorldInstanceId(str(instance_payload["instance_id"]))
    record = playable.store.get_instance(instance.value)
    branch = BranchId(record.branch_id)
    state = runtime.current_state(instance, branch)
    actors = _actor_ids(state)
    assert {"Alice", "Bob"}.issubset(actors)
    alice_id = actors["Alice"]
    bob_id = actors["Bob"]
    assert profile.world_package_ref == authored.package.package_id

    # The first real action travels through the product facade and then through
    # the existing Commit Authority before the detached long run begins.
    action = playable.action(
        instance.value,
        viewer_id=OWNER,
        action_type="set_status",
        payload={"entity_id": alice_id, "status": "active"},
    )
    assert action.event_id

    # The existing temporal fixture supplies only the canonical clock and
    # deterministic temporal entities; all long-run proposals below still use
    # the normal runtime command path.
    _commit(
        runtime,
        instance,
        branch,
        command_id="g92h_temporal_calendar",
        action_type="temporal.instantiate",
        payload={"fixture": "calendar", "version": 1},
        world_time=runtime.current_state(instance, branch).revision.value + 1,
    )

    world_budget = BudgetKey("world", instance.value)
    alice_budget = BudgetKey("actor", alice_id)
    bob_budget = BudgetKey("actor", bob_id)
    ledger = CostBudgetLedger()
    ledger.register(
        world_budget, CostLimit(max_calls=200, max_time_ms=200, max_storage_bytes=500_000)
    )
    ledger.register(
        alice_budget, CostLimit(max_calls=100, max_time_ms=100, max_storage_bytes=250_000)
    )
    ledger.register(
        bob_budget, CostLimit(max_calls=100, max_time_ms=100, max_storage_bytes=250_000)
    )

    availability = ActorAvailability(
        (
            AvailabilityWindow(alice_id, DAY, HORIZON_DAYS * DAY + 1),
            AvailabilityWindow(bob_id, DAY, HORIZON_DAYS * DAY + 1),
        )
    )
    scheduler = RecurringScheduler(availability=availability)
    for actor_id in (alice_id, bob_id):
        scheduler.add(
            RecurringSchedule(
                schedule_id=f"g92h_daily_{actor_id}",
                action="set_status",
                start_tick=DAY,
                interval_ticks=DAY,
                actor_id=actor_id,
                payload=(("entity_id", actor_id), ("status", "active")),
            )
        )
    profile_runtime = RuntimeProfile(
        runtime_id="g92h-accelerated",
        time_scale=DAY,
        simulation_lod="L1",
        seed=9208,
    )
    background = BackgroundSimulation(
        scheduler,
        BackgroundPolicy(profile_runtime, mode="accelerated"),
        world_ref=instance.value,
        branch_ref=branch.value,
    )
    cursor = background.leave("session_g92h_detached")
    checkpoint_store = RunCheckpointStore()
    checkpoint_service = LongRunCheckpointService(checkpoint_store)
    qualification = HorizonQualification("run-g92h-literary")
    lod_runtime = SimulationLODRuntime()
    lod_states = {
        actor_id: LODState(
            actor_id,
            "L0",
            f"world://{instance.value}/actor/{actor_id}",
            f"memory://{instance.value}/actor/{actor_id}/summary/0",
        )
        for actor_id in (alice_id, bob_id)
    }
    lod_levels: set[SimulationLevel] = set()
    baseline_storage = state_storage_bytes(runtime.current_state(instance, branch))
    checkpoint_count = 0

    for day in range(1, HORIZON_DAYS + 1):
        run = background.run_offline(cursor, elapsed_ticks=1)
        cursor = background.reenter(run)
        assert run.world_ticks_advanced == DAY
        assert len(run.occurrences) == 2
        assert all(item.available and item.due_tick == day * DAY for item in run.occurrences)

        for actor_id in (alice_id, bob_id):
            activity = ActorActivityInput(
                actor_id=actor_id,
                current_tick=day * DAY,
                last_active_tick=DAY if actor_id == alice_id else 0,
                goal_urgency=0.8 if actor_id == alice_id and day == 1 else 0.0,
                interaction_rate=0.7 if actor_id == alice_id and day == 1 else 0.0,
                proximity=0.6 if actor_id == alice_id and day == 1 else 0.0,
            )
            score = lod_runtime.score(activity)
            transition = lod_runtime.transition(lod_states[actor_id], score)
            lod_states[actor_id] = LODState(
                actor_id,
                transition.to_level,
                lod_states[actor_id].state_ref,
                f"memory://{instance.value}/actor/{actor_id}/summary/{day}",
            )
            lod_levels.add(transition.to_level)

        current_tick = day * DAY
        before = state_storage_bytes(runtime.current_state(instance, branch))
        _commit(
            runtime,
            instance,
            branch,
            command_id=f"g92h_clock_{day:02d}",
            action_type="temporal.advance_to",
            payload={"ticks": current_tick},
            world_time=current_tick,
        )
        _charge(
            ledger,
            runtime,
            instance,
            branch,
            before=before,
            keys=(world_budget,),
            requested_lod="L0",
        )

        for actor_index, actor_id in enumerate((alice_id, bob_id), start=1):
            actor_key = alice_budget if actor_id == alice_id else bob_budget
            before = state_storage_bytes(runtime.current_state(instance, branch))
            _commit(
                runtime,
                instance,
                branch,
                command_id=f"g92h_status_{day:02d}_{actor_index}",
                action_type="set_status",
                payload={"entity_id": actor_id, "status": "active"},
                world_time=current_tick,
                actor_id=actor_id,
            )
            _charge(
                ledger,
                runtime,
                instance,
                branch,
                before=before,
                keys=(world_budget, actor_key),
                requested_lod=lod_states[actor_id].level,
            )

            before = state_storage_bytes(runtime.current_state(instance, branch))
            _commit(
                runtime,
                instance,
                branch,
                command_id=f"g92h_memory_{day:02d}_{actor_index}",
                action_type="epistemic.record_observation",
                payload={
                    "memory_id": f"g92h_memory_{actor_index}_{day:02d}",
                    "actor_id": actor_id,
                    "content_ref": f"memory://g92h/{actor_id}/day-{day:02d}",
                    "at_ticks": current_tick,
                    "salience": 0.5,
                    "source_obs_ref": f"observation://g92h/{actor_id}/{day:02d}",
                },
                world_time=current_tick,
                actor_id=actor_id,
            )
            _charge(
                ledger,
                runtime,
                instance,
                branch,
                before=before,
                keys=(world_budget, actor_key),
                requested_lod=lod_states[actor_id].level,
            )

        runtime.create_checkpoint(instance, branch)
        checkpoint_count += 1
        checkpoint_service.checkpoint(
            "run-g92h-literary",
            instance.value,
            branch.value,
            scheduler,
            state_hash=runtime.current_state(instance, branch).semantic_hash(),
            event_head=len(runtime.events(instance, branch)),
        )

        if day in (1, 7, HORIZON_DAYS):
            state = runtime.current_state(instance, branch)
            replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(
                runtime.events(instance, branch)
            )
            recovery = runtime.restore_and_replay(instance, branch)
            qualification.record(
                HorizonSample(
                    "24h" if day == 1 else "7d" if day == 7 else "30d",
                    current_tick,
                    TemporalQuery(state).now(),
                    (alice_id, bob_id),
                    len(runtime.events(instance, branch)),
                    checkpoint_count,
                    state_storage_bytes(state),
                    replayed.semantic_hash(),
                    recovery.state.semantic_hash(),
                )
            )

        if day == 15:
            left = playable.leave(instance.value, viewer_id=OWNER)
            continued = playable.continue_instance(instance.value, viewer_id=OWNER)
            assert left["status"] == "left"
            assert cast(dict[str, object], continued["instance"])["instance_id"] == instance.value
            assert cast(dict[str, object], continued["instance"])["branch_id"] == branch.value

    report = qualification.finish()
    assert report.qualified is True
    assert {sample.label for sample in report.samples} == {"24h", "7d", "30d"}
    assert report.storage_bytes_growth > 0
    assert "L4" in lod_levels
    assert (
        len(
            EpistemicQuery(
                runtime.current_state(instance, branch), now_ticks=HORIZON_DAYS * DAY
            ).memories(EntityId(alice_id))
        )
        == HORIZON_DAYS
    )
    assert (
        len(
            EpistemicQuery(
                runtime.current_state(instance, branch), now_ticks=HORIZON_DAYS * DAY
            ).memories(EntityId(bob_id))
        )
        == HORIZON_DAYS
    )
    assert state_storage_bytes(runtime.current_state(instance, branch)) > baseline_storage
    assert ledger.usage(world_budget).calls > 0
    assert ledger.usage(alice_budget).storage_bytes > 0
    assert ledger.usage(bob_budget).storage_bytes > 0

    # A failed publication leaves no checkpoint behind; the regular run store
    # above is therefore only populated by successful atomic publications.
    crash_scheduler = RecurringScheduler()
    crash_scheduler.add(RecurringSchedule("g92h_crash_probe", "probe", 1, 1, max_occurrences=1))
    crash_scheduler.advance_to(1)
    crash_store = RunCheckpointStore(CrashPlan((1,)))
    with pytest.raises(CheckpointCrash):
        LongRunCheckpointService(crash_store).checkpoint(
            "run-g92h-crash",
            instance.value,
            branch.value,
            crash_scheduler,
            state_hash=report.samples[-1].replay_hash,
            event_head=len(runtime.events(instance, branch)),
        )
    assert crash_store.latest("run-g92h-crash") is None

    resumed_scheduler = RecurringScheduler(availability=availability)
    for actor_id in (alice_id, bob_id):
        resumed_scheduler.add(
            RecurringSchedule(
                f"g92h_daily_{actor_id}",
                "set_status",
                DAY,
                DAY,
                actor_id=actor_id,
                payload=(("entity_id", actor_id), ("status", "active")),
            )
        )
    resumed = checkpoint_service.resume("run-g92h-literary", resumed_scheduler)
    assert resumed.scheduler_cursor == scheduler.cursor()

    restarted = make_world_runtime(persist_db_path, extra_resolvers=_register)
    restarted_state = restarted.restore_and_replay(instance, branch)
    final_state = runtime.current_state(instance, branch)
    assert restarted_state.state.semantic_hash() == final_state.semantic_hash()
    events = runtime.events(instance, branch)
    snapshot = runtime.create_checkpoint(instance, branch)
    manifest = CompactionService(
        CompactionPolicy(retain_recent_events=12, memory_summary_every_events=12)
    ).compact(
        events,
        snapshot,
        replay_hash_before=final_state.semantic_hash(),
        replay_hash_after=restarted_state.state.semantic_hash(),
    )
    assert manifest.compacted
    assert manifest.source_event_count == len(events)
    assert manifest.memory_summary_refs
    assert manifest.replay_hash == final_state.semantic_hash()
    print(
        "G92H_EVIDENCE "
        + json.dumps(
            {
                "package_id": authored.package.package_id,
                "instance_id": instance.value,
                "actors": [alice_id, bob_id],
                "days": HORIZON_DAYS,
                "ticks": HORIZON_DAYS * DAY,
                "events": len(events),
                "checkpoints": checkpoint_count,
                "storage_baseline": baseline_storage,
                "storage_final": state_storage_bytes(final_state),
                "memory_per_actor": HORIZON_DAYS,
                "memory_summaries": len(manifest.memory_summary_refs),
                "lod_levels": sorted(lod_levels),
                "world_calls": ledger.usage(world_budget).calls,
                "world_storage_bytes": ledger.usage(world_budget).storage_bytes,
                "replay_recovery_equal": report.replay_recovery_equal,
                "qualified": report.qualified,
            },
            sort_keys=True,
        )
    )
