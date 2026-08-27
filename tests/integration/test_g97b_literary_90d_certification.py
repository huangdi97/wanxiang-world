"""G97B: selected literary world 30d/90d certification on real SQLite."""

from __future__ import annotations

import json
import pathlib
from dataclasses import replace
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
from wanxiang_substrate.actor_continuity.relationship_graph import RelationshipGraph
from wanxiang_substrate.actor_continuity.relationship_model import (
    RelationshipDimensions,
    RelationshipState,
)
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.epistemic.query import EpistemicQuery
from wanxiang_substrate.epistemic.resolver import register_epistemic_resolvers
from wanxiang_substrate.evolution.actor_evolution import ActorEvolutionTracker
from wanxiang_substrate.evolution.delta import EvolutionCommitPolicy, EvolutionProvenance
from wanxiang_substrate.evolution.persona_adaptation import (
    PersonaAdaptationPolicy,
    PersonaObservation,
    PersonaTraitState,
    propose_persona_adaptation,
    review_persona_adaptation,
)
from wanxiang_substrate.evolution.relationship_evolution import (
    RelationshipDeltaRule,
    RelationshipEvolutionEvent,
    apply_relationship_proposal,
    propose_relationship_evolution,
    relationship_behavior_feedback,
)
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
HORIZON_DAYS = 90
OWNER = "g97b_owner"
SAMPLE_DAYS = (1, 7, 30, 90)
DRIFT_DAYS = (30, 60, 90)


