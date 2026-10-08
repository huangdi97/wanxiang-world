"""G95G: real source-to-living runtime evidence feeds an independent profile."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_substrate.authoring.living_world import (
    evaluate_living_world,
    instantiate_living_world,
)
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.worldness import BoundedSimulation, WorldnessInput
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import (
    ValidationCheck,
    ValidationProfile,
    ValidationStack,
    WorldRunArtifact,
)


def _source() -> SourceRecord:
    content = (
        "# G95G private source\nCharacter: Alice\nCharacter: Bob\n"
        "Alice kept watch at the gate.\nBob carried the letter.\n"
        "relationship: Alice -> Bob\nrule: witnesses remember shared events\n"
    )
    return SourceRecord(
        source_id="g95g_private_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g95g_private_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="g95g",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g95g",
        access="private",
    )


def test_real_product_chain_emits_independent_v0_v7_report(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    authored = OneClickAuthoring().run("job_g95g", (source,), profile="book")
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    world, living = instantiate_living_world(runtime, authored.package, authored.preview)
    worldness_run, living_after = evaluate_living_world(runtime, world, authored.package, living)
    state = runtime.current_state(world.instance_id, world.branch_id)
    events = runtime.events(world.instance_id, world.branch_id)
    action = living_after.action
    trace_value = WorldnessInput(
        entity_count=len(authored.package.draft.entities),
        relation_count=len(authored.package.draft.relations),
        event_count=len(events),
        source_count=len(authored.package.draft.source_refs),
        uncertainty=authored.package.draft.uncertainty,
        replay_equal=bool(action and action.replay_equal),
        branch_isolated=worldness_run.branch_proof.isolated,
        draft_id=authored.package.draft_id,
        draft_revision=authored.package.draft_revision,
        source_refs=authored.package.draft.source_refs,
        domain_refs=tuple(item[0] for item in authored.package.domain_versions),
        completion_refs=authored.package.draft.completion_items,
        package_id=authored.package.package_id,
        provider_ids=("reference",),
        seed=95_07,
        evidence_coverage=authored.package.evidence_coverage,
        action_committed=bool(action and action.committed),
        action_evidence_refs=("runtime.commit", "runtime.replay") if action else (),
    )
    first_trace = BoundedSimulation().run(trace_value, branch_id=world.branch_id.value)
    replay_trace = BoundedSimulation().run(trace_value, branch_id=world.branch_id.value)
    source_fidelity = (
        authored.package.draft.source_refs == (source.source_id,)
        and dict(authored.package.source_versions).get(source.source_id) == source.version
    )
    structural = (
        authored.package.manifest.kind == "world"
        and authored.package.manifest.content_hash == authored.package.manifest.compute_hash()
        and bool(state.entities())
    )
    checks = (
        ValidationCheck(
            "V0",
            "pass" if structural else "fail",
            (
                "WorldPackage manifest and living entities were measured; "
                "Worldness remains a separate evidence surface"
            ),
            (authored.package.manifest.package_id, f"worldness:{worldness_run.score.overall:.6f}"),
            score=worldness_run.score.overall,
            measurements=(("entity_count", len(state.entities())),),
        ),
        ValidationCheck(
            "V1",
            "pass" if source_fidelity else "fail",
            "source identity and version pins remained unchanged through authoring",
            (f"source:{source.source_id}:{source.content_hash}",),
        ),
        ValidationCheck(
            "V2",
            "pass" if action is not None and action.committed and action.replay_equal else "fail",
            "a product-facade action committed and replayed to the same state",
            ("runtime.commit", "runtime.replay"),
        ),
        ValidationCheck(
            "V3",
            "pass" if events and bool(events[-1].delta.operations) else "fail",
            "the committed event contains validated state operations",
            (events[-1].event_id.value,) if events else (),
            measurements=(("event_count", len(events)),),
        ),
        ValidationCheck(
            "V4",
            "pass" if len(state.entities()) >= 2 and len(events) >= 1 else "fail",
            "macro counts were measured from the same living instance",
            ("runtime.state", "runtime.events"),
            measurements=(("entity_count", len(state.entities())), ("event_count", len(events))),
        ),
        ValidationCheck(
            "V5",
            "pass" if first_trace == replay_trace and len(first_trace.steps) == 7 else "fail",
            "bounded seven-day reference traces were deterministic",
            (f"trace:{first_trace.replay_hash}",),
            measurements=(("horizon_days", first_trace.horizon_days),),
        ),
        ValidationCheck(
            "V6",
            "pass"
            if worldness_run.branch_proof.isolated
            and worldness_run.parent_hash_after_probe != worldness_run.child_hash_after_probe
            else "fail",
            "counterfactual branch stayed isolated and diverged after its probe",
            tuple(f"branch:{item}" for item in worldness_run.branch_proof.branch_ids),
        ),
        ValidationCheck(
            "V7",
            "unknown",
            "no external calibration dataset is in scope for this private-source run",
        ),
    )
    profile = ValidationProfile("validation:g95g:real-chain", 1)
    worldness_ref = f"worldness:{authored.package.package_id}:{worldness_run.score.overall:.6f}"
    report = ValidationStack().evaluate(profile, checks, worldness_ref=worldness_ref)
    artifact = WorldRunArtifact(
        artifact_id="artifact:g95g:real-chain",
        world_package_ref=authored.package.package_id,
        world_package_version=str(authored.package.manifest.version),
        scenario_ref="scenario:g95g",
        scenario_version="1",
        constitution_version=authored.package.draft.constitution_ref or "constitution:default",
        runtime_profile_ref=living_after.runtime_profile,
        provider_versions=(("reference", "1.0.0"),),
        seed=trace_value.seed,
        commit_refs=tuple(event.event_id.value for event in events),
        snapshot_refs=(living_after.snapshot_id,),
        branch_refs=(world.branch_id.value,),
        actor_trajectory_refs=(("world", state.semantic_hash()),),
        validation_results=tuple((check.level, check.status) for check in report.checks),
        metrics=(("worldness_overall", worldness_run.score.overall), ("event_count", len(events))),
    ).with_hash()

    restored = type(report).from_dict(report.to_dict())
    api = ValidationStack().api_report(profile, report)
    assert authored.package.evidence_coverage > 0.0
    assert worldness_run.score.evidence
    assert report.complete is True
    assert report.overall_status == "unknown"
    assert report.accepted is False
    assert report.unknown_levels == ("V7",)
    assert restored == report
    assert artifact.verify_hash() is True
    assert "G95G private source" not in repr(api)
    assert "G95G private source" not in repr(artifact.to_dict())
