"""A player sees what another character changed while they were away."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_domain.errors import NotFound
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.local_store import LocalJsonPlayableStore
from wanxiang_substrate.playable.player_service import player_observe
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
        "Alice and Bob arrived in Garden in 1985.\nrule: visitors register\n"
    )
    return SourceRecord(
        source_id="away_summary_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://away_summary_source",
        stage="E3",
        rights=RightsEnvelope(owner="test", usage="test", approved=True),
        payload=content,
        provenance="synthetic:away-summary",
        access="public",
    )


def test_shared_world_changes_appear_after_the_player_returns() -> None:
    authored = OneClickAuthoring().run("job_away_summary", (_source(),), profile="book")
    runtime = build_reference_runtime()
    playable = PlayableService(runtime)
    profile = playable.register_package(authored.package, owner_id="alice", visibility="public")
    alice = playable.entry.create_character(
        "alice",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_alice",
    )
    bob = playable.entry.create_character(
        "bob",
        "Bob",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_bob",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="alice",
        mode="embodiment",
        session_id="away_alice",
        character_id=alice.character_id,
    )
    instance_id = str(cast(dict[str, object], entered["instance"])["instance_id"])
    leave = playable.leave(instance_id, viewer_id="alice")
    assert leave["status"] == "left"

    bob_entered = playable.enter(
        profile.profile_id,
        viewer_id="bob",
        mode="embodiment",
        session_id="away_bob",
        character_id=bob.character_id,
    )
    bob_instance = cast(dict[str, object], bob_entered["instance"])
    assert bob_instance["instance_id"] == instance_id
    action = playable.action(instance_id, viewer_id="bob", text="set status to alert")
    assert action.proposal.accepted
    playable.leave(instance_id, viewer_id="bob")

    alice_record = playable.store.get_instance_for(instance_id, "alice")
    assert alice_record is not None
    assert alice_record.owner_id == "alice"
    view = player_observe(playable, instance_id, "alice")
    session = cast(dict[str, object], view["session"])
    events = cast(list[dict[str, object]], session["events_since_leave"])
    assert events
    assert events[-1]["summary"]
    leave_time = cast(dict[str, int], session["leave_time"])
    assert int(leave_time["ticks"]) > 0
    assert session["status"] == "saved"

    resumed = playable.continue_instance(instance_id, viewer_id="alice")
    assert str(cast(dict[str, object], resumed["instance"])["instance_id"]) == instance_id
    active = player_observe(playable, instance_id, "alice")
    active_session = cast(dict[str, object], active["session"])
    assert active_session["events_since_leave"] == []
    assert active_session["status"] == "active"


def test_created_characters_bind_to_free_source_actors() -> None:
    authored = OneClickAuthoring().run("job_character_binding", (_source(),), profile="book")
    playable = PlayableService(build_reference_runtime())
    profile = playable.register_package(authored.package, owner_id="alice", visibility="public")
    alice = playable.entry.create_character(
        "alice",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
    )
    bob = playable.entry.create_character(
        "bob",
        "Bob",
        compatible_profile_ids=(profile.experience_package_ref,),
    )
    assert alice.character_id == "ent_alice"
    assert bob.character_id == "ent_bob"

    entered = playable.enter(
        profile.profile_id,
        viewer_id="alice",
        mode="embodiment",
        session_id="binding_alice",
        character_id=alice.character_id,
    )
    instance_id = str(cast(dict[str, object], entered["instance"])["instance_id"])
    action = playable.action(instance_id, viewer_id="alice", text="set status to alert")
    assert action.proposal.accepted
    assert action.event_id


def test_instance_handles_are_owner_scoped(tmp_path: pathlib.Path) -> None:
    authored = OneClickAuthoring().run("job_owner_scope", (_source(),), profile="book")
    store_path = tmp_path / "owner-scope.json"
    playable = PlayableService(
        build_reference_runtime(),
        store=LocalJsonPlayableStore(store_path),
    )
    profile = playable.register_package(authored.package, owner_id="alice", visibility="public")
    alice = playable.entry.create_character(
        "alice",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_alice",
    )
    bob = playable.entry.create_character(
        "bob",
        "Bob",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_bob",
    )
    alice_entered = playable.enter(
        profile.profile_id,
        viewer_id="alice",
        mode="embodiment",
        session_id="scope_alice",
        character_id=alice.character_id,
    )
    instance_id = str(cast(dict[str, object], alice_entered["instance"])["instance_id"])
    playable.enter(
        profile.profile_id,
        viewer_id="bob",
        mode="embodiment",
        session_id="scope_bob",
        character_id=bob.character_id,
    )

    assert playable.store.get_instance_for(instance_id, "alice") is not None
    assert playable.store.get_instance_for(instance_id, "bob") is not None
    with pytest.raises(NotFound):
        player_observe(playable, instance_id, "carol")

    reloaded = LocalJsonPlayableStore(store_path)
    assert reloaded.get_instance_for(instance_id, "alice") is not None
    assert reloaded.get_instance_for(instance_id, "bob") is not None
    assert reloaded.get_instance_for(instance_id, "carol") is None
