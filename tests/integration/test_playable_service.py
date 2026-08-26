"""G88H core E2E: source-created package to action, diff, leave and continue."""

from __future__ import annotations

from typing import cast

from scripts.reference_runtime import build_reference_runtime
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.store import ExperienceInstanceRecord
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
