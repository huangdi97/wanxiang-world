"""Generic source-to-visual assets are deterministic and book-agnostic."""

# pyright: reportPrivateUsage=false

import hashlib
import json
import pathlib
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from threading import Lock
from time import sleep
from typing import cast

import pytest
from wanxiang_substrate.assets.book_scene_plan import (
    _PlaceEvidence,
    _SourceSceneRequest,
    _SourceTopologyRelation,
    _SourceVisualPlan,
)
from wanxiang_substrate.assets.book_scene_visual import (
    _LocalJsonVisualCacheIndex,
    _materialize_product_visual_plan,
    _materialize_visual_plan,
    _ProceduralSvgSceneProvider,
    _render_visual_plan,
    _render_world_atlas,
    _SceneImageProvider,
    _SceneVisualAsset,
    _VisualAssetCache,
)
from wanxiang_substrate.assets.foundry import SemanticSceneSpec
from wanxiang_substrate.assets.storage import LocalObjectStore


def _request(place: str, key: str) -> _SourceSceneRequest:
    return _SourceSceneRequest(
        place_name=place,
        stable_key=key,
        spec=SemanticSceneSpec(
            spec_id=f"scene-{key}",
            semantic_id=f"place:{key}",
            kind="illustrated-environment",
            requirements=(f"source_place_name:{place}",),
        ),
        cache_key=f"cache-{key}",
    )


def _plan(
    *requests: _SourceSceneRequest,
    external_processing_allowed: bool = False,
    delivery_rights: str = "source-gated",
) -> _SourceVisualPlan:
    return _SourceVisualPlan(
        package_id="world:test",
        source_digest="a" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=requests,
        deferred_scene_count=0,
        delivery_rights=delivery_rights,
        external_processing_allowed=external_processing_allowed,
    )


def test_two_unrelated_places_use_same_provider_but_different_visuals() -> None:
    provider = _ProceduralSvgSceneProvider()
    garden = provider.produce(_request("园林", "garden"))
    fortress = provider.produce(_request("堡垒", "fortress"))

    assert garden.provider_id == fortress.provider_id == "procedural-svg"
    assert garden.media_type == fortress.media_type == "image/svg+xml"
    assert garden.content != fortress.content
    assert garden.content_sha256 != fortress.content_sha256
    assert "园林".encode() in garden.content
    assert "堡垒".encode() in fortress.content
    assert b"Wanxiang" in garden.content
    assert b"source-grounded preview" in garden.content
    assert b"Illustrative projection, not world truth" in garden.content
    assert garden.data_uri().startswith("data:image/svg+xml;base64,")
    assert garden.illustrative is True


def test_t0_scene_morphology_varies_by_generic_place_semantics() -> None:
    provider = _ProceduralSvgSceneProvider()
    bridge = provider.produce(_request("机关桥", "bridge"))
    harbor = provider.produce(_request("潮汐港", "harbor"))
    garden = provider.produce(_request("月影园", "garden"))
    study = provider.produce(_request("书房", "study"))

    assert provider.provider_version == "1.1.0"
    assert b'data-scene-motif="bridge"' in bridge.content
    assert b'data-scene-motif="harbor"' in harbor.content
    assert b'data-scene-motif="garden"' in garden.content
    assert b'data-scene-motif="interior"' in study.content
    assert (
        len(
            {
                bridge.content_sha256,
                harbor.content_sha256,
                garden.content_sha256,
                study.content_sha256,
            }
        )
        == 4
    )


def test_render_visual_plan_is_deterministic_and_cost_free_by_construction() -> None:
    study = _request("书房", "study")
    dock = _request("码头", "dock")
    shared_style = "story-style"
    study = _SourceSceneRequest(
        study.place_name,
        study.stable_key,
        study.spec,
        study.cache_key,
        style_key=shared_style,
    )
    dock = _SourceSceneRequest(
        dock.place_name,
        dock.stable_key,
        dock.spec,
        dock.cache_key,
        style_key=shared_style,
    )
    plan = _plan(study, dock)
    first = _render_visual_plan(plan)
    second = _render_visual_plan(plan)

    assert first == second
    assert [item.place_name for item in first] == ["书房", "码头"]
    assert len({item.content_sha256 for item in first}) == 2
    assert {item.style_key for item in first} == {shared_style}


