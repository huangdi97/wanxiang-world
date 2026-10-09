# pyright: reportPrivateUsage=false, reportUnusedClass=false, reportUnusedFunction=false

"""Deterministic zero-cost visual rendering for source-grounded book scenes."""

from __future__ import annotations

import hashlib
import math
from html import escape

from wanxiang_substrate.assets.book_scene_motif import (
    _motif_svg,
    _motif_uses_water,
    _scene_motif,
)
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest, _SourceVisualPlan
from wanxiang_substrate.assets.book_scene_types import SceneImageProvider, _SceneVisualAsset


class _ProceduralSvgSceneProvider(SceneImageProvider):
    """Deterministic fallback so every valid book has real pixels at zero API cost."""

    provider_id = "procedural-svg"
    provider_version = "1.1.0"
    requires_network = False
    cost_units_per_asset = 0
    private_safe = True

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        layout_digest = hashlib.sha256(request.cache_key.encode()).digest()
        style_seed = request.style_key or request.cache_key
        style_digest = hashlib.sha256(style_seed.encode()).digest()
        sky_hue = 185 + style_digest[0] % 36
        ground_hue = 72 + style_digest[1] % 28
        accent_hue = 20 + style_digest[2] % 40
        ridge_a = 175 + layout_digest[3] % 70
        ridge_b = 320 + layout_digest[4] % 110
        tower_x = 250 + layout_digest[5] % 420
        motif = _scene_motif(request.place_name)
        water = _motif_uses_water(motif) or layout_digest[6] % 3 != 0
        place = escape(request.place_name)
        motif_layer = _motif_svg(
            motif,
            accent_hue=accent_hue,
            ground_hue=ground_hue,
            anchor_x=tower_x,
        )
        water_layer = (
            '<path d="M0 690 C260 610 610 760 1200 600 L1200 900 L0 900Z" '
            'fill="hsl(194 42% 37%)" opacity=".78"/>'
            if water
            else ""
        )
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900"
 role="img" data-scene-motif="{motif}">
<defs>
  <linearGradient id="sky" x2="0" y2="1">
    <stop stop-color="hsl({sky_hue} 44% 77%)"/>
    <stop offset="1" stop-color="hsl({sky_hue + 12} 28% 92%)"/>
  </linearGradient>
  <linearGradient id="mist" x2="1">
    <stop stop-color="#fff" stop-opacity=".55"/>
    <stop offset="1" stop-color="#fff" stop-opacity=".05"/>
  </linearGradient>
</defs>
<rect width="1200" height="900" fill="url(#sky)"/>
<circle cx="940" cy="155" r="62" fill="hsl({accent_hue} 72% 78%)" opacity=".72"/>
<path d="M0 515 Q{ridge_a} 260 430 500 T820 455 T1200 490 V900 H0Z"
 fill="hsl({ground_hue} 24% 45%)"/>
<path d="M0 585 Q{ridge_b} 380 650 545 T1200 510 V900 H0Z"
 fill="hsl({ground_hue + 12} 23% 35%)" opacity=".82"/>
{water_layer}
{motif_layer}
<path d="M55 720 C290 650 570 690 1135 555" fill="none"
 stroke="hsl({accent_hue} 16% 72%)" stroke-width="28" opacity=".82"/>
<rect x="0" y="0" width="1200" height="900" fill="url(#mist)" opacity=".14"/>
<g font-family="system-ui, 'Noto Sans SC', sans-serif" fill="#102b35">
  <text x="58" y="82" font-size="48" font-weight="800">{place}</text>
  <text x="60" y="125" font-size="22" opacity=".78">万相 · 来源驱动视觉预览</text>
</g>
<g transform="translate(58 805)" font-family="system-ui, 'Noto Sans SC', sans-serif">
  <rect width="650" height="52" rx="12" fill="#0f2734" opacity=".84"/>
  <text x="18" y="34" font-size="18" fill="#f2f5ed">
   示意投影：未证实的空间关系不会写入世界真相
  </text>
