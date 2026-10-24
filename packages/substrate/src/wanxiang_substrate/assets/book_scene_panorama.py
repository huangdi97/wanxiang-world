"""Synchronous T2 panorama adapter over the governed T1 scene-image contract.

The provider receives the same bounded SceneGenerationBrief and returns a
raster panorama projection. Panorama pixels remain illustrative and cannot
create topology, location, or canonical History.
"""

# pyright: reportPrivateUsage=false, reportUnusedClass=false

from __future__ import annotations

from dataclasses import dataclass, replace

from wanxiang_substrate.assets.book_scene_external import _PromptedExternalSceneProvider
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_scene_types import _SceneVisualAsset


@dataclass(frozen=True, slots=True)
class _PromptedPanoramaSceneProvider(_PromptedExternalSceneProvider):
    """Explicit T2 upgrade provider; never used by default book ingestion."""

    presentation_kind: str = "panorama"

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        asset = _PromptedExternalSceneProvider.produce(self, request)
        return replace(asset, presentation_kind="panorama")
