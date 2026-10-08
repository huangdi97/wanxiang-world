"""G95F: compare real private-source worldline evidence across all metric planes."""

from __future__ import annotations

import pathlib
from typing import cast

from tests.conftest import make_world_runtime
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import (
    TrajectoryPoint,
    WorldlineComparator,
    WorldlineMeasurement,
    WorldRunArtifact,
)


def _measurement(
    worldline_id: str,
    artifact: WorldRunArtifact,
    revision: int,
    event_count: int,
    *,
    alignment_ref: str,
) -> WorldlineMeasurement:
    points = (
        TrajectoryPoint("actor", "alice.revision", 30, float(revision)),
        TrajectoryPoint("relation", "alice_bob.edge", 30, float(event_count > 0)),
        TrajectoryPoint("institution", "community.active", 30, 1.0),
        TrajectoryPoint("macro", "world.event_count", 30, float(event_count)),
        TrajectoryPoint("cost", "calls", 30, float(event_count + 1)),
        TrajectoryPoint("cost", "latency_ms", 30, float(event_count + 2)),
        TrajectoryPoint("cost", "storage_bytes", 30, float(len(artifact.to_dict()))),
    )
    return WorldlineMeasurement(
        worldline_id=worldline_id,
        worldline_ref=f"worldline:g95f:{worldline_id}",
        artifact_ref=artifact.artifact_id,
        alignment_ref=alignment_ref,
        points=points,
        seed=revision + 1,
        parameters=(("scenario", "same-world-input"),),
    )


def test_real_worldline_artifacts_compare_without_mutating_runtime(
    persist_db_path: pathlib.Path,
) -> None:
    content = (
        "# G95F private source\nCharacter: Alice\nCharacter: Bob\nrelationship: Alice -> Bob\n"
    )
    source = SourceRecord(
        source_id="g95f_private_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g95f_private_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="g95f",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g95f",
        access="private",
    )
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    playable = PlayableService(runtime)
    authored = OneClickAuthoring().run("job_g95f", (source,), profile="book")
    profile = playable.register_package(
        authored.package, owner_id="owner:g95f", visibility="private"
    )
    character = playable.entry.create_character(
        "owner:g95f",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g95f_alice",
    )

    entered = playable.enter(
        profile.profile_id,
        viewer_id="owner:g95f",
        mode="embodiment",
        session_id="session:g95f",
        character_id=character.character_id,
    )
    candidate_instance = WorldInstanceId(
        str(cast(dict[str, object], entered["instance"])["instance_id"])
    )
    candidate_branch = BranchId(playable.store.get_instance(candidate_instance.value).branch_id)
    base_branch = runtime.create_branch(candidate_instance, candidate_branch).branch_id
    playable.action(
        candidate_instance.value,
        viewer_id="owner:g95f",
        action_type="set_status",
        payload={"entity_id": "ent_alice", "status": "comparator-candidate"},
    )
    base_state = runtime.current_state(candidate_instance, base_branch)
    candidate_state = runtime.current_state(candidate_instance, candidate_branch)
    base_snapshot = runtime.create_checkpoint(candidate_instance, base_branch)
    candidate_snapshot = runtime.create_checkpoint(candidate_instance, candidate_branch)
    base_events = runtime.events(candidate_instance, base_branch)
    candidate_events = runtime.events(candidate_instance, candidate_branch)
    alignment_ref = f"alignment:{source.content_hash}"

    def artifact(
        worldline_id: str,
        instance: WorldInstanceId,
        branch: BranchId,
        snapshot_id: str,
        events: tuple[CommittedEvent, ...],
        state_hash: str,
        seed: int,
    ) -> WorldRunArtifact:
        return WorldRunArtifact(
            artifact_id=f"artifact:g95f:{worldline_id}",
            world_package_ref=authored.package.package_id,
            world_package_version=str(authored.package.manifest.version),
            scenario_ref=profile.scenario_ref,
            scenario_version=str(profile.version),
            constitution_version="1",
            runtime_profile_ref=profile.runtime_profile_ref,
            provider_versions=(("reference", "1.0.0"),),
            seed=seed,
            commit_refs=tuple(event.event_id.value for event in events),
            snapshot_refs=(snapshot_id,),
            branch_refs=(branch.value,),
            actor_trajectory_refs=(("actor:alice", state_hash),),
            metrics=(("revision", float(runtime.current_state(instance, branch).revision.value)),),
        ).with_hash()

    base_artifact = artifact(
        "baseline",
        candidate_instance,
        base_branch,
        base_snapshot.snapshot_id.value,
        base_events,
        base_state.semantic_hash(),
        1,
    )
    candidate_artifact = artifact(
        "candidate",
        candidate_instance,
        candidate_branch,
        candidate_snapshot.snapshot_id.value,
        candidate_events,
        candidate_state.semantic_hash(),
        2,
    )
    measurements = (
        _measurement(
            "baseline",
            base_artifact,
            base_state.revision.value,
            len(base_events),
            alignment_ref=alignment_ref,
        ),
        _measurement(
            "candidate",
            candidate_artifact,
            candidate_state.revision.value,
            len(candidate_events),
            alignment_ref=alignment_ref,
        ),
    )

    comparator = WorldlineComparator()
    comparison = comparator.compare(measurements)
    report = comparator.api_report(comparison, measurements)

    assert base_artifact.verify_hash() is True
    assert candidate_artifact.verify_hash() is True
    assert base_state.semantic_hash() != candidate_state.semantic_hash()
    assert comparison.aligned is True
    assert comparison.qualified is True
    assert {item.category for item in comparison.categories} == {
        "actor",
        "relation",
        "institution",
        "macro",
        "cost",
    }
    assert len(comparison.differences) == 7
    series = report["series"]
    assert isinstance(series, list)
    assert len(cast(list[object], series)) == 2
    assert "G95F private source" not in repr(report)
    assert (
        runtime.restore_and_replay(candidate_instance, base_branch).state.semantic_hash()
        == base_state.semantic_hash()
    )
    assert (
        runtime.restore_and_replay(candidate_instance, candidate_branch).state.semantic_hash()
        == candidate_state.semantic_hash()
    )
    assert runtime.events(candidate_instance, base_branch) == base_events
