"""G97C: family/structured source uses the shared long-run substrate."""

from __future__ import annotations

import json
import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_application.world_runtime import SubmitCommandResult, WorldRuntime
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
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

DAY = 100
HORIZON_DAYS = 30
OWNER = "g97c_owner"


def _source() -> SourceRecord:
    content = (
        "0 HEAD\n1 SOUR G97C\n"
        "0 @I1@ INDI\n1 NAME Alice /Doe/\n1 BIRT\n2 DATE 1980\n2 PLAC Harbor\n"
        "0 @I2@ INDI\n1 NAME Bob /Doe/\n1 BIRT\n2 DATE 1982\n2 PLAC Harbor\n"
        "0 @I3@ INDI\n1 NAME Carol /Doe/\n1 BIRT\n2 DATE 2005\n2 PLAC Harbor\n"
        "0 @F1@ FAM\n1 HUSB @I1@\n1 WIFE @I2@\n1 CHIL @I3@\n0 TRLR\n"
    )
    return SourceRecord(
        source_id="g97c_family_source",
        kind="gedcom",
        content_hash=payload_hash(content),
        content_ref="memory://g97c_family_source",
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
        provenance="synthetic:g97c",
        access="public",
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
) -> SubmitCommandResult:
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
    decision = ledger.admit(
        keys,
        CostUsage(calls=1, time_ms=1, storage_bytes=max(0, after - before)),
        requested_lod=requested_lod,
    )
    assert decision.status == "accepted"


def _scheduler(actor_pair: tuple[str, str]) -> RecurringScheduler:
    availability = ActorAvailability(
        tuple(AvailabilityWindow(actor_id, DAY, HORIZON_DAYS * DAY + 1) for actor_id in actor_pair)
    )
    scheduler = RecurringScheduler(availability=availability)
    for actor_id in actor_pair:
        scheduler.add(
            RecurringSchedule(
                schedule_id=f"g97c_daily_{actor_id}",
                action="set_status",
                start_tick=DAY,
                interval_ticks=DAY,
                actor_id=actor_id,
                payload=(("entity_id", actor_id), ("status", "active")),
                max_occurrences=HORIZON_DAYS,
            )
        )
    return scheduler


