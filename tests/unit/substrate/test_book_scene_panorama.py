"""T2 panorama is a bounded, cacheable projection upgrade rather than world state."""

# pyright: reportPrivateUsage=false

from dataclasses import dataclass

from wanxiang_substrate.assets.book_scene_external import (
    _ExternalImageClient,
    _ExternalImageResult,
)
from wanxiang_substrate.assets.book_scene_panorama import _PromptedPanoramaSceneProvider
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest, _SourceVisualPlan
from wanxiang_substrate.assets.book_scene_prompt import _SceneGenerationBrief
from wanxiang_substrate.assets.book_scene_visual import (
    _materialize_visual_plan,
    _VisualAssetCache,
)
from wanxiang_substrate.assets.foundry import SemanticSceneSpec


@dataclass
class _Client(_ExternalImageClient):
    briefs: list[_SceneGenerationBrief]

    def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
        self.briefs.append(brief)
        return _ExternalImageResult(b"\x89PNG\r\n\x1a\npanorama", "image/png")


def _request() -> _SourceSceneRequest:
    return _SourceSceneRequest(
        place_name="潮汐港",
        stable_key="harbor",
        spec=SemanticSceneSpec(
            spec_id="source-scene-harbor",
            semantic_id="place:harbor",
            kind="illustrated-environment",
            requirements=(
                "source_place_name:潮汐港",
                "source_context_candidate:event:靠岸",
            ),
        ),
        cache_key="cache-harbor",
        source_refs=("text://book#paragraph/7",),
        confidence=0.82,
        style_key="story-style",
    )


def _plan() -> _SourceVisualPlan:
    return _SourceVisualPlan(
        package_id="world:panorama",
        source_digest="a" * 64,
        status="READY_FOR_ASSET_PROVIDER",
        scene_requests=(_request(),),
        deferred_scene_count=0,
        external_processing_allowed=True,
    )


def test_panorama_provider_uses_bounded_brief_and_marks_projection_kind() -> None:
    client = _Client([])
    provider = _PromptedPanoramaSceneProvider(
        provider_id="provider:panorama",
        provider_version="2026-10",
        client=client,
        cost_units_per_asset=4,
        private_safe=False,
    )

    asset = provider.produce(_request())

    assert asset.presentation_kind == "panorama"
    assert asset.place_name == "潮汐港"
    assert len(client.briefs) == 1
    assert client.briefs[0].source_refs == ()
    assert client.briefs[0].full_source_included is False
    assert "潮汐港" in client.briefs[0].semantic_prompt
    assert "text://book#paragraph/7" not in client.briefs[0].semantic_prompt


def test_panorama_materialization_reuses_content_addressed_cache() -> None:
    client = _Client([])
    provider = _PromptedPanoramaSceneProvider(
        provider_id="provider:panorama",
        provider_version="2026-10",
        client=client,
        cost_units_per_asset=4,
        private_safe=False,
    )
    cache = _VisualAssetCache()

    first = _materialize_visual_plan(
        _plan(),
        provider=provider,
        cache=cache,
        allow_network=True,
        max_cost_units=4,
    )
    second = _materialize_visual_plan(
        _plan(),
        provider=provider,
        cache=cache,
        allow_network=False,
        max_cost_units=0,
    )

    assert first.provider_calls == 1
    assert first.cost_units == 4
    assert second.provider_calls == 0
    assert second.cache_hits == 1
    assert second.cost_units == 0
    assert second.assets[0].presentation_kind == "panorama"
    assert len(client.briefs) == 1