def _source() -> SourceRecord:
    content = (
        "# Literary Long Horizon\nCharacter: Alice\nCharacter: Bob\n"
        "Alice kept watch at the gate. Bob carried the letter.\n"
        "relationship: Alice -> Bob\nrule: witnesses remember shared events\n"
    )
    return SourceRecord(
        source_id="g97b_literary_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g97b_literary_source",
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
        provenance="synthetic:g97b",
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


def _scheduler(actor_ids: tuple[str, str]) -> RecurringScheduler:
    availability = ActorAvailability(
        tuple(AvailabilityWindow(actor_id, DAY, HORIZON_DAYS * DAY + 1) for actor_id in actor_ids)
    )
    scheduler = RecurringScheduler(availability=availability)
    for actor_id in actor_ids:
        scheduler.add(
            RecurringSchedule(
                schedule_id=f"g97b_daily_{actor_id}",
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
def test_selected_literary_world_certifies_30d_and_90d_with_drift_and_recovery(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    authored = OneClickAuthoring().run("job_g97b_literary", (source,), profile="book")
    assert authored.package.evidence_coverage > 0.0

    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(authored.package, owner_id=OWNER, visibility="private")
    character = playable.entry.create_character(
        OWNER,
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g97b_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id=OWNER,
        mode="embodiment",
        session_id="session_g97b_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    actors = _actor_ids(runtime.current_state(instance, branch))
    assert {"Alice", "Bob"}.issubset(actors)
    alice_id, bob_id = actors["Alice"], actors["Bob"]
    actor_pair = (alice_id, bob_id)
    assert profile.world_package_ref == authored.package.package_id

    entry_action = playable.action(
        instance.value,
        viewer_id=OWNER,
        action_type="set_status",
        payload={"entity_id": alice_id, "status": "active"},
    )
    _commit(
        runtime,
        instance,
        branch,
        command_id="g97b_temporal_calendar",
        action_type="temporal.instantiate",
        payload={"fixture": "calendar", "version": 1},
        world_time=runtime.current_state(instance, branch).revision.value + 1,
    )

    world_budget = BudgetKey("world", instance.value)
    alice_budget = BudgetKey("actor", alice_id)
    bob_budget = BudgetKey("actor", bob_id)
    ledger = CostBudgetLedger()
    ledger.register(
        world_budget, CostLimit(max_calls=600, max_time_ms=600, max_storage_bytes=2_000_000)
    )
    for actor_budget in (alice_budget, bob_budget):
        ledger.register(
            actor_budget,
            CostLimit(max_calls=400, max_time_ms=400, max_storage_bytes=1_000_000),
        )

    scheduler = _scheduler(actor_pair)
    background = BackgroundSimulation(
        scheduler,
        BackgroundPolicy(
            RuntimeProfile(
                runtime_id="g97b-selected-90d",
                time_scale=DAY,
                simulation_lod="L1",
                seed=9702,
            ),
            mode="accelerated",
        ),
        world_ref=instance.value,
        branch_ref=branch.value,
    )
    cursor = background.leave("session_g97b_detached")
    checkpoint_store = RunCheckpointStore()
    checkpoint_service = LongRunCheckpointService(checkpoint_store)
    qualification = HorizonQualification(
        "run-g97b-literary",
        required_labels=("24h", "7d", "30d", "90d"),
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
    status_refs: dict[tuple[str, int], str] = {}
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
                last_active_tick=DAY if actor_id == alice_id else 0,
                goal_urgency=0.8 if actor_id == alice_id and day == 1 else 0.0,
                interaction_rate=0.7 if actor_id == alice_id and day == 1 else 0.0,
                proximity=0.6 if actor_id == alice_id and day == 1 else 0.0,
            )
            score = lod_runtime.score(activity)
            transition = lod_runtime.transition(lod_states[actor_id], score)
            lod_states[actor_id] = replace(
                lod_states[actor_id],
                level=transition.to_level,
                memory_summary_ref=(f"memory://{instance.value}/actor/{actor_id}/summary/{day}"),
            )
            lod_levels.add(transition.to_level)

        before = state_storage_bytes(runtime.current_state(instance, branch))
        _commit(
            runtime,
            instance,
            branch,
            command_id=f"g97b_clock_{day:02d}",
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
            actor_budget = alice_budget if actor_id == alice_id else bob_budget
            before = state_storage_bytes(runtime.current_state(instance, branch))
            status = _commit(
                runtime,
                instance,
                branch,
                command_id=f"g97b_status_{day:02d}_{actor_index}",
                action_type="set_status",
                payload={"entity_id": actor_id, "status": "active"},
                world_time=current_tick,
                actor_id=actor_id,
            )
            if day in DRIFT_DAYS:
                status_refs[(actor_id, day)] = status.event.event_id.value
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
                command_id=f"g97b_memory_{day:02d}_{actor_index}",
                action_type="epistemic.record_observation",
                payload={
                    "memory_id": f"g97b_memory_{actor_index}_{day:02d}",
                    "actor_id": actor_id,
                    "content_ref": f"memory://g97b/{actor_id}/day-{day:02d}",
                    "at_ticks": current_tick,
                    "salience": 0.5,
                    "source_obs_ref": f"observation://g97b/{actor_id}/{day:02d}",
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
            "run-g97b-literary",
            instance.value,
            branch.value,
            scheduler,
            state_hash=runtime.current_state(instance, branch).semantic_hash(),
            event_head=len(runtime.events(instance, branch)),
        )

        if day in SAMPLE_DAYS:
            state = runtime.current_state(instance, branch)
            replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(
                runtime.events(instance, branch)
            )
            recovered = runtime.restore_and_replay(instance, branch)
            qualification.record(
                HorizonSample(
                    "24h" if day == 1 else "7d" if day == 7 else "30d" if day == 30 else "90d",
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

        if day == 45:
            parent_fork_hash = runtime.current_state(instance, branch).semantic_hash()
            parent_fork_events = runtime.events(instance, branch)
            child_branch = runtime.create_branch(instance, branch).branch_id
            child_before = runtime.current_state(instance, child_branch)
            assert child_before.semantic_hash() == parent_fork_hash
            _commit(
                runtime,
                instance,
                child_branch,
                command_id="g97b_child_branch_probe",
                action_type="set_status",
                payload={"entity_id": alice_id, "status": "branch-only"},
                world_time=current_tick,
                actor_id=alice_id,
            )
            assert runtime.current_state(instance, branch).semantic_hash() == parent_fork_hash
            assert runtime.events(instance, branch) == parent_fork_events
            assert runtime.current_state(instance, child_branch).semantic_hash() != parent_fork_hash
            assert (
                runtime.restore_and_replay(instance, child_branch).state.semantic_hash()
                == runtime.current_state(instance, child_branch).semantic_hash()
            )

        if day == 45:
            left = playable.leave(instance.value, viewer_id=OWNER)
            continued = playable.continue_instance(instance.value, viewer_id=OWNER)
            assert left["status"] == "left"
            assert cast(dict[str, object], continued["instance"])["instance_id"] == instance.value

    report = qualification.finish()
    assert report.qualified is True
    assert [sample.label for sample in report.samples] == ["24h", "7d", "30d", "90d"]
    assert report.storage_bytes_growth > 0
    assert report.replay_recovery_equal is True
    assert {"L0", "L3", "L4"}.issubset(lod_levels)
    assert checkpoint_count == HORIZON_DAYS
    latest = checkpoint_store.latest("run-g97b-literary")
    assert latest is not None
    assert latest.scheduler_cursor.current_tick == HORIZON_DAYS * DAY
    assert latest.event_head == len(runtime.events(instance, branch))

    resumed_scheduler = _scheduler(actor_pair)
    resumed = checkpoint_service.resume("run-g97b-literary", resumed_scheduler)
    assert resumed.scheduler_cursor == resumed_scheduler.cursor()

    crash_scheduler = RecurringScheduler()
    crash_scheduler.add(RecurringSchedule("g97b_crash_probe", "probe", 1, 1, max_occurrences=1))
    crash_scheduler.advance_to(1)
    crash_store = RunCheckpointStore(CrashPlan((1,)))
    with pytest.raises(CheckpointCrash):
        LongRunCheckpointService(crash_store).checkpoint(
            "run-g97b-crash",
            instance.value,
            branch.value,
            crash_scheduler,
            state_hash=report.samples[-1].replay_hash,
            event_head=len(runtime.events(instance, branch)),
        )
    assert crash_store.latest("run-g97b-crash") is None

    final_state = runtime.current_state(instance, branch)
    assert (
        len(EpistemicQuery(final_state, now_ticks=HORIZON_DAYS * DAY).memories(EntityId(alice_id)))
        == HORIZON_DAYS
    )
    assert (
        len(EpistemicQuery(final_state, now_ticks=HORIZON_DAYS * DAY).memories(EntityId(bob_id)))
        == HORIZON_DAYS
    )
    assert state_storage_bytes(final_state) > baseline_storage
    assert ledger.usage(world_budget).calls > 0
    assert ledger.usage(alice_budget).storage_bytes > 0
    assert ledger.usage(bob_budget).storage_bytes > 0

    canonical_hash_before_projection = final_state.semantic_hash()
    canonical_events_before_projection = runtime.events(instance, branch)
    relationship = RelationshipState(
        relationship_id="relationship_g97b_literary",
        source_actor_id=EntityId(alice_id),
        target_actor_id=EntityId(bob_id),
        relation_type="gate-partners",
        dimensions=RelationshipDimensions(),
        valid_from=0,
        event_refs=(entry_action.event_id,),
    )
    relationship_graph, _ = RelationshipGraph().add(
        relationship,
        event_ref=entry_action.event_id,
        at_ticks=0,
        reason="source-created relationship baseline",
    )
    actor_tracker = ActorEvolutionTracker(EntityId(alice_id), seed=9702)
    actor_baseline = actor_tracker.state
    provenance = EvolutionProvenance(
        origin_ref=f"package:{authored.package.package_id}",
        source_refs=(source.content_ref,),
        event_refs=(entry_action.event_id,),
        producer="runtime_projection",
    )
    persona_proposal = propose_persona_adaptation(
        proposal_id="g97b_persona",
        current=PersonaTraitState(actor_id=EntityId(alice_id), trait="caution"),
        observations=tuple(
            PersonaObservation(
                observation_id=f"g97b_caution_{day}",
                actor_id=EntityId(alice_id),
                trait="caution",
                direction="increase",
                strength=0.6,
                at_ticks=day * DAY,
                event_ref=status_refs[(alice_id, day)],
            )
            for day in DRIFT_DAYS
        ),
        now_ticks=HORIZON_DAYS * DAY,
        provenance=provenance,
        policy=PersonaAdaptationPolicy(
            window_ticks=HORIZON_DAYS * DAY,
            minimum_observations=3,
            minimum_span_ticks=100,
            maximum_abs_change=0.1,
        ),
    )
    persona_approved = review_persona_adaptation(persona_proposal, reviewer="policy", approved=True)
    actor_evolved = actor_tracker.apply_persona(
        persona_approved.persona_delta,
        provenance_ref=status_refs[(alice_id, HORIZON_DAYS)],
    )
    EvolutionCommitPolicy.validate_proposal(persona_approved.persona_delta)

    for day in DRIFT_DAYS:
        current_relationship = relationship_graph.state(relationship.relationship_id)
        assert current_relationship is not None
        evolution_event = RelationshipEvolutionEvent(
            event_ref=status_refs[(alice_id, day)],
            relationship_id=relationship.relationship_id,
            source_actor_id=EntityId(alice_id),
            target_actor_id=EntityId(bob_id),
            signal="shared_aid",
            strength=0.8,
            at_ticks=day * DAY,
            evidence_refs=(source.content_ref,),
        )
        proposal = propose_relationship_evolution(
            proposal_id=f"g97b_relationship_{day}",
            state=current_relationship,
            event=evolution_event,
            rules=(RelationshipDeltaRule("shared_aid", "trust", 0.5, maximum_step=0.2),),
            provenance=provenance,
        )
        EvolutionCommitPolicy.validate_proposal(proposal.delta)
        relationship_graph, _ = apply_relationship_proposal(
            relationship_graph, replace(proposal, approved=True)
        )

    relationship_after = relationship_graph.state(relationship.relationship_id)
    assert relationship_after is not None
    feedback = relationship_behavior_feedback(relationship_after, at_ticks=HORIZON_DAYS * DAY)
    assert feedback.cooperation_bias > 0.0
    assert actor_evolved.persona_hash() != actor_baseline.persona_hash()
    assert relationship_after != relationship
    assert RelationshipGraph.replay(relationship_graph.revisions) == relationship_graph
    assert (
        runtime.current_state(instance, branch).semantic_hash() == canonical_hash_before_projection
    )
    assert runtime.events(instance, branch) == canonical_events_before_projection
    assert source.payload == _source().payload
    assert source.content_hash == _source().content_hash

    restarted = make_world_runtime(persist_db_path, extra_resolvers=_register)
    restarted_state = restarted.restore_and_replay(instance, branch)
    assert restarted_state.state.semantic_hash() == final_state.semantic_hash()
    snapshot = runtime.create_checkpoint(instance, branch)
    manifest = CompactionService(
        CompactionPolicy(retain_recent_events=24, memory_summary_every_events=24)
    ).compact(
        runtime.events(instance, branch),
        snapshot,
        replay_hash_before=final_state.semantic_hash(),
        replay_hash_after=restarted_state.state.semantic_hash(),
    )
    assert manifest.compacted is True
    assert manifest.source_event_count == len(canonical_events_before_projection)
    assert manifest.memory_summary_refs
    assert manifest.replay_hash == final_state.semantic_hash()
    assert child_branch is not None

    print(
        "G97B_EVIDENCE "
        + json.dumps(
            {
                "package_id": authored.package.package_id,
                "instance_id": instance.value,
                "branch_id": branch.value,
                "child_branch_id": child_branch.value,
                "source_actors": list(actor_pair),
                "sample_days": list(SAMPLE_DAYS),
                "world_ticks": HORIZON_DAYS * DAY,
                "events": len(canonical_events_before_projection),
                "checkpoints": checkpoint_count,
                "storage_baseline": baseline_storage,
                "storage_final": state_storage_bytes(final_state),
                "memory_per_actor": HORIZON_DAYS,
                "memory_summaries": len(manifest.memory_summary_refs),
                "lod_levels": sorted(lod_levels),
                "world_calls": ledger.usage(world_budget).calls,
                "world_storage_bytes": ledger.usage(world_budget).storage_bytes,
                "relationship_revisions": len(relationship_graph.revisions),
                "relationship_trust": relationship_after.dimensions.trust,
                "persona_changed": actor_evolved.persona_hash() != actor_baseline.persona_hash(),
                "replay_recovery_equal": report.replay_recovery_equal,
                "qualified": report.qualified,
            },
            sort_keys=True,
        )
    )