@pytest.mark.integration
def test_family_world_uses_shared_long_run_without_literary_path(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    authoring = OneClickAuthoring()
    authored = authoring.run("job_g97c_family", (source,), profile="family")
    assert authored.source_profile == "family"
    assert authored.package.evidence_coverage > 0.0
    assert authoring.publish(authored).publish_ok is True

    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(authored.package, owner_id=OWNER, visibility="public")
    entry_name = "Alice Doe"
    character = playable.entry.create_character(
        OWNER,
        entry_name,
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g97c_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id=OWNER,
        mode="embodiment",
        session_id="session_g97c_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    actors = _actor_ids(runtime.current_state(instance, branch))
    assert set(actors) >= {"Alice Doe", "Bob Doe", "Carol Doe"}
    actor_pair = (actors["Alice Doe"], actors["Bob Doe"])

    entry_action = playable.action(
        instance.value,
        viewer_id=OWNER,
        action_type="set_status",
        payload={"entity_id": actor_pair[0], "status": "active"},
    )
    _commit(
        runtime,
        instance,
        branch,
        command_id="g97c_temporal_calendar",
        action_type="temporal.instantiate",
        payload={"fixture": "calendar", "version": 1},
        world_time=runtime.current_state(instance, branch).revision.value + 1,
    )

    world_budget = BudgetKey("world", instance.value)
    actor_budgets = tuple(BudgetKey("actor", actor_id) for actor_id in actor_pair)
    ledger = CostBudgetLedger()
    ledger.register(
        world_budget, CostLimit(max_calls=250, max_time_ms=250, max_storage_bytes=1_000_000)
    )
    for actor_budget in actor_budgets:
        ledger.register(
            actor_budget,
            CostLimit(max_calls=150, max_time_ms=150, max_storage_bytes=500_000),
        )

    scheduler = _scheduler(actor_pair)
    background = BackgroundSimulation(
        scheduler,
        BackgroundPolicy(
            RuntimeProfile(
                runtime_id="g97c-family-30d",
                time_scale=DAY,
                simulation_lod="L1",
                seed=9703,
            ),
            mode="accelerated",
        ),
        world_ref=instance.value,
        branch_ref=branch.value,
    )
    cursor = background.leave("session_g97c_detached")
    checkpoint_store = RunCheckpointStore()
    checkpoint_service = LongRunCheckpointService(checkpoint_store)
    qualification = HorizonQualification(
        "run-g97c-family",
        required_labels=("24h", "7d", "30d"),
    )
    lod_runtime = SimulationLODRuntime()
    lod_states = {
        actor_id: LODState(
            actor_id,
            "L0",
            f"world://{instance.value}/actor/{actor_id}",
            f"memory://{instance.value}/actor/{actor_id}/summary/0",
        )
        for actor_id in actor_pair
    }
    lod_levels: set[SimulationLevel] = set()
    baseline_storage = state_storage_bytes(runtime.current_state(instance, branch))
    checkpoint_count = 0
    parent_fork_hash = ""
    parent_fork_events: tuple[object, ...] = ()
    child_branch: BranchId | None = None

    for day in range(1, HORIZON_DAYS + 1):
        run = background.run_offline(cursor, elapsed_ticks=1)
        cursor = background.reenter(run)
        current_tick = day * DAY
        assert run.world_ticks_advanced == DAY
        assert len(run.occurrences) == 2
        assert all(item.available and item.due_tick == current_tick for item in run.occurrences)

        for actor_id in actor_pair:
            activity = ActorActivityInput(
                actor_id=actor_id,
                current_tick=current_tick,
                last_active_tick=DAY if actor_id == actor_pair[0] else 0,
                goal_urgency=0.8 if actor_id == actor_pair[0] and day == 1 else 0.0,
                interaction_rate=0.7 if actor_id == actor_pair[0] and day == 1 else 0.0,
                proximity=0.6 if actor_id == actor_pair[0] and day == 1 else 0.0,
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

        before = state_storage_bytes(runtime.current_state(instance, branch))
        _commit(
            runtime,
            instance,
            branch,
            command_id=f"g97c_clock_{day:02d}",
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

        for actor_index, actor_id in enumerate(actor_pair, start=1):
            actor_budget = actor_budgets[actor_index - 1]
            before = state_storage_bytes(runtime.current_state(instance, branch))
            _commit(
                runtime,
                instance,
                branch,
                command_id=f"g97c_status_{day:02d}_{actor_index}",
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
                keys=(world_budget, actor_budget),
                requested_lod=lod_states[actor_id].level,
            )

            before = state_storage_bytes(runtime.current_state(instance, branch))
            _commit(
                runtime,
                instance,
                branch,
                command_id=f"g97c_memory_{day:02d}_{actor_index}",
                action_type="epistemic.record_observation",
                payload={
                    "memory_id": f"g97c_memory_{actor_index}_{day:02d}",
                    "actor_id": actor_id,
                    "content_ref": f"memory://g97c/{actor_id}/day-{day:02d}",
                    "at_ticks": current_tick,
                    "salience": 0.5,
                    "source_obs_ref": f"observation://g97c/{actor_id}/{day:02d}",
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
                keys=(world_budget, actor_budget),
                requested_lod=lod_states[actor_id].level,
            )

        runtime.create_checkpoint(instance, branch)
        checkpoint_count += 1
        checkpoint_service.checkpoint(
            "run-g97c-family",
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
            recovered = runtime.restore_and_replay(instance, branch)
            qualification.record(
                HorizonSample(
                    "24h" if day == 1 else "7d" if day == 7 else "30d",
                    current_tick,
                    current_tick,
                    actor_pair,
                    len(runtime.events(instance, branch)),
                    checkpoint_count,
                    state_storage_bytes(state),
                    replayed.semantic_hash(),
                    recovered.state.semantic_hash(),
                )
            )

        if day == 15:
            left = playable.leave(instance.value, viewer_id=OWNER)
            continued = playable.continue_instance(instance.value, viewer_id=OWNER)
            assert left["status"] == "left"
            assert cast(dict[str, object], continued["instance"])["instance_id"] == instance.value

        if day == 20:
            parent_fork_hash = runtime.current_state(instance, branch).semantic_hash()
            parent_fork_events = runtime.events(instance, branch)
            child_branch = runtime.create_branch(instance, branch).branch_id
            _commit(
                runtime,
                instance,
                child_branch,
                command_id="g97c_child_branch_probe",
                action_type="set_status",
                payload={"entity_id": actor_pair[0], "status": "family-branch-only"},
                world_time=current_tick,
                actor_id=actor_pair[0],
            )
            assert runtime.current_state(instance, branch).semantic_hash() == parent_fork_hash
            assert runtime.events(instance, branch) == parent_fork_events
            assert (
                runtime.restore_and_replay(instance, child_branch).state.semantic_hash()
                == runtime.current_state(instance, child_branch).semantic_hash()
            )

    report = qualification.finish()
    assert report.qualified is True
    assert report.replay_recovery_equal is True
    assert report.storage_bytes_growth > 0
    assert {"L0", "L3", "L4"}.issubset(lod_levels)
    assert checkpoint_count == HORIZON_DAYS
    latest = checkpoint_store.latest("run-g97c-family")
    assert latest is not None
    assert latest.scheduler_cursor.current_tick == HORIZON_DAYS * DAY
    assert latest.event_head == len(runtime.events(instance, branch))

    resumed_scheduler = _scheduler(actor_pair)
    resumed = checkpoint_service.resume("run-g97c-family", resumed_scheduler)
    assert resumed.scheduler_cursor == resumed_scheduler.cursor()

    crash_scheduler = RecurringScheduler()
    crash_scheduler.add(RecurringSchedule("g97c_crash_probe", "probe", 1, 1, max_occurrences=1))
    crash_scheduler.advance_to(1)
    crash_store = RunCheckpointStore(CrashPlan((1,)))
    with pytest.raises(CheckpointCrash):
        LongRunCheckpointService(crash_store).checkpoint(
            "run-g97c-crash",
            instance.value,
            branch.value,
            crash_scheduler,
            state_hash=report.samples[-1].replay_hash,
            event_head=len(runtime.events(instance, branch)),
        )
    assert crash_store.latest("run-g97c-crash") is None

    final_state = runtime.current_state(instance, branch)
    assert (
        len(
            EpistemicQuery(final_state, now_ticks=HORIZON_DAYS * DAY).memories(
                EntityId(actor_pair[0])
            )
        )
        == HORIZON_DAYS
    )
    assert (
        len(
            EpistemicQuery(final_state, now_ticks=HORIZON_DAYS * DAY).memories(
                EntityId(actor_pair[1])
            )
        )
        == HORIZON_DAYS
    )
    assert state_storage_bytes(final_state) > baseline_storage
    assert ledger.usage(world_budget).calls > 0
    assert all(ledger.usage(key).storage_bytes > 0 for key in actor_budgets)

    restarted = make_world_runtime(persist_db_path, extra_resolvers=_register)
    restarted_state = restarted.restore_and_replay(instance, branch)
    assert restarted_state.state.semantic_hash() == final_state.semantic_hash()
    snapshot = runtime.create_checkpoint(instance, branch)
    manifest = CompactionService(
        CompactionPolicy(retain_recent_events=12, memory_summary_every_events=12)
    ).compact(
        runtime.events(instance, branch),
        snapshot,
        replay_hash_before=final_state.semantic_hash(),
        replay_hash_after=restarted_state.state.semantic_hash(),
    )
    assert manifest.compacted is True
    assert manifest.replay_hash == final_state.semantic_hash()
    assert manifest.memory_summary_refs
    assert child_branch is not None
    assert entry_action.event_id

    print(
        "G97C_EVIDENCE "
        + json.dumps(
            {
                "profile": authored.source_profile,
                "package_id": authored.package.package_id,
                "instance_id": instance.value,
                "actors": list(actor_pair),
                "horizon_days": HORIZON_DAYS,
                "world_ticks": HORIZON_DAYS * DAY,
                "events": len(runtime.events(instance, branch)),
                "checkpoints": checkpoint_count,
                "storage_baseline": baseline_storage,
                "storage_final": state_storage_bytes(final_state),
                "memory_per_actor": HORIZON_DAYS,
                "memory_summaries": len(manifest.memory_summary_refs),
                "lod_levels": sorted(lod_levels),
                "world_calls": ledger.usage(world_budget).calls,
                "world_storage_bytes": ledger.usage(world_budget).storage_bytes,
                "branch_isolated": True,
                "replay_recovery_equal": report.replay_recovery_equal,
                "qualified": report.qualified,
            },
            sort_keys=True,
        )
    )
