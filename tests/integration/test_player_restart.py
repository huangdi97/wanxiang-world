"""Durable Player catalog round-trip and restart integration tests."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from scripts.reference_runtime import build_reference_runtime
from tests.conftest import make_world_runtime
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.factory import profile_from_world_package
from wanxiang_substrate.playable.local_store import LocalJsonPlayableStore
from wanxiang_substrate.playable.player_service import player_observe
from wanxiang_substrate.playable.restore import restore_playable_service
from wanxiang_substrate.playable.store import CharacterRecord, ExperienceInstanceRecord
from wanxiang_substrate.preview import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# Chapter\nCharacter: Alice\nAlice arrived in Beijing in 1985.\nrule: visitors register\n"
    )
    return SourceRecord(
        source_id="durable_store_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://durable_store_source",
        stage="E3",
        rights=RightsEnvelope(owner="test", usage="test", approved=True),
        payload=content,
        provenance="synthetic:durable-store",
        access="private",
    )


def _package() -> WorldPackageDraft:
    return OneClickAuthoring().run("job_durable_store", (_source(),), profile="book").package


def test_local_store_round_trips_all_product_records(tmp_path: pathlib.Path) -> None:
    package = _package()
    profile = profile_from_world_package(package, owner_id="alice", visibility="public")
    instance = ExperienceInstanceRecord(
        "play_instance",
        profile.profile_id,
        "alice",
        "branch_one",
        mode="embodiment",
        actor_id="ent_alice",
        session_id="",
        last_revision=3,
        updated_seq=4,
        runtime_instance_id="runtime_instance",
    )
    character = CharacterRecord(
        "ent_alice",
        "alice",
        "Alice",
        compatible_profile_ids=(profile.profile_id,),
        identity="守夜人",
    )
    path = tmp_path / "playable.json"
    store = LocalJsonPlayableStore(path)
    store.save_profile(profile)
    store.save_instance(instance)
    store.save_character(character)
    store.save_package(profile.profile_id, package)

    restored = LocalJsonPlayableStore(path)
    assert restored.get_profile(profile.profile_id) == profile
    assert restored.get_instance(instance.instance_id) == instance
    assert restored.get_character(character.character_id) == character
    assert restored.load_packages()[profile.profile_id] == package


def test_local_store_rejects_corrupt_file(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "broken.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(ContractError):
        LocalJsonPlayableStore(path)


def test_player_world_resumes_after_restart(
    persist_db_path: pathlib.Path,
    tmp_path: pathlib.Path,
) -> None:
    store_path = tmp_path / "playable.json"
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    first = PlayableService(runtime, store=LocalJsonPlayableStore(store_path))
    authored = OneClickAuthoring().run("job_restart_world", (_source(),), profile="book")
    profile = first.register_package(
        authored.package,
        owner_id="alice",
        visibility="public",
        display_name="重启世界",
    )
    character = first.entry.create_character(
        "alice",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_alice",
    )
    entered = first.enter(
        profile.profile_id,
        viewer_id="alice",
        mode="embodiment",
        session_id="restart_first",
        character_id=character.character_id,
    )
    instance = str(cast(dict[str, object], entered["instance"])["instance_id"])
    first.action(instance, viewer_id="alice", text="让自己保持清醒")
    first.leave(instance, viewer_id="alice")
    before = player_observe(first, instance, "alice")
    before_history = first.history(instance, viewer_id="alice")

    restarted_runtime = make_world_runtime(
        persist_db_path,
        extra_resolvers=register_preview_resolvers,
    )
    second = PlayableService(
        restarted_runtime,
        store=LocalJsonPlayableStore(store_path),
    )
    assert restore_playable_service(second) == 1

    cards = second.plaza.explore_worlds("alice")
    assert [card.profile_id for card in cards] == [profile.profile_id]
    current = second.plaza.continue_last("alice")
    assert current is not None
    assert current.instance_id == instance
    resumed = second.continue_instance(instance, viewer_id="alice")
    assert cast(dict[str, object], resumed["instance"])["instance_id"] == instance
    after = player_observe(second, instance, "alice")
    before_player = cast(dict[str, object], before["player"])
    after_player = cast(dict[str, object], after["player"])
    assert after_player["status"] == before_player["status"]
    assert second.history(instance, viewer_id="alice")["total"] == before_history["total"]


def test_in_memory_service_has_no_durable_packages_by_default() -> None:
    service = PlayableService(build_reference_runtime())
    assert service.store.load_packages() == {}
