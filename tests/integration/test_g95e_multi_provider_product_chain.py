"""G95E: the real private source chain runs a mixed provider population."""

from __future__ import annotations

import pathlib
from typing import cast

from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.providers import ProviderCapability, ReferenceProvider
from wanxiang_substrate.capability.runtime_control import RuntimeControlLedger
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash
from wanxiang_substrate.world_lab import (
    MultiProviderWorldlineRunner,
    ProviderAssignmentPolicy,
    ProviderRunInput,
    WorldRunArtifact,
)


def test_mixed_providers_share_real_world_input_without_world_commit(
    persist_db_path: pathlib.Path,
) -> None:
    content = (
        "# G95E private source\nCharacter: Alice\nCharacter: Bob\nrelationship: Alice -> Bob\n"
    )
    source = SourceRecord(
        source_id="g95e_private_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g95e_private_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="g95e",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g95e",
        access="private",
    )
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    playable = PlayableService(runtime)
    authored = OneClickAuthoring().run("job_g95e", (source,), profile="book")
    profile = playable.register_package(
        authored.package, owner_id="owner:g95e", visibility="private"
    )
    character = playable.entry.create_character(
        "owner:g95e",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g95e_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="owner:g95e",
        mode="embodiment",
        session_id="session:g95e",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    events_before = runtime.events(instance, branch)

    input_data = ProviderRunInput(
        run_id="run:g95e:private",
        world_package_ref=authored.package.package_id,
        world_package_version=str(authored.package.manifest.version),
        scenario_ref=profile.scenario_ref,
        scenario_version=str(profile.version),
        source_refs=(source.content_ref,),
        population_refs=("actor:alice", "actor:bob", "actor:carol", "actor:dora"),
        seed=29,
        parameters=(("population", "mixed"),),
        payload=source.payload,
        private_source=True,
        control_timestamp="2026-08-27T00:00:00Z",
    )
    policy = ProviderAssignmentPolicy(
        policy_id="policy:g95e:reference-mixed",
        version=1,
        mode="round_robin",
        provider_ids=("provider:g95e:alpha", "provider:g95e:beta"),
    )
    runner = MultiProviderWorldlineRunner(
        {
            "provider:g95e:alpha": ReferenceProvider(
                ProviderCapability(
                    "provider:g95e:alpha",
                    "semantic",
                    "1.0.0",
                    private_safe=True,
                )
            ),
            "provider:g95e:beta": ReferenceProvider(
                ProviderCapability(
                    "provider:g95e:beta",
                    "semantic",
                    "1.0.0",
                    private_safe=True,
                )
            ),
        },
        RuntimeControlLedger(),
    )

    provider_run = runner.execute(input_data, policy)

    assert len(provider_run.invocations) == 4
    assert provider_run.proposal_count == 4
    assert {item.input_hash for item in provider_run.invocations} == {input_data.input_hash}
    assert runtime.events(instance, branch) == events_before

    action = playable.action(
        instance.value,
        viewer_id="owner:g95e",
        action_type="set_status",
        payload={"entity_id": "ent_alice", "status": "provider-reviewed"},
    )
    state = runtime.current_state(instance, branch)
    snapshot = runtime.create_checkpoint(instance, branch)
    events = runtime.events(instance, branch)
    artifact = WorldRunArtifact(
        artifact_id="artifact:g95e:private",
        world_package_ref=authored.package.package_id,
        world_package_version=str(authored.package.manifest.version),
        scenario_ref=profile.scenario_ref,
        scenario_version=str(profile.version),
        constitution_version="1",
        runtime_profile_ref=profile.runtime_profile_ref,
        provider_versions=provider_run.provider_versions,
        seed=input_data.seed,
        control_ledger_refs=provider_run.control_transaction_ids,
        commit_refs=tuple(event.event_id.value for event in events),
        snapshot_refs=(snapshot.snapshot_id.value,),
        branch_refs=(branch.value,),
        actor_trajectory_refs=(("actor:alice", state.semantic_hash()),),
        validation_results=(("provider_output", "proposal_only"),),
        metrics=(("revision", float(action.revision)), ("provider_count", 2.0)),
    ).with_hash()

    assert artifact.verify_hash() is True
    assert artifact.to_dict()["provider_versions"] == [
        ["provider:g95e:alpha", "1.0.0"],
        ["provider:g95e:beta", "1.0.0"],
    ]
    assert "source" not in repr(artifact.to_dict()).casefold()
    assert (
        runtime.restore_and_replay(instance, branch).state.semantic_hash() == state.semantic_hash()
    )
