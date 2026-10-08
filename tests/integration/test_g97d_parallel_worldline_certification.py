"""G97D: certify parallel, multi-provider worldlines with complete evidence."""

from __future__ import annotations

import json
import pathlib
import threading
import uuid
from typing import cast

from tests.conftest import cleanup_db_file, make_world_runtime
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import BranchId
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.providers import ProviderCapability, ReferenceProvider
from wanxiang_substrate.capability.runtime_control import RuntimeControlLedger
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import (
    METRIC_CATEGORIES,
    BatchRunResult,
    BatchWorldlineExecutor,
    ExperimentDefinition,
    ExperimentRegistry,
    MultiProviderRun,
    MultiProviderWorldlineRunner,
    ProviderAssignmentPolicy,
    ProviderRunInput,
    TrajectoryPoint,
    WorldlineComparator,
    WorldlineMeasurement,
    WorldRunArtifact,
)
from wanxiang_substrate.world_lab.registry_models import ExperimentRun


def _source() -> SourceRecord:
    content = (
        "# G97D private parallel source\n"
        "Character: Alice\n"
        "Character: Bob\n"
        "relationship: Alice -> Bob\n"
    )
    return SourceRecord(
        source_id="g97d_private_parallel_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g97d_private_parallel_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="g97d",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g97d",
        access="private",
    )


def _definition() -> ExperimentDefinition:
    return ExperimentDefinition(
        experiment_id="experiment:g97d:parallel",
        version=1,
        world_package_ref="world:g97d:parallel",
        world_package_version="1",
        scenario_ref="scenario:g97d:parallel",
        scenario_version="1",
        seeds=(9704, 9705),
        parameter_variants=(
            ("provider_policy", "forward"),
            ("provider_policy", "reverse"),
        ),
        provider_matrix=(
            ("provider:g97d:alpha", "1.0.0"),
            ("provider:g97d:beta", "1.0.0"),
        ),
        population_policy="explicit-two-provider",
        run_horizon=1,
        metrics=METRIC_CATEGORIES,
        validation_profile_ref="validation:g97d:parallel",
        owner_id="owner:g97d",
        rights_ref="rights:g97d:private-approved",
    )


def _policy(policy_name: str) -> ProviderAssignmentPolicy:
    if policy_name == "forward":
        assignments = (
            ("actor:alice", "provider:g97d:alpha"),
            ("actor:bob", "provider:g97d:beta"),
        )
    else:
        assignments = (
            ("actor:alice", "provider:g97d:beta"),
            ("actor:bob", "provider:g97d:alpha"),
        )
    return ProviderAssignmentPolicy(
        policy_id=f"policy:g97d:{policy_name}",
        version=1,
        mode="explicit",
        provider_ids=("provider:g97d:alpha", "provider:g97d:beta"),
        explicit_assignments=assignments,
    )


def _measurement(
    run: ExperimentRun,
    artifact: WorldRunArtifact,
    *,
    revision: int,
    event_count: int,
    provider_count: int,
    policy_signal: float,
    alignment_ref: str,
) -> WorldlineMeasurement:
    return WorldlineMeasurement(
        worldline_id=run.run_id,
        worldline_ref=f"worldline:{run.run_id}",
        artifact_ref=artifact.artifact_id,
        alignment_ref=alignment_ref,
        points=(
            TrajectoryPoint("actor", "alice.revision", 1, float(revision)),
            TrajectoryPoint("relation", "provider.assignment", 1, policy_signal),
            TrajectoryPoint("institution", "provider.count", 1, float(provider_count)),
            TrajectoryPoint("macro", "world.event_count", 1, float(event_count)),
            TrajectoryPoint("cost", "worldline.seed", 1, float(run.seed)),
        ),
        seed=run.seed,
        parameters=run.parameters,
    )


