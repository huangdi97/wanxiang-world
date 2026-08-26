"""G95D: a real private source produces a reproducible batch of worldlines."""

from __future__ import annotations

import json
import pathlib
import uuid
from typing import cast

from tests.conftest import cleanup_db_file, make_world_runtime
from wanxiang_domain.hierarchy import BranchId
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import (
    BatchRunResult,
    BatchWorldlineExecutor,
    ExperimentDefinition,
    ExperimentRegistry,
    WorldRunArtifact,
)
from wanxiang_substrate.world_lab.registry_models import ExperimentRun


def _source() -> SourceRecord:
    content = "# G95D source\nCharacter: Alice\nrule: each run keeps a ledger\n"
    return SourceRecord(
        source_id="g95d_private_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g95d_private_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="g95d",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g95d",
        access="private",
    )


def _definition() -> ExperimentDefinition:
    return ExperimentDefinition(
        experiment_id="experiment:g95d:product",
        version=1,
        world_package_ref="world:g95d:product",
        world_package_version="1",
        scenario_ref="scenario:g95d:product",
        scenario_version="1",
        seeds=(5, 7),
        parameter_variants=(("pressure", "high"), ("pressure", "low")),
        owner_id="owner:g95d",
        rights_ref="rights:g95d:private-approved",
    )


def test_real_product_chain_runs_seed_parameter_batch_with_sanitized_evidence(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    authored = OneClickAuthoring().run("job_g95d", (source,), profile="book")
    registry = ExperimentRegistry()
    registry.register(_definition())
    executor = BatchWorldlineExecutor(registry, max_parallelism=1)
    plan = executor.enqueue("experiment:g95d:product", batch_id="batch:g95d:product")

    def worker(run: ExperimentRun) -> BatchRunResult:
        variant = str(dict(run.parameters)["pressure"])
        db_path = persist_db_path.with_name(f"g95d_{uuid.uuid4().hex}.db")
        try:
            runtime = make_world_runtime(db_path, extra_resolvers=register_preview_resolvers)
            playable = PlayableService(runtime)
            profile = playable.register_package(
                authored.package,
                owner_id="owner:g95d",
                visibility="private",
            )
            character = playable.entry.create_character(
                "owner:g95d",
                "Alice",
                compatible_profile_ids=(profile.experience_package_ref,),
                character_id=f"character_g95d_{run.seed}_{variant}",
            )
            entered = playable.enter(
                profile.profile_id,
                viewer_id="owner:g95d",
                mode="embodiment",
                session_id=f"session_g95d_{run.seed}_{variant}",
                character_id=character.character_id,
            )
            payload = cast(dict[str, object], entered["instance"])
            instance = WorldInstanceId(str(payload["instance_id"]))
            branch = BranchId(playable.store.get_instance(instance.value).branch_id)
            playable.action(
                instance.value,
                viewer_id="owner:g95d",
                action_type="set_status",
                payload={"entity_id": "ent_alice", "status": variant},
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
                provider_versions=(("deterministic", "1"),),
                seed=run.seed,
                commit_refs=tuple(event.event_id.value for event in events),
                snapshot_refs=(snapshot.snapshot_id.value,),
                branch_refs=(branch.value,),
                actor_trajectory_refs=((f"actor:alice:{variant}", state.semantic_hash()),),
                validation_results=(("V0", "pass"),),
                metrics=(
                    ("event_count", float(len(events))),
                    ("revision", float(state.revision.value)),
                ),
                privacy_metadata=(("visibility", "private"),),
                redacted_fields=("source_payload",),
            ).with_hash()
            assert artifact.verify_hash()
            assert runtime.restore_and_replay(instance, branch).state.semantic_hash() == (
                state.semantic_hash()
            )
            return BatchRunResult(
                run_id=run.run_id,
                seed=run.seed,
                parameters=run.parameters,
                worldline_ref=f"worldline:{instance.value}",
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
    exported = json.dumps(execution.to_dict(), ensure_ascii=False, sort_keys=True)

    assert len(execution.results) == 4
    assert execution.aggregate.completed_runs == 4
    assert execution.aggregate.failed_runs == 0
    assert execution.aggregate.metric("event_count") is not None
    assert execution.checkpoint.completed_run_ids == plan.run_ids
    assert source.payload not in exported
    assert tuple(
        sorted((item.seed, dict(item.parameters)["pressure"]) for item in execution.results)
    ) == (
        (5, "high"),
        (5, "low"),
        (7, "high"),
        (7, "low"),
    )
