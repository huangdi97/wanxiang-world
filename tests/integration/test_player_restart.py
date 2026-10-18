"""Durable Player catalog round-trip and restart integration tests."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import pathlib
from dataclasses import replace
from typing import Any, cast

import pytest
from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from tests.conftest import make_world_runtime
from wanxiang_api.app import create_app
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.assets.book_scene_cache import (
    LocalJsonVisualCacheIndex,
    VisualAssetCache,
)
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_scene_render import _ProceduralSvgSceneProvider
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider, _SceneVisualAsset
from wanxiang_substrate.assets.storage import LocalObjectStore
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.experience import experience_from_profile
from wanxiang_substrate.playable.factory import profile_from_world_package
from wanxiang_substrate.playable.local_store import LocalJsonPlayableStore
from wanxiang_substrate.playable.player_service import player_observe
from wanxiang_substrate.playable.restore import restore_playable_service
from wanxiang_substrate.playable.store import CharacterRecord, ExperienceInstanceRecord
from wanxiang_substrate.preview import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

HEADERS = {"X-Wanxiang-User": "studio"}


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
    experience = experience_from_profile(profile, allowed_actions=("set_status", "look"))
    store.save_package(profile.profile_id, package, experience)

    restored = LocalJsonPlayableStore(path)
    assert restored.get_profile(profile.profile_id) == profile
    assert restored.get_instance(instance.instance_id) == instance
    assert restored.get_character(character.character_id) == character
    assert restored.load_packages()[profile.profile_id] == package
    assert restored.load_experiences()[profile.profile_id] == experience


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
        allowed_actions=("set_status", "look"),
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
    assert second._experiences[profile.profile_id].allowed_actions == ("set_status", "look")

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


class _RestartProvider(SceneImageProvider):
    provider_id = "provider:restart-cache"
    provider_version = "1.0"
    cost_units_per_asset = 1
    private_safe = True

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        produced = _ProceduralSvgSceneProvider().produce(request)
        return replace(
            produced,
            provider_id=self.provider_id,
            provider_version=self.provider_version,
            cache_key=f"{request.cache_key}:{self.provider_id}@{self.provider_version}",
        )


def test_t1_cache_hit_is_free_after_service_restart(tmp_path: pathlib.Path) -> None:
    authored = OneClickAuthoring().run("job_restart_cache", (_source(),), profile="book")
    assert authored.visual_plan is not None
    place = authored.visual_plan.place_names[0]
    runtime = build_reference_runtime()

    first_cache = VisualAssetCache(
        LocalObjectStore(tmp_path / "blobs"),
        LocalJsonVisualCacheIndex(tmp_path / "index.json"),
    )
    store_path = tmp_path / "t1-store.json"
    first = PlayableService(
        runtime,
        store=LocalJsonPlayableStore(store_path),
        visual_cache=first_cache,
    )
    profile = first.register_package(authored.package, owner_id="alice", visibility="public")
    provider = _RestartProvider()
    generated = first.materialize_visual_place(
        profile.profile_id,
        place,
        viewer_id="alice",
        provider=provider,
        max_cost_units=5,
        max_deferred_generations=5,
    )
    assert generated.provider_calls == 1

    restarted_cache = VisualAssetCache(
        LocalObjectStore(tmp_path / "blobs"),
        LocalJsonVisualCacheIndex(tmp_path / "index.json"),
    )
    second = PlayableService(
        runtime,
        store=LocalJsonPlayableStore(store_path),
        visual_cache=restarted_cache,
    )
    assert restore_playable_service(second) == 1
    restored_assets = second.visual_assets(profile.profile_id, viewer_id="alice")
    assert provider.provider_id in {asset.provider_id for asset in restored_assets}
    assert {
        asset.place_name for asset in restored_assets if asset.provider_id == provider.provider_id
    } == {place}
    reused = second.materialize_visual_place(
        profile.profile_id,
        place,
        viewer_id="alice",
        provider=provider,
        max_cost_units=5,
        max_deferred_generations=5,
    )
    assert reused.provider_calls == 0
    assert reused.cache_hits == 1
    assert {asset.provider_id for asset in reused.assets} == {provider.provider_id}


def test_app_restart_resumes_world_from_saved_catalog(
    persist_db_path: pathlib.Path,
    tmp_path: pathlib.Path,
) -> None:
    source = {
        "source_id": "restart_api_source",
        "kind": "text",
        "content": (
            "# Chapter\nCharacter: Alice\nAlice arrived in Beijing in 1985.\n"
            "rule: visitors register\n"
        ),
        "stage": "E3",
        "rights_approved": True,
        "access": "private",
        "private_analysis_allowed": True,
        "package_inclusion_allowed": True,
        "public_export_allowed": False,
        "training_allowed": False,
    }
    store_path = tmp_path / "player-store.json"
    runtime = make_world_runtime(persist_db_path, extra_resolvers=register_preview_resolvers)
    first: Any = TestClient(create_app(runtime, playable_store=LocalJsonPlayableStore(store_path)))
    created = first.post(
        "/studio/one-click",
        json={"job_id": "restart_api_job", "profile": "book", "sources": [source]},
    )
    assert created.status_code == 201, created.text
    profile = first.post(
        "/studio/jobs/restart_api_job/playable-profile",
        json={"owner_id": "studio", "visibility": "public", "display_name": "重启 API 世界"},
    )
    assert profile.status_code == 200, profile.text
    profile_id = str(profile.json()["profile"]["profile_id"])
    character = first.post(
        "/experience/player/characters",
        headers=HEADERS,
        json={
            "display_name": "沈砚",
            "character_id": "ent_alice",
            "compatible_profile_ids": [profile_id],
            "identity": "守夜人",
        },
    )
    assert character.status_code == 201, character.text
    entered = first.post(
        f"/experience/player/worlds/{profile_id}/enter",
        headers=HEADERS,
        json={"mode": "embodiment", "session_id": "api_restart", "character_id": "ent_alice"},
    )
    assert entered.status_code == 200, entered.text
    instance = str(entered.json()["instance_id"])
    assert (
        first.post(
            f"/experience/player/instances/{instance}/action",
            headers=HEADERS,
            json={"text": "让自己保持清醒"},
        ).status_code
        == 200
    )
    assert first.post(
        f"/experience/player/instances/{instance}/leave", headers=HEADERS
    ).status_code == (200)
    before_history = first.get(
        f"/experience/player/instances/{instance}/history",
        headers=HEADERS,
    )
    assert before_history.status_code == 200
    before_total = int(cast(int, before_history.json()["total"]))

    restarted_runtime = make_world_runtime(
        persist_db_path,
        extra_resolvers=register_preview_resolvers,
    )
    second: Any = TestClient(
        create_app(restarted_runtime, playable_store=LocalJsonPlayableStore(store_path))
    )
    plaza = second.get("/experience/player/plaza", headers=HEADERS)
    assert plaza.status_code == 200
    body = cast(dict[str, object], plaza.json())
    world_ids = {str(item["profile_id"]) for item in cast(list[dict[str, object]], body["worlds"])}
    assert profile_id in world_ids
    continuation = cast(dict[str, object], body["continue"])
    assert continuation["instance_id"] == instance

    resumed = second.post(f"/experience/player/instances/{instance}/continue", headers=HEADERS)
    assert resumed.status_code == 200, resumed.text
    view = cast(dict[str, object], resumed.json()["view"])
    player = cast(dict[str, object], view["player"])
    assert player["name"] == "沈砚"
    history = second.get(
        f"/experience/player/instances/{instance}/history",
        headers=HEADERS,
    )
    assert history.status_code == 200
    assert int(cast(int, history.json()["total"])) == before_total
    assert before_total >= 2