</g>
</svg>"""
        content = svg.encode()
        return _SceneVisualAsset(
            scene_key=request.stable_key,
            place_name=request.place_name,
            provider_id=self.provider_id,
            media_type="image/svg+xml",
            content=content,
            content_sha256=hashlib.sha256(content).hexdigest(),
            cache_key=f"{request.cache_key}:{self.provider_id}@{self.provider_version}",
            style_key=request.style_key,
            provider_version=self.provider_version,
        )


def _render_world_atlas(plan: _SourceVisualPlan) -> _SceneVisualAsset | None:
    """Render a narrative topology atlas; coordinates are layout only, never geography."""
    places = plan.place_names or tuple(
        dict.fromkeys(request.place_name for request in plan.scene_requests)
    )
    if not places:
        return None

    visible_places = places[:24]
    center_x, center_y, radius = 600.0, 410.0, 285.0
    positions: dict[str, tuple[float, float]] = {}
    count = len(visible_places)
    if count == 1:
        positions[visible_places[0]] = (center_x, center_y)
    else:
        for index, place in enumerate(visible_places):
            angle = (-math.pi / 2) + (2 * math.pi * index / count)
            positions[place] = (
                center_x + radius * math.cos(angle),
                center_y + radius * math.sin(angle),
            )

    style_seed = (
        plan.scene_requests[0].style_key
        if plan.scene_requests and plan.scene_requests[0].style_key
        else plan.source_digest
    )
    style_digest = hashlib.sha256(style_seed.encode()).digest()
    base_hue = 175 + style_digest[0] % 52
    accent_hue = 18 + style_digest[1] % 52

    edges: list[str] = []
    for relation in plan.topology_relations:
        source = positions.get(relation.source_place)
        target = positions.get(relation.target_place)
        if source is None or target is None:
            continue
        edges.append(
            f'<line x1="{source[0]:.1f}" y1="{source[1]:.1f}" '
            f'x2="{target[0]:.1f}" y2="{target[1]:.1f}" '
            f'stroke="hsl({base_hue} 32% 43%)" stroke-width="4" '
            'marker-end="url(#arrow)" opacity=".78"/>'
        )

    nodes: list[str] = []
    for index, place in enumerate(visible_places):
        x, y = positions[place]
        label = escape(place[:18])
        hue = (accent_hue + index * 17) % 360
        nodes.append(
            f'<g transform="translate({x:.1f} {y:.1f})">'
            f'<circle r="38" fill="hsl({hue} 42% 78%)" '
            f'stroke="hsl({hue} 30% 30%)" stroke-width="4"/>'
            '<text y="61" text-anchor="middle" font-size="20" '
            'font-family="system-ui, Noto Sans SC, sans-serif" fill="#18333b">'
            f"{label}</text></g>"
        )

    omitted = max(0, len(places) - len(visible_places))
    omitted_label = (
        f'<text x="600" y="825" text-anchor="middle" font-size="18" '
        f'fill="#536a70">另有 {omitted} 个来源地点未在首屏展开</text>'
        if omitted
        else ""
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" role="img">
<defs>
  <linearGradient id="paper" x2="0" y2="1">
    <stop stop-color="hsl({base_hue} 34% 94%)"/>
    <stop offset="1" stop-color="hsl({base_hue} 20% 86%)"/>
  </linearGradient>
  <marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="3"
   orient="auto" markerUnits="strokeWidth">
    <path d="M0,0 L0,6 L9,3 z" fill="hsl({base_hue} 32% 43%)"/>
  </marker>
</defs>
<rect width="1200" height="900" fill="url(#paper)"/>
<text x="56" y="70" font-size="38" font-weight="800"
 font-family="system-ui, Noto Sans SC, sans-serif" fill="#17323d">万相 · 叙事世界图谱</text>
<text x="57" y="108" font-size="18"
 font-family="system-ui, Noto Sans SC, sans-serif" fill="#536a70">
节点来自原文地点；连线只表达来源关系；关系不等于地理坐标
</text>
{"".join(edges)}
{"".join(nodes)}
{omitted_label}
</svg>"""
    content = svg.encode()
    return _SceneVisualAsset(
        scene_key=f"atlas-{plan.source_digest[:24]}",
        place_name="世界图谱",
        provider_id="narrative-atlas-v1",
        media_type="image/svg+xml",
        content=content,
        content_sha256=hashlib.sha256(content).hexdigest(),
        cache_key=f"{plan.source_digest}:narrative-atlas-v1",
        illustrative=True,
        style_key=style_seed,
    )