def test_non_ready_plan_never_generates_pixels() -> None:
    blocked = _SourceVisualPlan(
        package_id="world:blocked",
        source_digest="b" * 64,
        status="RIGHTS_BLOCKED",
        scene_requests=(_request("私有地点", "private"),),
        deferred_scene_count=0,
    )
    assert _render_visual_plan(blocked) == ()


class _RemoteLikeProvider(_SceneImageProvider):
    provider_id = "remote-test"
    provider_version = "2.3.0"
    requires_network = True
    cost_units_per_asset = 2
    private_safe = False

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        base = _ProceduralSvgSceneProvider().produce(request)
        return _SceneVisualAsset(
            scene_key=base.scene_key,
            place_name=base.place_name,
            provider_id=self.provider_id,
            media_type=base.media_type,
            content=base.content,
            content_sha256=hashlib.sha256(base.content).hexdigest(),
            cache_key=f"{request.cache_key}:{self.provider_id}@{self.provider_version}",
            illustrative=base.illustrative,
            style_key=base.style_key,
            provider_version=self.provider_version,
        )


def test_network_and_cost_are_denied_until_explicitly_authorized() -> None:
    plan = _plan(
        _request("远方", "remote"),
        external_processing_allowed=True,
    )
    provider = _RemoteLikeProvider()

    with pytest.raises(ValueError, match="allow_network"):
        _render_visual_plan(plan, provider=provider)
    with pytest.raises(ValueError, match="exceeds budget"):
        _render_visual_plan(plan, provider=provider, allow_network=True, max_cost_units=1)
    with pytest.raises(ValueError, match="private-safe"):
        _render_visual_plan(
            plan,
            provider=provider,
            allow_network=True,
            max_cost_units=2,
            private_source=True,
        )

    rendered = _render_visual_plan(
        plan,
        provider=provider,
        allow_network=True,
        max_cost_units=2,
    )
    assert rendered[0].place_name == "远方"


@pytest.mark.parametrize(
    (
        "external_processing_allowed",
        "allow_network",
        "max_cost_units",
        "private_source",
        "expected_reason",
    ),
    [
        (True, False, 2, False, "network_not_allowed"),
        (False, True, 2, False, "source_external_processing_not_allowed"),
        (True, True, 1, False, "budget_insufficient"),
        (True, True, 2, True, "private_source_provider_not_safe"),
    ],
)
def test_product_visual_ladder_falls_back_to_t0_when_t1_is_ineligible(
    external_processing_allowed: bool,
    allow_network: bool,
    max_cost_units: int,
    private_source: bool,
    expected_reason: str,
) -> None:
    plan = _plan(
        _request("备用场景", "fallback"),
        external_processing_allowed=external_processing_allowed,
    )
    result = _materialize_product_visual_plan(
        plan,
        provider=_RemoteLikeProvider(),
        allow_network=allow_network,
        max_cost_units=max_cost_units,
        private_source=private_source,
    )

    assert result.assets[0].provider_id == "procedural-svg"
    assert result.assets[0].provider_version == "1.1.0"
    assert result.cost_units == 0
    assert result.fallback_from_provider == "remote-test@2.3.0"
    assert result.fallback_reason == expected_reason


def test_cached_t1_scene_replays_offline_with_zero_generation_budget() -> None:
    plan = _plan(
        _request("已缓存远方", "cached-remote"),
        external_processing_allowed=True,
    )
    provider = _RemoteLikeProvider()
    cache = _VisualAssetCache()

    first = _materialize_product_visual_plan(
        plan,
        provider=provider,
        cache=cache,
        allow_network=True,
        max_cost_units=2,
    )
    replay = _materialize_product_visual_plan(
        plan,
        provider=provider,
        cache=cache,
        allow_network=False,
        max_cost_units=0,
    )

    assert first.provider_calls == 1
    assert first.cost_units == 2
    assert replay.provider_calls == 0
    assert replay.cache_hits == 1
    assert replay.cost_units == 0
    assert replay.fallback_from_provider == ""
    assert replay.assets[0].provider_id == "remote-test"
    assert replay.assets[0].content_sha256 == first.assets[0].content_sha256


class _FailingRemoteProvider(_RemoteLikeProvider):
    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        _ = request
        raise TimeoutError("synthetic T1 timeout")


