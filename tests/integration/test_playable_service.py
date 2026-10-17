"""G88H core E2E: source-created package to action, diff, leave and continue."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from scripts.reference_runtime import build_reference_runtime
from tests.conftest import make_world_runtime
from wanxiang_domain.errors import NotFound
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.authoring.local_semantic_provider import LocalSemanticProvider
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.service import AuthoringService
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


def test_deferred_book_place_generates_once_then_reuses_visual_cache() -> None:
    content = (
        "# 第一章\n角色：沈砚\n"
        "沈砚来到江南城。\n"
        "沈砚来到机关桥。\n"
        "沈砚来到潮汐港。\n"
        "沈砚来到望月亭。\n"
        "沈砚来到青石巷。\n"
        "规则：入城者必须登记。\n"
    )
    source = SourceRecord(
        source_id="playable_visual_deferred",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://playable_visual_deferred",
        stage="E3",
        rights=RightsEnvelope(owner="test", usage="test", approved=True),
        payload=content,
        provenance="synthetic:deferred-visual",
        access="private",
    )
    authoring_service = AuthoringService(
        providers=ProviderRouter((LocalSemanticProvider(),)),
    )
    authored = OneClickAuthoring(authoring_service).run(
        "job_playable_visual_deferred",
        (source,),
        profile="book",
        semantic_provider="local",
    )
    assert authored.visual_plan is not None
    assert len(authored.visual_plan.place_names) >= 5

    playable = PlayableService(build_reference_runtime())
    profile = playable.register_package(
        authored.package,
        owner_id="alice",
        visibility="private",
    )
    initial_assets = playable.visual_assets(profile.profile_id, viewer_id="alice")
    assert len(initial_assets) == 3
    generated_places = {asset.place_name for asset in initial_assets}
    target = next(
        place for place in authored.visual_plan.place_names if place not in generated_places
    )

    entered = playable.enter(
        profile.profile_id,
        viewer_id="alice",
        mode="observer",
        session_id="observer_tour_session",
    )
    instance_id = str(cast(dict[str, object], entered["instance"])["instance_id"])
    observation_before = playable.observe(instance_id, "alice")
    instances_before = playable.store.list_instances()

    first = playable.materialize_visual_place(
        profile.profile_id,
        target,
        viewer_id="alice",
    )
    second = playable.materialize_visual_place(
        profile.profile_id,
        target,
        viewer_id="alice",
    )

    assert first.provider_calls == 1
    assert first.cache_hits == 0
    assert second.provider_calls == 0
    assert second.cache_hits == 1
    assert playable.store.list_instances() == instances_before
    # Observer scene browsing is a visual preview: it must not move the
    # canonical location, advance world time, or append history.
    assert playable.observe(instance_id, "alice") == observation_before
    assert target in {
        asset.place_name for asset in playable.visual_assets(profile.profile_id, viewer_id="alice")
    }
    with pytest.raises(NotFound):
        playable.materialize_visual_place(
            profile.profile_id,
            "不存在的地点",
            viewer_id="alice",
        )


def test_worldline_fork_preserves_parent_and_diverges_independently() -> None:
    authored = OneClickAuthoring().run("job_worldline_fork", (_source(),), profile="book")
    playable = PlayableService(build_reference_runtime())
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
        session_id="fork_parent_session",
        character_id=character.character_id,
    )
    parent = str(cast(dict[str, object], entered["instance"])["instance_id"])
    action = playable.action(parent, viewer_id="alice", text="让自己保持清醒")
    assert action.diff.no_change is False
    parent_before = playable.observe(parent, "alice")

    fork = playable.fork_worldline(parent, viewer_id="alice")
    child = str(fork["instance_id"])
    assert child != parent
    record = playable.store.get_instance(child)
    assert record.branch_id == child
    assert record.runtime_instance_id
    assert record.session_id == ""
    assert playable.observe(parent, "alice") == parent_before

    child_before_continue = playable.observe(child, "alice")
    assert child_before_continue["state_hash"] == parent_before["state_hash"]

    listing = playable.worldlines(child, viewer_id="alice")
    cards = cast(list[dict[str, object]], listing["worldlines"])
    assert {str(card["instance_id"]) for card in cards} == {parent, child}
    assert listing["branches"] == 2
    child_card = next(card for card in cards if card["instance_id"] == child)
    parent_card = next(card for card in cards if card["instance_id"] == parent)
    assert child_card["current"] is True
    assert parent_card["current"] is False
    assert child_card["forked_from_revision"] is not None
    parent_record = playable.store.get_instance(parent)
    parent_events = playable.runtime.events(
        WorldInstanceId(record.runtime_instance_id), BranchId(parent_record.branch_id)
    )
    assert child_card["world_time"] == parent_events[-1].world_time.ticks

    playable.leave(parent, viewer_id="alice")
    playable.continue_instance(child, viewer_id="alice")
    child_action = playable.action(child, viewer_id="alice", text="让自己保持警觉")
    assert child_action.diff.no_change is False

    child_after = playable.observe(child, "alice")
    parent_after = playable.observe(parent, "alice")
    assert child_after["state_hash"] != parent_after["state_hash"]
    assert parent_after["state_hash"] == parent_before["state_hash"]
    assert parent_after["revision"] == parent_before["revision"]

    # The forked worldline replays inherited history plus its own event.
    runtime_id = WorldInstanceId(record.runtime_instance_id)
    child_events = playable.runtime.events(runtime_id, BranchId(child))
    assert len(child_events) == 1
    replay = playable.replay_at(
        child,
        viewer_id="alice",
        at_ticks=child_events[-1].world_time.ticks,
    )
    assert cast(dict[str, object], replay["replay"])["event_count"] == 5
    assert cast(dict[str, object], replay["player"])["status"] == "警觉"
