"""Generic T1 external image adapter over bounded Wanxiang scene briefs.

Vendor-specific HTTP/auth code lives behind _ExternalImageClient. This module
contains no API keys, endpoints, canonical writers, or raw-book transport.
"""

# pyright: reportPrivateUsage=false
# pyright: reportUnusedClass=false

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_scene_prompt import (
    _compile_scene_generation_brief,
    _SceneGenerationBrief,
    _story_visual_profile_from_style_key,
)
from wanxiang_substrate.assets.book_scene_visual import (
    _SceneImageProvider,
    _SceneVisualAsset,
)


@dataclass(frozen=True, slots=True)
class _ExternalImageResult:
    content: bytes
    media_type: str


class _ExternalImageClient:
    def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class _PromptedExternalSceneProvider(_SceneImageProvider):
    """T1 provider adapter; network/privacy/cost policy is enforced by materializer."""

    provider_id: str
    provider_version: str
    client: _ExternalImageClient
    cost_units_per_asset: int
    private_safe: bool
    max_output_bytes: int = 20 * 1024 * 1024
    requires_network: bool = True

    def __post_init__(self) -> None:
        if not self.provider_id or not self.provider_version:
            raise ValueError("external visual provider requires id and version")
        if self.cost_units_per_asset < 0:
            raise ValueError("external visual provider cost must be non-negative")
        if self.max_output_bytes <= 0:
            raise ValueError("external visual provider output limit must be positive")

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        style_key = (
            request.style_key
            or hashlib.sha256(f"{request.cache_key}:story-style".encode()).hexdigest()[:24]
        )
        profile = _story_visual_profile_from_style_key(style_key)
        brief = _compile_scene_generation_brief(request, profile)
        result = self.client.generate(brief)
        if not result.content:
            raise ValueError("external visual provider returned empty image bytes")
        if len(result.content) > self.max_output_bytes:
            raise ValueError("external visual provider output exceeds size limit")
        if not result.media_type.startswith("image/"):
            raise ValueError("external visual provider must return an image media type")
        digest = hashlib.sha256(result.content).hexdigest()
        return _SceneVisualAsset(
            scene_key=request.stable_key,
            place_name=request.place_name,
            provider_id=self.provider_id,
            media_type=result.media_type,
            content=result.content,
            content_sha256=digest,
            cache_key=(f"{request.cache_key}:{self.provider_id}@{self.provider_version}"),
            illustrative=True,
            style_key=style_key,
            provider_version=self.provider_version,
        )