class _InvalidRemoteProvider(_RemoteLikeProvider):
    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        good = super().produce(request)
        return _SceneVisualAsset(
            scene_key=good.scene_key,
            place_name=good.place_name,
            provider_id=good.provider_id,
            media_type=good.media_type,
            content=good.content,
            content_sha256="0" * 64,
            cache_key=good.cache_key,
            illustrative=good.illustrative,
            style_key=good.style_key,
            provider_version=good.provider_version,
        )


@pytest.mark.parametrize("provider", [_FailingRemoteProvider(), _InvalidRemoteProvider()])
def test_product_visual_ladder_falls_back_to_t0_when_eligible_t1_fails(
    provider: _SceneImageProvider,
) -> None:
    plan = _plan(
        _request("运行时保底", "runtime-fallback"),
        external_processing_allowed=True,
    )
    result = _materialize_product_visual_plan(
        plan,
        provider=provider,
        allow_network=True,
        max_cost_units=2,
    )

    assert result.assets[0].provider_id == "procedural-svg"
    assert result.assets[0].provider_version == "1.1.0"
    assert result.provider_calls == 2
    assert result.cost_units == 2
    assert result.fallback_from_provider == "remote-test@2.3.0"
    assert result.fallback_reason == "provider_failure"


class _SecondCallFailingProvider(_RemoteLikeProvider):
    def __init__(self) -> None:
        self.calls = 0

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        self.calls += 1
        if self.calls == 2:
            raise TimeoutError("synthetic second-scene timeout")
        return super().produce(request)


def test_runtime_fallback_keeps_paid_t1_asset_and_attempted_cost_after_partial_success() -> None:
    provider = _SecondCallFailingProvider()
    plan = _plan(
        _request("场景一", "partial-one"),
        _request("场景二", "partial-two"),
        external_processing_allowed=True,
    )
    result = _materialize_product_visual_plan(
        plan,
        provider=provider,
        allow_network=True,
        max_cost_units=4,
    )

    assert provider.calls == 2
    assert [asset.provider_id for asset in result.assets] == [
        "remote-test",
        "procedural-svg",
    ]
    assert result.provider_calls == 3
    assert result.cache_hits == 1
    assert result.cost_units == 4
    assert result.fallback_from_provider == "remote-test@2.3.0"
    assert result.fallback_reason == "provider_failure"


def test_strict_visual_materializer_still_surfaces_t1_execution_failure() -> None:
    plan = _plan(
        _request("严格模式", "strict-runtime"),
        external_processing_allowed=True,
    )
    with pytest.raises(ValueError, match="visual provider execution failed"):
        _materialize_visual_plan(
            plan,
            provider=_FailingRemoteProvider(),
            allow_network=True,
            max_cost_units=2,
        )


def test_visual_cache_reuses_content_addressed_asset_identity_and_avoids_provider_call() -> None:
    plan = _plan(_request("旧城", "old-city"))
    cache = _VisualAssetCache()

    first = _materialize_visual_plan(plan, cache=cache)
    second = _materialize_visual_plan(plan, cache=cache)

    assert first.provider_calls == 1
    assert first.cache_hits == 0
    assert second.provider_calls == 0
    assert second.cache_hits == 1
    assert first.assets == second.assets
    assert first.asset_refs == second.asset_refs
    assert first.asset_refs[0].content_hash == first.assets[0].content_sha256
    assert first.asset_refs[0].rights == "source-gated"
    assert cache.store.get(first.asset_refs[0]) == first.assets[0].content


class _BadDigestProvider(_RemoteLikeProvider):
    requires_network = False
    cost_units_per_asset = 0

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        good = super().produce(request)
        return _SceneVisualAsset(
            scene_key=good.scene_key,
            place_name=good.place_name,
            provider_id=good.provider_id,
            media_type=good.media_type,
            content=good.content,
            content_sha256="0" * 64,
            cache_key=good.cache_key,
        )


def test_provider_output_integrity_is_verified_before_storage() -> None:
    with pytest.raises(ValueError, match="invalid content digest"):
        _materialize_visual_plan(_plan(_request("荒原", "bad")), provider=_BadDigestProvider())


def test_remote_provider_is_blocked_by_source_rights_even_with_network_permission() -> None:
    with pytest.raises(ValueError, match="external visual processing"):
        _render_visual_plan(
            _plan(_request("私密地点", "private-remote")),
            provider=_RemoteLikeProvider(),
            allow_network=True,
            max_cost_units=2,
        )


