"""G88H core E2E: source-created package to action, diff, leave and continue."""

from __future__ import annotations

import pathlib
from typing import cast

from scripts.reference_runtime import build_reference_runtime
from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.store import ExperienceInstanceRecord
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
        "Alice arrived in Beijing in 1985.\nBob visited Beijing.\n"
        "relationship: Alice -> Bob\nrule: visitors register\n"
    )
    return SourceRecord(
        source_id="playable_e2e_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://playable_e2e_source",
        stage="E3",
        rights=RightsEnvelope(owner="test", usage="test", approved=True),
        payload=content,
        provenance="synthetic:g88h",
        access="private",
    )


def test_source_created_world_is_playable_and_continuous() -> None:
    authored = OneClickAuthoring().run("job_playable_e2e", (_source(),), profile="book")
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
        session_id="session_playable",
        character_id=character.character_id,
    )
    instance = cast(dict[str, object], entered["instance"])
    state = cast(dict[str, object], entered["state"])
    instance_id = str(instance["instance_id"])
    assert len(cast(list[object], state["entities"])) == 2
    action = playable.action(instance_id, viewer_id="alice", text="set status to awake")
    assert action.proposal.accepted
    assert action.event_id
    assert action.diff.changes
    record: ExperienceInstanceRecord = playable.store.get_instance(instance_id)
    replayed = runtime.restore_and_replay(WorldInstanceId(instance_id), BranchId(record.branch_id))
    assert replayed.state.semantic_hash() == action.state_hash
    left = playable.leave(instance_id, viewer_id="alice")
    assert left["status"] == "left"
    continued = playable.continue_instance(instance_id, viewer_id="alice")
    continued_instance = cast(dict[str, object], continued["instance"])
    assert continued_instance["instance_id"] == instance_id
    assert continued["state_hash"] == action.state_hash


def test_enter_reuses_persisted_preview_after_runtime_restart(
    persist_db_path: pathlib.Path,
) -> None:
    authored = OneClickAuthoring().run("playable_restart", (_source(),), profile="book")

    runtime1 = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    playable1 = PlayableService(runtime1)
    profile1 = playable1.register_package(authored.package, owner_id="alice", visibility="public")
    character1 = playable1.entry.create_character(
        "alice",
        "Alice",
        compatible_profile_ids=(profile1.experience_package_ref,),
        character_id="ent_alice",
    )
    first = playable1.enter(
        profile1.profile_id,
        viewer_id="alice",
        mode="embodiment",
        session_id="session_restart_1",
        character_id=character1.character_id,
    )
    first_instance = cast(dict[str, object], first["instance"])
    instance_id = str(first_instance["instance_id"])
    branch_id = str(first_instance["branch_id"])
    first_event_count = len(runtime1.events(WorldInstanceId(instance_id), BranchId(branch_id)))

    runtime2 = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    playable2 = PlayableService(runtime2)
    profile2 = playable2.register_package(authored.package, owner_id="alice", visibility="public")
    character2 = playable2.entry.create_character(
        "alice",
        "Alice",
        compatible_profile_ids=(profile2.experience_package_ref,),
        character_id="ent_alice",
    )
    second = playable2.enter(
        profile2.profile_id,
        viewer_id="alice",
        mode="embodiment",
        session_id="session_restart_2",
        character_id=character2.character_id,
    )
    second_instance = cast(dict[str, object], second["instance"])

    assert second_instance["instance_id"] == instance_id
    assert len(runtime2.events(WorldInstanceId(instance_id), BranchId(branch_id))) == (
        first_event_count
    )
    assert len(cast(list[object], cast(dict[str, object], second["state"])["entities"])) == 2
