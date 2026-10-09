"""One book -> visual world uses the same generic pipeline for unrelated books."""

# pyright: reportPrivateUsage=false

from typing import cast

from wanxiang_substrate.assets.book_scene_external import (
    _ExternalImageResult,
    _PromptedExternalSceneProvider,
)
from wanxiang_substrate.assets.book_scene_prompt import _SceneGenerationBrief
from wanxiang_substrate.authoring.local_semantic_provider import LocalSemanticProvider
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.player_projection import player_world_detail
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _book(source_id: str, character: str, place: str) -> SourceRecord:
    text = (
        f"# Chapter\nCharacter: {character}\n"
        f"{character} arrived in {place} in 1985.\n"
        "rule: visitors register\n"
    )
    return SourceRecord(
        source_id=source_id,
        kind="text",
        content_hash=payload_hash(text),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(owner="synthetic", usage="test", approved=True),
        payload=text,
        provenance=f"synthetic:source-to-visual:{source_id}",
        access="public",
    )


def _profile(package_id: str, name: str) -> PlayableWorldProfile:
    return PlayableWorldProfile(
        profile_id=f"profile:{name}",
        world_package_ref=package_id,
        scenario_ref=f"scenario:{name}",
        runtime_profile_ref="runtime:reference",
        experience_package_ref=f"experience:{name}",
        projection_profile_ref="projection:player",
        visibility="public",
        display_name=name,
    )


def test_two_books_automatically_create_different_visual_assets_without_custom_code() -> None:
    fiction = OneClickAuthoring().run(
        "visual_fiction",
        (_book("fiction_source", "Alice", "Garden"),),
        profile="book",
    )
    history = OneClickAuthoring().run(
        "visual_history",
        (_book("history_source", "Clara", "Fortress"),),
        profile="book",
    )

    assert fiction.visual_plan is not None
    assert history.visual_plan is not None
    assert fiction.visual_plan.status == "READY_FOR_ASSET_PROVIDER"
    assert history.visual_plan.status == "READY_FOR_ASSET_PROVIDER"
    assert fiction.visual_assets
    assert history.visual_assets
    assert fiction.visual_asset_refs
    assert history.visual_asset_refs
    assert fiction.visual_asset_refs[0].content_hash == fiction.visual_assets[0].content_sha256
    assert history.visual_asset_refs[0].content_hash == history.visual_assets[0].content_sha256
    assert fiction.visual_plan.scene_requests[0].source_refs
    assert history.visual_plan.scene_requests[0].source_refs
    assert fiction.visual_plan.scene_requests[0].confidence > 0
    assert history.visual_plan.scene_requests[0].confidence > 0
    assert fiction.visual_assets[0].place_name == "Garden"
    assert history.visual_assets[0].place_name == "Fortress"
    assert fiction.visual_assets[0].content_sha256 != history.visual_assets[0].content_sha256

    fiction_view = player_world_detail(
        _profile(fiction.package.package_id, "Fiction"),
        fiction.package,
        locale="en-US",
        include_visual=True,
    )
    history_view = player_world_detail(
        _profile(history.package.package_id, "History"),
        history.package,
        locale="en-US",
        include_visual=True,
    )

    fiction_visual = fiction_view["visual"]
    history_visual = history_view["visual"]
    assert isinstance(fiction_visual, dict)
    assert isinstance(history_visual, dict)
    fiction_atlas = fiction_visual["atlas"]
    history_atlas = history_visual["atlas"]
    assert isinstance(fiction_atlas, dict)
    assert isinstance(history_atlas, dict)
    assert str(fiction_atlas["data_uri"]).startswith("data:image/svg+xml;base64,")
    assert str(history_atlas["data_uri"]).startswith("data:image/svg+xml;base64,")
    raw_fiction_scenes = fiction_visual["scenes"]
    raw_history_scenes = history_visual["scenes"]
    assert isinstance(raw_fiction_scenes, list)
    assert isinstance(raw_history_scenes, list)
    fiction_scenes = cast(list[dict[str, object]], raw_fiction_scenes)
    history_scenes = cast(list[dict[str, object]], raw_history_scenes)
    assert str(fiction_scenes[0]["data_uri"]).startswith("data:image/svg+xml;base64,")
    assert str(history_scenes[0]["data_uri"]).startswith("data:image/svg+xml;base64,")


def test_reimport_same_book_content_reuses_visual_cache_across_job_ids() -> None:
    from wanxiang_substrate.assets.book_scene_visual import _VisualAssetCache

    cache = _VisualAssetCache()
    first_source = _book("same_content_a", "Alice", "Garden")
    second_source = _book("same_content_b", "Alice", "Garden")
    first = OneClickAuthoring(visual_cache=cache).run(
        "visual_cache_a",
        (first_source,),
        profile="book",
    )
    second = OneClickAuthoring(visual_cache=cache).run(
        "visual_cache_b",
        (second_source,),
        profile="book",
    )

    assert first.visual_provider_calls == 1
    assert first.visual_cache_hits == 0
    assert second.visual_provider_calls == 0
    assert second.visual_cache_hits == 1
    assert first.visual_assets[0].content_sha256 == second.visual_assets[0].content_sha256
    assert first.visual_plan is not None
    assert second.visual_plan is not None
    assert first.visual_plan.source_digest == second.visual_plan.source_digest


