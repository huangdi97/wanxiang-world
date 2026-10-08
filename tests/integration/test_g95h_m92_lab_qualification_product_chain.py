"""G95H: qualify one four-worldline literary laboratory experiment."""

from __future__ import annotations

import json
import pathlib
import uuid
from typing import cast

from tests.conftest import cleanup_db_file, make_world_runtime
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchId
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.reality.intervention import (
    ExperimentSetup,
    Intervention,
    InterventionTrigger,
)
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import (
    BatchRunResult,
    BatchWorldlineExecutor,
    ExperimentDefinition,
    ExperimentRegistry,
    ForkInterventionRunner,
    LabQualification,
    TrajectoryPoint,
    ValidationProfile,
    WorldLabQualifier,
    WorldlineComparator,
    WorldlineMeasurement,
    WorldRunArtifact,
)
from wanxiang_substrate.world_lab.registry_models import ExperimentRun


def _source() -> SourceRecord:
    content = (
        "# G95H literary source\nCharacter: Alice\nCharacter: Bob\n"
        "Alice kept watch at the gate.\nBob carried the letter.\n"
        "relationship: Alice -> Bob\nrule: witnesses remember shared events\n"
    )
    return SourceRecord(
        source_id="g95h_private_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g95h_private_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="g95h",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g95h",
        access="private",
    )


def _definition(package_id: str, package_version: str) -> ExperimentDefinition:
    return ExperimentDefinition(
        experiment_id="experiment:g95h:literary",
        version=1,
        world_package_ref=package_id,
        world_package_version=package_version,
        scenario_ref="scenario:g95h:literary",
        scenario_version="1",
        seeds=(5, 7),
        parameter_variants=(
            ("pressure", "high"),
            ("pressure", "low"),
        ),
        run_horizon=7,
        metrics=("event_count", "revision"),
        validation_profile_ref="validation:g95g:real-chain",
        owner_id="owner:g95h",
        rights_ref="rights:g95h:private-approved",
    )


def _artifact(
    run: ExperimentRun,
    package_id: str,
    profile: PlayableWorldProfile,
    state: InMemoryCanonicalState,
    events: tuple[CommittedEvent, ...],
    snapshot_id: str,
    branch_id: str,
) -> WorldRunArtifact:
    return WorldRunArtifact(
        artifact_id=f"artifact:{run.run_id}",
        world_package_ref=package_id,
        world_package_version="1.0.0",
        scenario_ref=profile.scenario_ref,
        scenario_version=str(profile.version),
        constitution_version="1",
        runtime_profile_ref=profile.runtime_profile_ref,
        provider_versions=(("deterministic", "1"),),
        seed=run.seed,
        commit_refs=tuple(event.event_id.value for event in events),
        snapshot_refs=(snapshot_id,),
        branch_refs=(branch_id,),
        actor_trajectory_refs=(("world", state.semantic_hash()),),
        validation_results=(("V0", "pass"),),
        metrics=(
            ("event_count", float(len(events))),
            ("revision", float(state.revision.value)),
        ),
        privacy_metadata=(("visibility", "private"),),
        redacted_fields=("source_payload",),
    ).with_hash()