def test_world_atlas_uses_places_and_only_source_grounded_relations() -> None:
    plan = _SourceVisualPlan(
        package_id="world:atlas",
        source_digest="c" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(_request("园林", "garden"), _request("书房", "study")),
        deferred_scene_count=1,
        topology_relations=(_SourceTopologyRelation("园林", "书房", "route", ("book#1",), 0.8),),
        place_names=("园林", "书房", "码头"),
    )
    atlas = _render_world_atlas(plan)

    assert atlas is not None
    assert atlas.provider_id == "narrative-atlas-v1"
    assert atlas.media_type == "image/svg+xml"
    assert "园林".encode() in atlas.content
    assert "书房".encode() in atlas.content
    assert "码头".encode() in atlas.content
    assert b"<line " in atlas.content
    assert "关系不等于地理坐标".encode() in atlas.content


def test_world_atlas_marks_conflicting_relations_visually() -> None:
    plan = _SourceVisualPlan(
        package_id="world:atlas-conflict",
        source_digest="f" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(_request("园林", "garden"), _request("书房", "study")),
        deferred_scene_count=0,
        topology_relations=(
            _SourceTopologyRelation(
                "园林",
                "书房",
                "route",
                ("book#1",),
                0.8,
                conflicting=True,
            ),
        ),
        place_names=("园林", "书房"),
    )
    atlas = _render_world_atlas(plan)

    assert atlas is not None
    assert b"arrow-conflict" in atlas.content
    assert b"stroke-dasharray" in atlas.content
    assert b"<desc>" in atlas.content
    assert "园林 → 书房 [route]".encode() in atlas.content
    assert "来源存在不同说法".encode() in atlas.content
    assert "橙色虚线：来源存在相反或不同类型的关系说法".encode() in atlas.content


def test_world_atlas_localizes_english_labels() -> None:
    plan = _SourceVisualPlan(
        package_id="world:atlas-en",
        source_digest="1" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(_request("Garden", "garden"), _request("Harbor", "harbor")),
        deferred_scene_count=0,
        topology_relations=(
            _SourceTopologyRelation(
                "Garden",
                "Harbor",
                "route",
                ("book#1",),
                0.8,
                conflicting=True,
            ),
        ),
        place_names=("Garden", "Harbor"),
    )
    atlas = _render_world_atlas(plan, locale="en-US")

    assert atlas is not None
    assert atlas.place_name == "World Atlas"
    assert b"Narrative World Atlas" in atlas.content
    assert b"Orange dashed edges" in atlas.content
    assert b"sources disagree" in atlas.content
    assert "橙色虚线".encode() not in atlas.content


def test_world_atlas_counts_relations_to_undrawn_places() -> None:
    place_names = ("园林", "书房") + tuple(f"P{index}" for index in range(23))
    plan = _SourceVisualPlan(
        package_id="world:atlas-omitted-relations",
        source_digest="9" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(_request("园林", "garden"), _request("书房", "study")),
        deferred_scene_count=0,
        topology_relations=(
            _SourceTopologyRelation("园林", "书房", "route", ("book#1",), 0.8),
            _SourceTopologyRelation("园林", "P22", "route", ("book#2",), 0.8),
        ),
        place_names=place_names,
    )
    atlas = _render_world_atlas(plan)

    assert atlas is not None
    assert "园林 → 书房 [route]".encode() in atlas.content
    assert "1 条关系涉及未绘制地点。".encode() in atlas.content
    assert "园林 → P22".encode() not in atlas.content


def test_world_atlas_omits_conflict_legend_when_no_conflict_is_drawn() -> None:
    place_names = ("园林", "书房") + tuple(f"P{index}" for index in range(23))
    plan = _SourceVisualPlan(
        package_id="world:atlas-undrawn-conflict",
        source_digest="8" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(_request("园林", "garden"),),
        deferred_scene_count=0,
        topology_relations=(
            _SourceTopologyRelation("园林", "书房", "route", ("book#1",), 0.8),
            _SourceTopologyRelation(
                "园林",
                "P22",
                "route",
                ("book#2",),
                0.8,
                conflicting=True,
            ),
        ),
        place_names=place_names,
    )
    atlas = _render_world_atlas(plan)

    assert atlas is not None
    assert b'marker-end="url(#arrow-conflict)"' not in atlas.content
    assert b"stroke-dasharray" not in atlas.content
    assert "橙色虚线".encode() not in atlas.content
    assert "1 条关系涉及未绘制地点。".encode() in atlas.content


