"""G91H: real playable-world qualification for M88 pressure/director paths."""

from __future__ import annotations

from typing import cast

from scripts.reference_runtime import build_reference_runtime
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.authoring.living_ports import LivingRuntimePort
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.store import ExperienceInstanceRecord
from wanxiang_substrate.reality.benchmark import PressureBehaviorBenchmark
from wanxiang_substrate.reality.canon_attractor import CanonAttractorPolicy, CanonConstraint
from wanxiang_substrate.reality.challenge import Opportunity, OpportunityLifecycle
from wanxiang_substrate.reality.director import DirectorPolicy, DirectorProposal
from wanxiang_substrate.reality.intervention import (
    ExperimentInterventionRunner,
    ExperimentSetup,
    Intervention,
    InterventionTrigger,
)
from wanxiang_substrate.reality.pressure import PressureProfile
from wanxiang_substrate.reality.quest import QuestProjectionAdapter
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# M88 qualification\nCharacter: Alice\nCharacter: Bob\n"
        "Alice arrived in Beijing in 1985.\nBob visited Beijing.\n"
        "relationship: Alice -> Bob\nrule: visitors register\n"
    )
    return SourceRecord(
        source_id="g91h_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g91h_source",
        stage="E3",
        rights=RightsEnvelope(owner="test", usage="test", approved=True),
        payload=content,
        provenance="synthetic:g91h",
        access="private",
    )


def test_m88_modes_pressure_opportunity_and_intervention_use_playable_chain() -> None:
    authored = OneClickAuthoring().run("job_g91h", (_source(),), profile="book")
    runtime = build_reference_runtime()
    playable = PlayableService(runtime)
    profile = playable.register_package(authored.package, owner_id="alice", visibility="public")
    character = playable.entry.create_character(
        "alice",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="alice",
        mode="embodiment",
        session_id="session_g91h",
        character_id=character.character_id,
    )
    instance_payload = cast(dict[str, object], entered["instance"])
    instance_id = str(instance_payload["instance_id"])
    record: ExperienceInstanceRecord = playable.store.get_instance(instance_id)
    instance = WorldInstanceId(instance_id)
    parent_branch = BranchId(record.branch_id)

    pressure = PressureProfile(
        profile_id=f"pressure:{profile.profile_id}",
        scenario_ref=profile.profile_id,
        domain_ref="literary-town",
        scarcity=0.6,
        goals=0.7,
        obligation=0.5,
        reward=0.4,
        risk=0.3,
        time=0.8,
        norm=0.7,
        source_refs=("scenario:qualification",),
    )
    benchmark = PressureBehaviorBenchmark().compare(pressure, seed=11, horizon_ticks=8)
    assert benchmark.same_seed and benchmark.same_profile and benchmark.repeatable

    canon = DirectorPolicy.for_mode("CANON")
    decision = canon.evaluate(DirectorProposal("proposal_g91h", "world", "opportunity"))
    assert decision.allowed is True
    switched = canon.transition("LIVING", at_ticks=1, reason="player entered living mode")
    assert switched.policy.mode == "LIVING"
    assert switched.audit.previous_mode == "CANON"

    opportunity = Opportunity(
        opportunity_id="opp_g91h_market",
        kind="resource",
        condition="market_open",
        score=0.8,
        at_ticks=1,
        eligibility=("actor:alice", "state:market"),
        available_from=1,
        expires_at=20,
        reward_refs=("reward:trust",),
        risk_refs=("risk:reputation",),
        evidence_refs=("event:market_trade",),
        world_state_refs=("state:market",),
    )
    lifecycle = OpportunityLifecycle()
    eligible = lifecycle.mark_eligible(
        opportunity, actor_id="alice", world_state_refs=("state:market",), at_ticks=1
    )
    ignored = lifecycle.ignore(lifecycle.offer(eligible, at_ticks=2), decision_ref="alice:ignored")
    assert ignored.status == "ignored"
    assert QuestProjectionAdapter().from_opportunity(ignored).status == "ignored"

    # A real playable actor action is committed through PlayableService before
    # the experiment fork. Director/Opportunity operations above do not alter it.
    action = playable.action(instance_id, viewer_id="alice", text="set status to awake")
    parent_before = runtime.current_state(instance, parent_branch).semantic_hash()
    parent_events_before = runtime.events(instance, parent_branch)
    attractor = CanonAttractorPolicy(
        (CanonConstraint("status", "status", 1.0, kind="soft", tolerance=0.2),)
    )
    assessment = attractor.assess("choice:awake", {"status": 1.0}, at_ticks=3)
    assert assessment.choice_preserved is True
    assert action.event_id

    intervention = Intervention(
        intervention_id="int_g91h",
        kind="pressure",
        trigger=InterventionTrigger.at_time(10),
        parent_branch_ref=parent_branch.value,
        artifact_ref="run-artifact:g91h",
        payload=(("profile_ref", pressure.profile_id),),
    )
    setup = ExperimentSetup(
        setup_id="setup_g91h",
        baseline_instance_ref=instance.value,
        baseline_branch_ref=parent_branch.value,
        artifact_ref="run-artifact:g91h",
    ).add(intervention)
    branch = ExperimentInterventionRunner().fork(
        cast(LivingRuntimePort, runtime), instance, parent_branch, setup, intervention
    )
    assert branch.isolated is True
    assert branch.branch_ref != parent_branch.value
    assert runtime.events(instance, parent_branch) == parent_events_before
    assert runtime.current_state(instance, parent_branch).semantic_hash() == parent_before
    replayed = runtime.restore_and_replay(instance, BranchId(branch.branch_ref))
    assert (
        replayed.state.semantic_hash()
        == runtime.current_state(instance, BranchId(branch.branch_ref)).semantic_hash()
    )