def test_m92_qualifies_batch_intervention_comparison_and_artifacts(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    authored = OneClickAuthoring().run("job_g95h", (source,), profile="book")
    definition = _definition(authored.package.package_id, str(authored.package.manifest.version))
    registry = ExperimentRegistry()
    registry.register(definition)
    executor = BatchWorldlineExecutor(registry, max_parallelism=1)
    plan = executor.enqueue(definition.experiment_id, batch_id="batch:g95h:literary")
    artifacts: dict[str, WorldRunArtifact] = {}

    def worker(run: ExperimentRun) -> BatchRunResult:
        variant = str(dict(run.parameters)["pressure"])
        db_path = persist_db_path.with_name(f"g95h_{uuid.uuid4().hex}.db")
        try:
            runtime = make_world_runtime(db_path, extra_resolvers=register_preview_resolvers)
            playable = PlayableService(runtime)
            profile = playable.register_package(
                authored.package,
                owner_id="owner:g95h",
                visibility="private",
            )
            character = playable.entry.create_character(
                "owner:g95h",
                "Alice",
                compatible_profile_ids=(profile.experience_package_ref,),
                character_id=f"character_g95h_{run.seed}_{variant}",
            )
            entered = playable.enter(
                profile.profile_id,
                viewer_id="owner:g95h",
                mode="embodiment",
                session_id=f"session_g95h_{run.seed}_{variant}",
                character_id=character.character_id,
            )
            payload = cast(dict[str, object], entered["instance"])
            instance = WorldInstanceId(str(payload["instance_id"]))
            branch = BranchId(playable.store.get_instance(instance.value).branch_id)
            playable.action(
                instance.value,
                viewer_id="owner:g95h",
                action_type="set_status",
                payload={"entity_id": "ent_alice", "status": variant},
            )
            state = runtime.current_state(instance, branch)
            snapshot = runtime.create_checkpoint(instance, branch)
            events = runtime.events(instance, branch)
            artifact = _artifact(
                run,
                authored.package.package_id,
                profile,
                state,
                events,
                snapshot.snapshot_id.value,
                branch.value,
            )
            artifacts[run.run_id] = artifact
            assert artifact.verify_hash()
            assert runtime.restore_and_replay(instance, branch).state.semantic_hash() == (
                state.semantic_hash()
            )
            return BatchRunResult(
                run_id=run.run_id,
                seed=run.seed,
                parameters=run.parameters,
                worldline_ref=f"worldline:g95h:{run.seed}:{variant}",
                artifact_ref=artifact.artifact_id,
                checkpoint_ref=snapshot.snapshot_id.value,
                metrics=(
                    ("event_count", float(len(events))),
                    ("revision", float(state.revision.value)),
                ),
            )
        finally:
            cleanup_db_file(db_path)

    execution = executor.execute(plan, worker)
    assert execution.aggregate.failed_runs == 0, execution.results
    measurements = tuple(
        WorldlineMeasurement(
            worldline_id=result.run_id,
            worldline_ref=result.worldline_ref,
            artifact_ref=result.artifact_ref,
            alignment_ref=f"alignment:{authored.package.package_id}",
            points=(
                TrajectoryPoint("actor", "alice.revision", 7, float(result.seed)),
                TrajectoryPoint("relation", "alice_bob.edge", 7, 1.0),
                TrajectoryPoint("institution", "community.active", 7, 1.0),
                TrajectoryPoint(
                    "macro", "world.event_count", 7, dict(result.metrics)["event_count"]
                ),
                TrajectoryPoint("cost", "calls", 7, dict(result.metrics)["event_count"] + 1),
            ),
            seed=result.seed,
            parameters=result.parameters,
        )
        for result in execution.results
    )
    comparison = WorldlineComparator().compare(measurements)

    intervention_runtime = make_world_runtime(
        persist_db_path,
        extra_resolvers=register_preview_resolvers,
    )
    playable = PlayableService(intervention_runtime)
    profile = playable.register_package(
        authored.package,
        owner_id="owner:g95h",
        visibility="private",
    )
    character = playable.entry.create_character(
        "owner:g95h",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g95h_intervention",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="owner:g95h",
        mode="embodiment",
        session_id="session_g95h_intervention",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    parent = BranchId(playable.store.get_instance(instance.value).branch_id)
    parent_events = intervention_runtime.events(instance, parent)
    intervention = Intervention(
        intervention_id="intervention:g95h:pressure",
        kind="pressure",
        trigger=InterventionTrigger.on_event(parent_events[0].event_id.value),
        parent_branch_ref=parent.value,
        artifact_ref="artifact:g95h:intervention",
    )
    setup = ExperimentSetup(
        setup_id="setup:g95h",
        baseline_instance_ref=instance.value,
        baseline_branch_ref=parent.value,
        artifact_ref="artifact:g95h:setup",
    ).add(intervention)
    intervention_runner = ForkInterventionRunner()
    forked = intervention_runner.fork(
        intervention_runtime,
        instance,
        parent,
        setup,
        intervention,
    )
    resumed = intervention_runner.resume(
        intervention_runtime,
        forked,
        expected_revision=forked.provenance.fork_revision,
    )

    qualification = WorldLabQualifier().qualify(
        qualification_id="qualification:g95h:m92",
        experiment_ref=definition.experiment_id,
        source_profile="literary",
        validation_profile_ref=ValidationProfile("validation:g95g:real-chain", 1).profile_id,
        batch=execution,
        intervention_runs=(resumed,),
        comparison=comparison,
        artifacts=tuple(artifacts.values()),
    )
    exported = json.dumps(qualification.to_dict(), ensure_ascii=False, sort_keys=True)
    restored = LabQualification.from_dict(qualification.to_dict())

    assert len(execution.results) == 4
    assert execution.aggregate.completed_runs == 4
    assert comparison.qualified is True
    assert resumed.status == "resumed"
    assert intervention_runtime.events(instance, parent) == parent_events
    assert qualification.qualified is True
    assert qualification.overall_status == "pass"
    assert restored == qualification
    assert source.payload not in exported
    assert "G95H literary source" not in exported