def test_world_atlas_marks_places_merged_from_multiple_sources() -> None:
    plan = _SourceVisualPlan(
        package_id="world:atlas-merged",
        source_digest="e" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(_request("Harbor", "harbor"),),
        deferred_scene_count=0,
        place_names=("Harbor",),
        place_evidence=(_PlaceEvidence("Harbor", 2, 0.8, 1, source_count=2),),
    )

    atlas = _render_world_atlas(plan)

    assert atlas is not None
    assert "Harbor · ×2".encode() in atlas.content
    assert "×N 表示多个来源同名合并".encode() in atlas.content


def test_world_atlas_discloses_places_beyond_the_first_screen() -> None:
    places = tuple(f"地点{index}" for index in range(30))
    plan = _SourceVisualPlan(
        package_id="world:atlas-truncated",
        source_digest="d" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(),
        deferred_scene_count=30,
        place_names=places,
    )

    atlas = _render_world_atlas(plan)

    assert atlas is not None
    assert "地点23".encode() in atlas.content
    assert "地点24".encode() not in atlas.content
    assert "另有 6 个来源地点未绘制；可在地点列表中查看".encode() in atlas.content


class _RemoteLikeProviderV3(_RemoteLikeProvider):
    provider_version = "3.0.0"


def test_provider_version_change_invalidates_visual_cache() -> None:
    plan = _plan(
        _request("远方", "versioned"),
        external_processing_allowed=True,
    )
    cache = _VisualAssetCache()

    first = _materialize_visual_plan(
        plan,
        provider=_RemoteLikeProvider(),
        cache=cache,
        allow_network=True,
        max_cost_units=2,
    )
    upgraded = _materialize_visual_plan(
        plan,
        provider=_RemoteLikeProviderV3(),
        cache=cache,
        allow_network=True,
        max_cost_units=2,
    )

    assert first.provider_calls == 1
    assert upgraded.provider_calls == 1
    assert upgraded.cache_hits == 0
    assert first.assets[0].cache_key != upgraded.assets[0].cache_key
    assert first.assets[0].provider_version != upgraded.assets[0].provider_version


def test_visual_cache_survives_restart_with_local_blob_store_and_json_index(
    tmp_path: pathlib.Path,
) -> None:
    plan = _plan(_request("旧城", "durable"))
    blob_root = tmp_path / "blobs"
    index_path = tmp_path / "visual-cache.json"

    first_cache = _VisualAssetCache(
        LocalObjectStore(blob_root),
        _LocalJsonVisualCacheIndex(index_path),
    )
    first = _materialize_visual_plan(plan, cache=first_cache, rights="source-gated")

    restarted_cache = _VisualAssetCache(
        LocalObjectStore(blob_root),
        _LocalJsonVisualCacheIndex(index_path),
    )
    second = _materialize_visual_plan(plan, cache=restarted_cache, rights="source-gated")

    assert first.provider_calls == 1
    assert second.provider_calls == 0
    assert second.cache_hits == 1
    assert first.assets == second.assets
    assert first.asset_refs == second.asset_refs
    assert index_path.exists()


def test_cached_bytes_can_be_reused_under_current_delivery_rights_without_regeneration() -> None:
    plan = _plan(_request("旧城", "rights-reissue"))
    cache = _VisualAssetCache()

    gated = _materialize_visual_plan(plan, cache=cache, rights="source-gated")
    public = _materialize_visual_plan(plan, cache=cache, rights="public")

    assert gated.provider_calls == 1
    assert public.provider_calls == 0
    assert public.cache_hits == 1
    assert gated.assets[0].content_sha256 == public.assets[0].content_sha256
    assert gated.asset_refs[0].rights == "source-gated"
    assert public.asset_refs[0].rights == "public"