def test_chinese_book_local_semantic_provider_builds_visual_scene_without_external_api() -> None:
    text = (
        "# 第一章\n"
        "角色：沈砚\n"
        "沈砚来到江南城。\n"
        "从江南城到机关桥需要穿过水道。\n"
        "规则：入城者必须登记。\n"
    )
    source = SourceRecord(
        source_id="zh_book_source",
        kind="text",
        content_hash=payload_hash(text),
        content_ref="memory://zh_book_source",
        stage="E3",
        rights=RightsEnvelope(owner="synthetic", usage="test", approved=True),
        payload=text,
        provenance="synthetic:source-to-visual:zh",
        access="private",
    )
    service = AuthoringService(
        providers=ProviderRouter((LocalSemanticProvider(),)),
    )
    result = OneClickAuthoring(service).run(
        "visual_chinese",
        (source,),
        profile="book",
        semantic_provider="local",
    )

    assert result.visual_plan is not None
    assert result.visual_plan.status == "READY_FOR_ASSET_PROVIDER"
    assert "江南城" in result.package.draft.places
    assert "机关桥" in result.package.draft.places
    assert any(
        relation.source_place == "江南城"
        and relation.target_place == "机关桥"
        and relation.relation_type == "route"
        for relation in result.visual_plan.topology_relations
    )
    scene = next(item for item in result.visual_plan.scene_requests if item.place_name == "江南城")
    assert scene.source_refs
    assert scene.confidence > 0
    assert scene.context_candidates
    assert any(
        item.startswith(("character:", "identity:", "event:")) for item in scene.context_candidates
    )
    assert result.visual_assets
    assert any(asset.place_name == "江南城" for asset in result.visual_assets)
    assert result.visual_provider_calls >= 1
    assert result.visual_cost_units == 0


def test_long_book_builds_bounded_preview_and_keeps_deferred_world_places() -> None:
    chapters = []
    places = ("Garden", "Fortress", "Harbor", "Library", "Market")
    for index in range(30):
        place = places[index % len(places)]
        chapters.append(
            f"# Chapter {index + 1}\nCharacter: Alice\n"
            f"Alice arrived in {place} in 1985.\n"
            f"rule: chapter-{index + 1} visitors register\n"
        )
    text = "\n".join(chapters)
    source = SourceRecord(
        source_id="long_book_source",
        kind="text",
        content_hash=payload_hash(text),
        content_ref="memory://long_book_source",
        stage="E3",
        rights=RightsEnvelope(owner="synthetic", usage="test", approved=True),
        payload=text,
        provenance="synthetic:source-to-visual:long",
        access="public",
    )
    result = OneClickAuthoring().run(
        "visual_long_book",
        (source,),
        profile="book",
    )

    assert result.visual_plan is not None
    assert result.visual_plan.status == "READY_FOR_ASSET_PROVIDER"
    assert len(result.visual_plan.place_names) >= 5
    assert len(result.visual_plan.scene_requests) == 3
    assert result.visual_plan.deferred_scene_count >= 2
    assert len(result.visual_assets) == 3
    assert all(scene.source_refs for scene in result.visual_plan.scene_requests)


class _OneClickExternalClient:
    def __init__(self) -> None:
        self.calls: list[_SceneGenerationBrief] = []

    def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
        self.calls.append(brief)
        return _ExternalImageResult(b"\x89PNG\r\none-click-external", "image/png")


def test_one_click_accepts_injected_t1_provider_without_changing_book_pipeline() -> None:
    text = "# Chapter\nCharacter: Alice\nAlice arrived in Garden in 1985.\n"
    source = SourceRecord(
        source_id="external_book_source",
        kind="text",
        content_hash=payload_hash(text),
        content_ref="memory://external_book_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="synthetic",
            usage="test",
            approved=True,
            external_model_processing_allowed=True,
            public_export_allowed=True,
        ),
        payload=text,
        provenance="synthetic:source-to-visual:external",
        access="public",
    )
    client = _OneClickExternalClient()
    provider = _PromptedExternalSceneProvider(
        provider_id="provider:integration-image",
        provider_version="2026-10",
        client=client,
        cost_units_per_asset=5,
        private_safe=False,
    )
    result = OneClickAuthoring(
        visual_provider=provider,
        visual_allow_network=True,
        visual_max_cost_units=5,
    ).run(
        "visual_external_provider",
        (source,),
        profile="book",
    )

    assert result.visual_provider_calls == 1
    assert result.visual_cost_units == 5
    assert result.visual_assets[0].provider_id == "provider:integration-image"
    assert result.visual_assets[0].provider_version == "2026-10"
    assert result.visual_assets[0].media_type == "image/png"
    assert len(client.calls) == 1
    assert client.calls[0].full_source_included is False


def test_source_gated_world_atlas_fails_closed_when_visual_delivery_is_denied() -> None:
    result = OneClickAuthoring().run(
        "visual_private_projection",
        (_book("private_projection_source", "Alice", "Garden"),),
        profile="book",
    )
    denied = player_world_detail(
        _profile(result.package.package_id, "Private"),
        result.package,
        locale="en-US",
        include_visual=True,
        visual_assets=(),
        visual_access_allowed=False,
    )

    assert denied["visual"] is None
