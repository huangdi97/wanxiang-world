"""G95B: registry metadata attaches to a real private playable run."""

from __future__ import annotations

import pathlib
from typing import cast

from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import (
    ExperimentDefinition,
    ExperimentRegistry,
    WorldRunArtifact,
)


def test_registry_run_refs_follow_real_product_chain(persist_db_path: pathlib.Path) -> None:
    content = (
        "# G95B private source\nCharacter: Alice\nCharacter: Bob\nrelationship: Alice -> Bob\n"
    )
    source = SourceRecord(
        source_id="g95b_private_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g95b_private_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="g95b",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g95b",
        access="private",
    )
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    playable = PlayableService(runtime)
    authored = OneClickAuthoring().run("job_g95b", (source,), profile="book")
    profile = playable.register_package(
        authored.package,
        owner_id="owner:g95b",
        visibility="private",
    )
    character = playable.entry.create_character(
        "owner:g95b",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g95b_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="owner:g95b",
        mode="embodiment",
        session_id="session:g95b",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    before = runtime.current_state(instance, branch).semantic_hash()
    action = playable.action(
        instance.value,
        viewer_id="owner:g95b",
        action_type="set_status",
        payload={"entity_id": "ent_alice", "status": "registered"},
    )
    state = runtime.current_state(instance, branch)
    snapshot = runtime.create_checkpoint(instance, branch)
    events = runtime.events(instance, branch)
    artifact = WorldRunArtifact(
        artifact_id="artifact:g95b:run",
        world_package_ref=authored.package.package_id,
        world_package_version=str(authored.package.manifest.version),
        scenario_ref=profile.scenario_ref,
        scenario_version=str(profile.version),
        constitution_version="1",
        runtime_profile_ref=profile.runtime_profile_ref,
        provider_versions=(("preview", "1"),),
        seed=7,
        commit_refs=tuple(event.event_id.value for event in events),
        snapshot_refs=(snapshot.snapshot_id.value,),
        branch_refs=(branch.value,),
        actor_trajectory_refs=(("actor:alice", state.semantic_hash()),),
        metrics=(("revision", float(action.revision)),),
    ).with_hash()
    registry = ExperimentRegistry()
    registry.register(
        ExperimentDefinition(
            experiment_id="experiment:g95b",
            version=1,
            world_package_ref=authored.package.package_id,
            world_package_version=str(authored.package.manifest.version),
            scenario_ref=profile.scenario_ref,
            scenario_version=str(profile.version),
            seeds=(7,),
            parameter_variants=(("mode", "private"),),
            owner_id="owner:g95b",
            rights_ref="rights:private-approved",
        )
    )
    run = registry.create_run(
        "experiment:g95b",
        seed=7,
        parameters=(("mode", "private"),),
    )
    claimed = registry.claim_run(run.run_id, worker_id="worker:g95b")
    completed = registry.complete_run(
        claimed.run_id,
        worker_id="worker:g95b",
        worldline_ref=f"worldline:{branch.value}",
        artifact_ref=artifact.artifact_id,
    )

    assert completed.status == "completed"
    assert completed.artifact_ref == artifact.artifact_id
    assert artifact.verify_hash() is True
    assert before != state.semantic_hash()
    assert (
        runtime.restore_and_replay(instance, branch).state.semantic_hash() == state.semantic_hash()
    )