def test_missing_durable_visual_blob_is_regenerated_under_existing_governance(
    tmp_path: pathlib.Path,
) -> None:
    """An orphaned index row should not permanently break deferred scenes."""
    plan = _plan(_request("荒原", "missing-blob"))
    cache = _VisualAssetCache(
        LocalObjectStore(tmp_path / "blobs"),
        _LocalJsonVisualCacheIndex(tmp_path / "index.json"),
    )
    first = _materialize_visual_plan(plan, cache=cache)
    cache.store.delete(first.asset_refs[0])

    recovered = _materialize_visual_plan(plan, cache=cache)
    assert recovered.provider_calls == 1
    assert recovered.cache_hits == 0
    assert recovered.assets == first.assets
    assert cache.store.get(recovered.asset_refs[0]) == first.assets[0].content


def test_visual_index_wrong_cache_key_is_never_treated_as_a_scene_hit(
    tmp_path: pathlib.Path,
) -> None:
    original = _request("园林", "revisioned-cache")
    cache_path = tmp_path / "index.json"
    cache = _VisualAssetCache(
        LocalObjectStore(tmp_path / "blobs"), _LocalJsonVisualCacheIndex(cache_path)
    )
    first = _materialize_visual_plan(_plan(original), cache=cache)
    assert first.provider_calls == 1

    revised = replace(original, cache_key="cache-reviewed-evidence")
    provider = _ProceduralSvgSceneProvider()
    target_key = f"{revised.cache_key}:{provider.provider_id}@{provider.provider_version}"
    raw: object = json.loads(cache_path.read_text(encoding="utf-8"))
    assert isinstance(raw, dict)
    rows = cast(dict[str, dict[str, object]], raw)
    old_key = next(iter(rows))
    rows[target_key] = dict(rows[old_key])
    cache_path.write_text(json.dumps(rows), encoding="utf-8")

    assert cache.get(target_key, rights="source-gated") is None
    repaired = _materialize_visual_plan(_plan(revised), cache=cache)
    assert repaired.provider_calls == 1
    assert repaired.cache_hits == 0
    assert repaired.assets[0].cache_key == target_key
    assert cache.get(target_key, rights="source-gated") is not None


def test_corrupt_durable_scene_recovers_then_reuses_verified_bytes(
    tmp_path: pathlib.Path,
) -> None:
    plan = _plan(_request("机关桥", "corrupt-recovery"))
    cache = _VisualAssetCache(
        LocalObjectStore(tmp_path / "blobs"),
        _LocalJsonVisualCacheIndex(tmp_path / "index.json"),
    )
    initial = _materialize_visual_plan(plan, cache=cache)
    ref = initial.asset_refs[0]
    corrupt_path = tmp_path / "blobs" / ref.content_hash[:2] / ref.content_hash
    corrupt_path.write_bytes(b"not-the-original-image")

    repaired = _materialize_visual_plan(plan, cache=cache)
    assert repaired.provider_calls == 1
    assert repaired.cache_hits == 0
    assert repaired.assets == initial.assets
    assert cache.store.get(repaired.asset_refs[0]) == initial.assets[0].content
    again = _materialize_visual_plan(plan, cache=cache)
    assert again.provider_calls == 0
    assert again.cache_hits == 1


def test_corrupt_scene_does_not_bypass_remote_cost_governance(
    tmp_path: pathlib.Path,
) -> None:
    plan = _plan(_request("机关桥", "corrupt-cost"), external_processing_allowed=True)
    cache = _VisualAssetCache(
        LocalObjectStore(tmp_path / "blobs"),
        _LocalJsonVisualCacheIndex(tmp_path / "index.json"),
    )
    provider = _RemoteLikeProvider()
    first = _materialize_visual_plan(
        plan, provider=provider, cache=cache, allow_network=True, max_cost_units=2
    )
    ref = first.asset_refs[0]
    (tmp_path / "blobs" / ref.content_hash[:2] / ref.content_hash).write_bytes(b"bad")
    with pytest.raises(ValueError, match="exceeds budget"):
        _materialize_visual_plan(
            plan, provider=provider, cache=cache, allow_network=True, max_cost_units=0
        )
    recovered = _materialize_visual_plan(
        plan, provider=provider, cache=cache, allow_network=True, max_cost_units=2
    )
    assert recovered.provider_calls == 1
    assert recovered.assets[0].content_sha256 == ref.content_hash


