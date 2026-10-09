"""Shared value types for source-derived visual assets.

These types describe illustrative assets and provider governance. They do not
own canonical world state or Commit Authority.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass

from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.storage import AssetRef


@dataclass(frozen=True, slots=True)
class SceneVisualAsset:
    scene_key: str
    place_name: str
    provider_id: str
    media_type: str
    content: bytes
    content_sha256: str
    cache_key: str
    illustrative: bool = True
    style_key: str = ""
    provider_version: str = "1.0.0"

    def data_uri(self) -> str:
        payload = base64.b64encode(self.content).decode("ascii")
        return f"data:{self.media_type};base64,{payload}"


class SceneImageProvider:
    """Minimal replaceable scene generator contract without adding a Kernel port."""

    provider_id: str = ""
    provider_version: str = ""
    requires_network: bool = False
    cost_units_per_asset: int = 0
    private_safe: bool = False

    def produce(self, request: _SourceSceneRequest) -> SceneVisualAsset:
        raise TypeError("concrete visual implementation required")


@dataclass(frozen=True, slots=True)
class VisualMaterialization:
    assets: tuple[SceneVisualAsset, ...]
    asset_refs: tuple[AssetRef, ...]
    provider_calls: int
    cache_hits: int
    cost_units: int
