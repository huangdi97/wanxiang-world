"""Vendor-neutral T1 image providers receive bounded scene briefs only."""

# pyright: reportPrivateUsage=false

from dataclasses import dataclass

import pytest
from wanxiang_substrate.assets.book_scene_external import (
    _ExternalImageClient,
    _ExternalImageResult,
    _PromptedExternalSceneProvider,
)
from wanxiang_substrate.assets.book_scene_plan import (
    _SourceSceneRequest,
    _SourceVisualPlan,
)
from wanxiang_substrate.assets.book_scene_prompt import _SceneGenerationBrief
from wanxiang_substrate.assets.book_scene_visual import _materialize_visual_plan
from wanxiang_substrate.assets.foundry import SemanticSceneSpec


@dataclass
class _FakeImageClient(_ExternalImageClient):
    briefs: list[_SceneGenerationBrief]

    def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
        self.briefs.append(brief)
        return _ExternalImageResult(b"\x89PNG\r\nwanxiang-test", "image/png")


def _request() -> _SourceSceneRequest:
    return _SourceSceneRequest(
        place_name="机关桥",
        stable_key="bridge",
        spec=SemanticSceneSpec(
            spec_id="scene-bridge",
            semantic_id="place:bridge",
            kind="illustrated-environment",
            requirements=(
                "source_place_name:机关桥",
                "source_context_candidate:character:沈砚",
                "source_context_candidate:event:入城",
            ),
        ),
        cache_key="cache-bridge",
        source_refs=("book#chapter-1:paragraph-3",),
        confidence=0.8,
        style_key="story-style-external",
    )


def _plan() -> _SourceVisualPlan:
    return _SourceVisualPlan(
        package_id="world:external",
        source_digest="1" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(_request(),),
        deferred_scene_count=0,
        delivery_rights="source-gated",
        external_processing_allowed=True,
    )


def test_external_provider_gets_minimal_brief_and_obeys_materializer_governance() -> None:
    client = _FakeImageClient([])
    provider = _PromptedExternalSceneProvider(
        provider_id="provider:test-image",
        provider_version="2026-10",
        client=client,
        cost_units_per_asset=3,
        private_safe=False,
    )

    with pytest.raises(ValueError, match="allow_network"):
        _materialize_visual_plan(_plan(), provider=provider, max_cost_units=3)
    with pytest.raises(ValueError, match="exceeds budget"):
        _materialize_visual_plan(
            _plan(),
            provider=provider,
            allow_network=True,
            max_cost_units=2,
        )
    with pytest.raises(ValueError, match="private-safe"):
        _materialize_visual_plan(
            _plan(),
            provider=provider,
            allow_network=True,
            max_cost_units=3,
            private_source=True,
        )

    materialized = _materialize_visual_plan(
        _plan(),
        provider=provider,
        allow_network=True,
        max_cost_units=3,
    )

    assert materialized.provider_calls == 1
    assert materialized.cost_units == 3
    assert materialized.assets[0].provider_id == "provider:test-image"
    assert materialized.assets[0].provider_version == "2026-10"
    assert materialized.assets[0].media_type == "image/png"
    assert materialized.asset_refs[0].rights == "source-gated"
    assert len(client.briefs) == 1
    brief = client.briefs[0]
    assert brief.full_source_included is False
    assert brief.source_refs == ("book#chapter-1:paragraph-3",)
    assert "机关桥" in brief.semantic_prompt
    assert "沈砚" in brief.semantic_prompt
    assert "book#chapter-1:paragraph-3" not in brief.semantic_prompt


def test_external_provider_rejects_non_image_or_oversized_output() -> None:
    class _BadClient(_ExternalImageClient):
        def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
            _ = brief
            return _ExternalImageResult(b"not-image", "text/plain")

    provider = _PromptedExternalSceneProvider(
        provider_id="provider:bad",
        provider_version="1",
        client=_BadClient(),
        cost_units_per_asset=0,
        private_safe=True,
    )
    with pytest.raises(ValueError, match="image media type"):
        provider.produce(_request())