def test_four_parallel_worldlines_use_same_initial_state_and_complete_evidence(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    authored = OneClickAuthoring().run("job_g97d", (source,), profile="book")
    registry = ExperimentRegistry()
    definition = _definition()
    registry.register(definition)
    executor = BatchWorldlineExecutor(registry, max_parallelism=4)
    plan = executor.enqueue("experiment:g97d:parallel", batch_id="batch:g97d:parallel")

    # Migrations are prepared serially because SQLite/Alembic initialization is
    # an environment concern; the four product-chain executions are concurrent.
    runtime_paths: dict[str, pathlib.Path] = {}
    runtimes: dict[str, WorldRuntime] = {}
    try:
        for run_id in plan.run_ids:
            path = persist_db_path.with_name(f"g97d_{uuid.uuid4().hex}.db")
            runtime_paths[run_id] = path
            runtimes[run_id] = make_world_runtime(
                path,
                extra_resolvers=register_preview_resolvers,
            )

        initial_hashes: dict[str, str] = {}
        final_hashes: dict[str, str] = {}
        events_before_provider: dict[str, tuple[CommittedEvent, ...]] = {}
        events_after_provider: dict[str, tuple[CommittedEvent, ...]] = {}
        provider_runs: dict[str, MultiProviderRun] = {}
        provider_input_exports: dict[str, dict[str, object]] = {}
        artifacts: dict[str, WorldRunArtifact] = {}
        measurements: dict[str, WorldlineMeasurement] = {}
        worker_thread_ids: set[int] = set()
        lock = threading.Lock()
        barrier = threading.Barrier(len(plan.run_ids), timeout=30)
        alignment_ref = f"alignment:{authored.package.manifest.content_hash}"

        def worker(run: ExperimentRun) -> BatchRunResult:
            runtime = runtimes[run.run_id]
            policy_name = str(dict(run.parameters)["provider_policy"])
            playable = PlayableService(runtime)
            profile = playable.register_package(
                authored.package,
                owner_id="owner:g97d",
                visibility="private",
            )
            character = playable.entry.create_character(
                "owner:g97d",
                "Alice",
                compatible_profile_ids=(profile.experience_package_ref,),
                character_id=f"character_g97d_{run.seed}_{policy_name}",
            )
            entered = playable.enter(
                profile.profile_id,
                viewer_id="owner:g97d",
                mode="embodiment",
                session_id=f"session:g97d:{run.seed}:{policy_name}",
                character_id=character.character_id,
            )
            instance = WorldInstanceId(
                str(cast(dict[str, object], entered["instance"])["instance_id"])
            )
            branch = BranchId(playable.store.get_instance(instance.value).branch_id)
            initial_state = runtime.current_state(instance, branch)
            before_provider = runtime.events(instance, branch)
            input_data = ProviderRunInput(
                run_id=run.run_id,
                world_package_ref=authored.package.package_id,
                world_package_version=str(authored.package.manifest.version),
                scenario_ref=profile.scenario_ref,
                scenario_version=str(profile.version),
                source_refs=(source.content_ref,),
                population_refs=("actor:alice", "actor:bob"),
                seed=run.seed,
                parameters=run.parameters,
                payload=source.payload,
                private_source=True,
                control_timestamp="2026-08-27T00:00:00Z",
            )
            providers = {
                "provider:g97d:alpha": ReferenceProvider(
                    ProviderCapability(
                        "provider:g97d:alpha",
                        "semantic",
                        "1.0.0",
                        private_safe=True,
                    )
                ),
                "provider:g97d:beta": ReferenceProvider(
                    ProviderCapability(
                        "provider:g97d:beta",
                        "semantic",
                        "1.0.0",
                        private_safe=True,
                    )
                ),
            }
            provider_run = MultiProviderWorldlineRunner(
                providers,
                RuntimeControlLedger(),
            ).execute(input_data, _policy(policy_name))

            with lock:
                initial_hashes[run.run_id] = initial_state.semantic_hash()
                events_before_provider[run.run_id] = before_provider
                worker_thread_ids.add(threading.get_ident())
            # Every worker must be alive at the same execution barrier. This
            # makes max_parallelism=4 observable rather than a configuration claim.
            barrier.wait()
            after_provider = runtime.events(instance, branch)
            with lock:
                events_after_provider[run.run_id] = after_provider
            assert after_provider == before_provider

            action = playable.action(
                instance.value,
                viewer_id="owner:g97d",
                action_type="set_status",
                payload={
                    "entity_id": "ent_alice",
                    "status": f"g97d-{policy_name}-{run.seed}",
                },
            )
            state = runtime.current_state(instance, branch)
            snapshot = runtime.create_checkpoint(instance, branch)
            events = runtime.events(instance, branch)
            artifact = WorldRunArtifact(
                artifact_id=f"artifact:{run.run_id}",
                world_package_ref=authored.package.package_id,
                world_package_version=str(authored.package.manifest.version),
                scenario_ref=profile.scenario_ref,
                scenario_version=str(profile.version),
                constitution_version="1",
                runtime_profile_ref=profile.runtime_profile_ref,
                provider_versions=provider_run.provider_versions,
                seed=run.seed,
                control_ledger_refs=provider_run.control_transaction_ids,
                commit_refs=tuple(event.event_id.value for event in events),
                snapshot_refs=(snapshot.snapshot_id.value,),
                branch_refs=(branch.value,),
                actor_trajectory_refs=(("actor:alice", state.semantic_hash()),),
                validation_results=(
                    ("provider_output", "proposal_only"),
                    ("commit_authority", "normal_action"),
                ),
                metrics=(
                    ("event_count", float(len(events))),
                    ("provider_count", float(len(provider_run.invocations))),
                    ("revision", float(action.revision)),
                ),
                privacy_metadata=(("visibility", "private"),),
                redacted_fields=("source_payload",),
            ).with_hash()
            replayed = runtime.restore_and_replay(instance, branch)
            assert replayed.state.semantic_hash() == state.semantic_hash()
            policy_signal = 1.0 if policy_name == "forward" else 2.0
            measurement = _measurement(
                run,
                artifact,
                revision=state.revision.value,
                event_count=len(events),
                provider_count=len(provider_run.invocations),
                policy_signal=policy_signal,
                alignment_ref=alignment_ref,
            )
            with lock:
                final_hashes[run.run_id] = state.semantic_hash()
                provider_runs[run.run_id] = provider_run
                provider_input_exports[run.run_id] = input_data.to_dict()
                artifacts[run.run_id] = artifact
                measurements[run.run_id] = measurement
            return BatchRunResult(
                run_id=run.run_id,
                seed=run.seed,
                parameters=run.parameters,
                worldline_ref=measurement.worldline_ref,
                artifact_ref=artifact.artifact_id,
                checkpoint_ref=snapshot.snapshot_id.value,
                metrics=(
                    ("event_count", float(len(events))),
                    ("provider_count", float(len(provider_run.invocations))),
                    ("revision", float(action.revision)),
                ),
            )

        execution = executor.execute(plan, worker)
    finally:
        for path in runtime_paths.values():
            cleanup_db_file(path)

    assert all(result.status == "completed" for result in execution.results), [
        result.error for result in execution.results
    ]
    comparison_measurements = tuple(measurements[run_id] for run_id in plan.run_ids)
    comparison = WorldlineComparator().compare(comparison_measurements)
    report = WorldlineComparator().api_report(comparison, comparison_measurements)
    exported = json.dumps(
        {
            "execution": execution.to_dict(),
            "provider_inputs": provider_input_exports,
            "provider_runs": {key: value.to_dict() for key, value in provider_runs.items()},
            "artifacts": {key: value.to_dict() for key, value in artifacts.items()},
            "comparison": report,
        },
        ensure_ascii=False,
        sort_keys=True,
    )

    assert len(plan.run_ids) == 4
    assert len(execution.results) == 4
    assert all(result.status == "completed" for result in execution.results)
    assert execution.aggregate.completed_runs == 4
    assert execution.aggregate.failed_runs == 0
    assert execution.checkpoint.completed_run_ids == plan.run_ids
    assert len(worker_thread_ids) == 4
    assert len(initial_hashes) == 4
    assert len(set(initial_hashes.values())) == 1
    assert len(set(final_hashes.values())) >= 2
    assert all(artifact.verify_hash() for artifact in artifacts.values())
    assert all(len(artifact.commit_refs) >= 1 for artifact in artifacts.values())
    assert all(artifact.snapshot_refs for artifact in artifacts.values())
    assert all(artifact.branch_refs for artifact in artifacts.values())
    assert all(artifact.control_ledger_refs for artifact in artifacts.values())
    assert all(run.proposal_count == 2 for run in provider_runs.values())
    assert all(run.to_dict()["proposal_only"] is True for run in provider_runs.values())
    assert all(
        events_after_provider[run_id] == events_before_provider[run_id] for run_id in plan.run_ids
    )
    assert {
        tuple((item.member_ref, item.provider_id) for item in provider_runs[run_id].invocations)
        for run_id in plan.run_ids
    } == {
        (
            ("actor:alice", "provider:g97d:alpha"),
            ("actor:bob", "provider:g97d:beta"),
        ),
        (
            ("actor:alice", "provider:g97d:beta"),
            ("actor:bob", "provider:g97d:alpha"),
        ),
    }
    assert comparison.aligned is True
    assert comparison.qualified is True
    assert len(comparison.worldline_ids) == 4
    assert any(item.absolute_delta > 0 for item in comparison.differences)
    assert {item.category for item in comparison.categories} == set(METRIC_CATEGORIES)
    series = report["series"]
    assert isinstance(series, list)
    assert len(cast(list[object], series)) == 4
    assert source.payload not in exported
    assert "G97D private parallel source" not in exported
