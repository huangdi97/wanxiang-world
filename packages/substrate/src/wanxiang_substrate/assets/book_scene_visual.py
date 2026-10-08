"""Zero-cost visual fallback for source-derived book scenes.

The generated SVG is an *illustrative projection candidate*, not canonical
geometry. Production image/world providers can implement the same private port
without changing Source -> World or Player semantics.
"""

# pyright: reportPrivateUsage=false
# ruff: noqa: E501

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass
from html import escape
from typing import Protocol

from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest, _SourceVisualPlan


@dataclass(frozen=True, slots=True)
class _SceneVisualAsset:
    scene_key: str
    place_name: str
    provider_id: str
    media_type: str
    content: bytes
    content_sha256: str
    cache_key: str
    illustrative: bool = True
    style_key: str = ""

    def data_uri(self) -> str:
        payload = base64.b64encode(self.content).decode("ascii")
        return f"data:{self.media_type};base64,{payload}"


class _SceneImageProvider(Protocol):
    provider_id: str
    requires_network: bool
    cost_units_per_asset: int
    private_safe: bool

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset: ...


class _ProceduralSvgSceneProvider:
    """Deterministic SVG fallback so every valid book can be visual, at zero API cost."""

    provider_id = "procedural-svg-v1"
    requires_network = False
    cost_units_per_asset = 0
    private_safe = True

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        layout_digest = hashlib.sha256(request.cache_key.encode("utf-8")).digest()
        style_seed = request.style_key or request.cache_key
        style_digest = hashlib.sha256(style_seed.encode("utf-8")).digest()
        sky_hue = 185 + style_digest[0] % 36
        ground_hue = 72 + style_digest[1] % 28
        accent_hue = 20 + style_digest[2] % 40
        ridge_a = 175 + layout_digest[3] % 70
        ridge_b = 320 + layout_digest[4] % 110
        tower_x = 250 + layout_digest[5] % 420
        water = layout_digest[6] % 3 != 0
        place = escape(request.place_name)
        water_layer = (
            '<path d="M0 690 C260 610 610 760 1200 600 L1200 900 L0 900Z" '
            'fill="hsl(194 42% 37%)" opacity=".78"/>'
            if water
            else ""
        )
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" role="img">
<defs>
  <linearGradient id="sky" x2="0" y2="1">
    <stop stop-color="hsl({sky_hue} 44% 77%)"/>
    <stop offset="1" stop-color="hsl({sky_hue + 12} 28% 92%)"/>
  </linearGradient>
  <linearGradient id="mist" x2="1">
    <stop stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity=".05"/>
  </linearGradient>
</defs>
<rect width="1200" height="900" fill="url(#sky)"/>
<circle cx="940" cy="155" r="62" fill="hsl({accent_hue} 72% 78%)" opacity=".72"/>
<path d="M0 515 Q{ridge_a} 260 430 500 T820 455 T1200 490 V900 H0Z"
 fill="hsl({ground_hue} 24% 45%)"/>
<path d="M0 585 Q{ridge_b} 380 650 545 T1200 510 V900 H0Z"
 fill="hsl({ground_hue + 12} 23% 35%)" opacity=".82"/>
{water_layer}
<g fill="hsl({accent_hue} 28% 78%)" stroke="hsl({accent_hue} 18% 32%)" stroke-width="8">
  <rect x="{tower_x}" y="450" width="210" height="190" rx="5"/>
  <rect x="{tower_x + 300}" y="515" width="155" height="125" rx="5"/>
  <rect x="{max(55, tower_x - 245)}" y="530" width="145" height="110" rx="5"/>
</g>
<g fill="hsl({accent_hue + 18} 21% 28%)">
  <path d="M{tower_x - 20} 455 L{tower_x + 105} 375 L{tower_x + 230} 455Z"/>
  <path d="M{tower_x + 282} 518 L{tower_x + 377} 454 L{tower_x + 474} 518Z"/>
  <path d="M{max(35, tower_x - 263)} 532 L{max(120, tower_x - 170)} 472 L{max(205, tower_x - 82)} 532Z"/>
</g>
<path d="M55 720 C290 650 570 690 1135 555" fill="none"
 stroke="hsl({accent_hue} 16% 72%)" stroke-width="28" opacity=".82"/>
<rect x="0" y="0" width="1200" height="900" fill="url(#mist)" opacity=".14"/>
<g font-family="system-ui, 'Noto Sans SC', sans-serif" fill="#102b35">
  <text x="58" y="82" font-size="48" font-weight="800">{place}</text>
  <text x="60" y="125" font-size="22" opacity=".78">万相 · 来源驱动视觉预览</text>
</g>
<g transform="translate(58 805)" font-family="system-ui, 'Noto Sans SC', sans-serif">
  <rect width="650" height="52" rx="12" fill="#0f2734" opacity=".84"/>
  <text x="18" y="34" font-size="18" fill="#f2f5ed">示意投影：未证实的空间关系不会写入世界真相</text>
</g>
</svg>"""
        content = svg.encode("utf-8")
        content_sha = hashlib.sha256(content).hexdigest()
        return _SceneVisualAsset(
            scene_key=request.stable_key,
            place_name=request.place_name,
            provider_id=self.provider_id,
            media_type="image/svg+xml",
            content=content,
            content_sha256=content_sha,
            cache_key=f"{request.cache_key}:{self.provider_id}",
            style_key=request.style_key,
        )


def _render_visual_plan(
    plan: _SourceVisualPlan,
    provider: _SceneImageProvider | None = None,
    *,
    allow_network: bool = False,
    max_cost_units: int = 0,
) -> tuple[_SceneVisualAsset, ...]:
    """Render only planned scenes under explicit network/cost governance."""
    if plan.status not in {"READY_FOR_ASSET_PROVIDER", "BUDGET_ZERO"}:
        return ()
    selected_provider = provider or _ProceduralSvgSceneProvider()
    if selected_provider.requires_network and not allow_network:
        raise ValueError("network visual provider requires explicit allow_network")
    expected_cost = selected_provider.cost_units_per_asset * len(plan.scene_requests)
    if expected_cost > max_cost_units:
        raise ValueError(f"visual provider cost {expected_cost} exceeds budget {max_cost_units}")
    return tuple(selected_provider.produce(request) for request in plan.scene_requests)