def test_missing_blob_does_not_bypass_network_or_cost_gates(
    tmp_path: pathlib.Path,
) -> None:
    plan = _plan(_request("港湾", "missing-remote"), external_processing_allowed=True)
    cache = _VisualAssetCache(
        LocalObjectStore(tmp_path / "blobs"),
        _LocalJsonVisualCacheIndex(tmp_path / "index.json"),
    )
    provider = _RemoteLikeProvider()
    first = _materialize_visual_plan(
        plan, provider=provider, cache=cache, allow_network=True, max_cost_units=2
    )
    cache.store.delete(first.asset_refs[0])

    with pytest.raises(ValueError, match="allow_network"):
        _materialize_visual_plan(plan, provider=provider, cache=cache)
    with pytest.raises(ValueError, match="exceeds budget"):
        _materialize_visual_plan(
            plan, provider=provider, cache=cache, allow_network=True, max_cost_units=0
        )


class _WrongSceneProvider(_RemoteLikeProvider):
    requires_network = False
    cost_units_per_asset = 0
    private_safe = True

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        good = super().produce(request)
        return _SceneVisualAsset(
            scene_key="another-book-scene",
            place_name=good.place_name,
            provider_id=good.provider_id,
            provider_version=good.provider_version,
            media_type=good.media_type,
            content=good.content,
            content_sha256=good.content_sha256,
            cache_key=good.cache_key,
            style_key=good.style_key,
        )


def test_visual_provider_cannot_rebind_image_to_unrelated_book_scene() -> None:
    with pytest.raises(ValueError, match="source scene identity"):
        _materialize_visual_plan(_plan(_request("花园", "garden")), provider=_WrongSceneProvider())


class _WrongMediaProvider(_WrongSceneProvider):
    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        good = _RemoteLikeProvider.produce(self, request)
        return _SceneVisualAsset(
            scene_key=good.scene_key,
            place_name=good.place_name,
            provider_id=good.provider_id,
            provider_version=good.provider_version,
            media_type="text/html",
            content=good.content,
            content_sha256=good.content_sha256,
            cache_key=good.cache_key,
            style_key=good.style_key,
        )


def test_visual_provider_cannot_inject_non_image_media_into_player() -> None:
    with pytest.raises(ValueError, match="non-empty image content"):
        _materialize_visual_plan(_plan(_request("城门", "gate")), provider=_WrongMediaProvider())


class _NegativeCostProvider(_WrongSceneProvider):
    cost_units_per_asset = -2


def test_negative_provider_cost_is_rejected_before_generation() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        _materialize_visual_plan(_plan(_request("城门", "gate")), provider=_NegativeCostProvider())


class _SlowCountingProvider(_RemoteLikeProvider):
    requires_network = False
    cost_units_per_asset = 0
    private_safe = True

    def __init__(self) -> None:
        self.calls = 0
        self._counter_lock = Lock()

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        with self._counter_lock:
            self.calls += 1
        sleep(0.025)
        return super().produce(request)


def test_simultaneous_requests_for_same_scene_pay_once_per_cache_key() -> None:
    plan = _plan(_request("潮汐港", "parallel-cost"))
    cache = _VisualAssetCache()
    provider = _SlowCountingProvider()

    def materialize(_: int) -> int:
        result = _materialize_visual_plan(plan, provider=provider, cache=cache)
        return result.provider_calls

    with ThreadPoolExecutor(max_workers=6) as executor:
        calls = list(executor.map(materialize, range(6)))

    assert provider.calls == 1
    assert sorted(calls) == [0, 0, 0, 0, 0, 1]


def test_separate_durable_cache_instances_coalesce_same_scene_generation(
    tmp_path: pathlib.Path,
) -> None:
    """Two API workers sharing a local JSON cache must not double-bill a scene."""
    plan = _plan(_request("潮汐港", "shared-file-lock"))
    provider = _SlowCountingProvider()
    caches = tuple(
        _VisualAssetCache(
            LocalObjectStore(tmp_path / "blobs"),
            _LocalJsonVisualCacheIndex(tmp_path / "index.json"),
        )
        for _ in range(4)
    )

    def materialize(cache: _VisualAssetCache) -> int:
        result = _materialize_visual_plan(plan, provider=provider, cache=cache)
        return result.provider_calls

    with ThreadPoolExecutor(max_workers=4) as executor:
        calls = list(executor.map(materialize, caches))

    assert provider.calls == 1
    assert sorted(calls) == [0, 0, 0, 1]
