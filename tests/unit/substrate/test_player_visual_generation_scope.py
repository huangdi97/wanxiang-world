"""Public viewers may reuse premium visuals but cannot create provider spend."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from types import SimpleNamespace
from typing import cast

import pytest
from tests.unit.substrate.test_book_scene_plan import package_from_book
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.assets.book_scene_cache import VisualAssetCache
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_scene_render import _ProceduralSvgSceneProvider
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider, _SceneVisualAsset
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.playable.service_visual import _materialize_visual_place


class _Plaza:
    def require_access(self, profile_id: str, viewer_id: str) -> object:
        _ = profile_id, viewer_id
        return SimpleNamespace(owner_id="owner")


class _CountingProvider(SceneImageProvider):
    provider_id = "provider:metered"
    provider_version = "2026-10"
    requires_network = True
    cost_units_per_asset = 5
    private_safe = False

    def __init__(self) -> None:
        self.calls = 0

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        self.calls += 1
        fallback = _ProceduralSvgSceneProvider().produce(request)
        return _SceneVisualAsset(
            scene_key=request.stable_key,
            place_name=request.place_name,
            provider_id=self.provider_id,
            media_type=fallback.media_type,
            content=fallback.content,
            content_sha256=fallback.content_sha256,
            cache_key=f"{request.cache_key}:{self.provider_id}@{self.provider_version}",
            illustrative=True,
            style_key=request.style_key,
            provider_version=self.provider_version,
        )


def _service() -> PlayableService:
    package = package_from_book(
        "public-paid-world",
        ("Garden",),
        compiler_metadata={
            "visual_asset_rights_v1": "public",
            "external_visual_processing_allowed_v1": "true",
            "visual_private_source_v1": "false",
        },
    )
    return cast(
        PlayableService,
        SimpleNamespace(
            plaza=_Plaza(),
            _packages={"profile": package},
            _visual_cache=VisualAssetCache(),
            _visual_assets={},
            _visual_asset_refs={},
            _deferred_visual_calls={},
        ),
    )


def test_owner_deferred_provider_calls_are_capped_but_cache_hits_stay_free() -> None:
    package = package_from_book(
        "budget-world",
        ("Garden", "Harbor"),
        compiler_metadata={
            "visual_asset_rights_v1": "public",
            "external_visual_processing_allowed_v1": "true",
            "visual_private_source_v1": "false",
        },
    )
    service = cast(
        PlayableService,
        SimpleNamespace(
            plaza=_Plaza(),
            _packages={"profile": package},
            _visual_cache=VisualAssetCache(),
            _visual_assets={},
            _visual_asset_refs={},
            _deferred_visual_calls={},
        ),
    )
    provider = _CountingProvider()

    first = _materialize_visual_place(
        service,
        "profile",
        "Garden",
        viewer_id="owner",
        provider=provider,
        allow_network=True,
        max_cost_units=5,
        max_deferred_generations=1,
    )
    assert first.provider_calls == 1

    with pytest.raises(ContractError, match=r"on-demand visual budget exhausted \(1/1\)"):
        _materialize_visual_place(
            service,
            "profile",
            "Harbor",
            viewer_id="owner",
            provider=provider,
            allow_network=True,
            max_cost_units=5,
            max_deferred_generations=1,
        )
    assert provider.calls == 1

    again = _materialize_visual_place(
        service,
        "profile",
        "Garden",
        viewer_id="owner",
        provider=provider,
        allow_network=True,
        max_cost_units=5,
        max_deferred_generations=1,
    )
    assert again.cache_hits == 1
    assert provider.calls == 1

    visitor = _materialize_visual_place(
        service,
        "profile",
        "Harbor",
        viewer_id="visitor",
        provider=provider,
        allow_network=True,
        max_cost_units=5,
        max_deferred_generations=1,
    )
    assert visitor.cost_units == 0
    assert visitor.fallback_reason == "provider_generation_not_allowed"
    assert provider.calls == 1


def test_public_viewer_falls_back_locally_instead_of_creating_provider_spend() -> None:
    service = _service()
    provider = _CountingProvider()

    visitor = _materialize_visual_place(
        service,
        "profile",
        "Garden",
        viewer_id="visitor",
        provider=provider,
        allow_network=True,
        max_cost_units=5,
    )

    assert provider.calls == 0
    assert visitor.assets[0].provider_id == "procedural-svg"
    assert visitor.cost_units == 0
    assert visitor.fallback_reason == "provider_generation_not_allowed"


def test_public_viewer_can_reuse_owner_generated_t1_without_new_provider_call() -> None:
    service = _service()
    provider = _CountingProvider()

    owner = _materialize_visual_place(
        service,
        "profile",
        "Garden",
        viewer_id="owner",
        provider=provider,
        allow_network=True,
        max_cost_units=5,
    )
    assert provider.calls == 1
    assert owner.assets[0].provider_id == provider.provider_id

    visitor = _materialize_visual_place(
        service,
        "profile",
        "Garden",
        viewer_id="visitor",
        provider=provider,
        allow_network=True,
        max_cost_units=5,
    )

    assert provider.calls == 1
    assert visitor.provider_calls == 0
    assert visitor.cache_hits == 1
    assert visitor.assets[0].provider_id == provider.provider_id
    assert visitor.fallback_reason == ""
