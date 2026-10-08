"""G95A: real private-source product chain produces sanitized run evidence."""

from __future__ import annotations

import json
import pathlib
from typing import cast

from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import WorldRunArtifact


def _source() -> SourceRecord:
    content = (
        "# G95A private source\nCharacter: Alice\nCharacter: Bob\n"
        "relationship: Alice -> Bob\nrule: the archive keeps a record\n"
    )
    return SourceRecord(
        source_id="g95a_private_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g95a_private_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="g95a",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g95a",
        access="private",
    )


def test_private_product_chain_emits_only_replayable_sanitized_refs(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    playable = PlayableService(runtime)
    source = _source()
    authored = OneClickAuthoring().run("job_g95a", (source,), profile="book")
    profile = playable.register_package(
        authored.package,
        owner_id="g95a_owner",
        visibility="private",
    )
    character = playable.entry.create_character(
        "g95a_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g95a_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g95a_owner",
        mode="embodiment",
        session_id="session_g95a",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    action = playable.action(
        instance.value,
        viewer_id="g95a_owner",
        action_type="set_status",
        payload={"entity_id": "ent_alice", "status": "observed"},
    )
    snapshot = runtime.create_checkpoint(instance, branch)
    state = runtime.current_state(instance, branch)
    events = runtime.events(instance, branch)
    artifact = WorldRunArtifact(
        artifact_id="artifact:g95a:product",
        world_package_ref=authored.package.package_id,
        world_package_version=str(authored.package.manifest.version),
        scenario_ref=profile.scenario_ref,
        scenario_version=str(profile.version),
        constitution_version="1",
        runtime_profile_ref=profile.runtime_profile_ref,
        provider_versions=(("preview", "1"), ("policy", "1")),
        seed=0,
        commit_refs=tuple(event.event_id.value for event in events),
        snapshot_refs=(snapshot.snapshot_id.value,),
        branch_refs=(branch.value,),
        actor_trajectory_refs=(("actor:alice", state.semantic_hash()),),
        validation_results=(("V0", "pass"), ("V1", "pass")),
        metrics=(
            ("event_count", float(len(events))),
            ("revision", float(action.revision)),
            ("storage_bytes", float(len(json.dumps(state.semantic_hash())))),
        ),
        privacy_metadata=(("visibility", "private"),),
        redacted_fields=("source_payload",),
    ).with_hash()

    exported = json.dumps(artifact.to_dict(), ensure_ascii=False, sort_keys=True)
    assert artifact.verify_hash() is True
    assert WorldRunArtifact.from_dict(artifact.to_dict()) == artifact
    assert source.payload not in exported
    assert (
        runtime.restore_and_replay(instance, branch).state.semantic_hash() == state.semantic_hash()
    )
