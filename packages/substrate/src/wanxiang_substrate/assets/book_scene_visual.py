"""Zero-cost visual fallback for source-derived book scenes.

The generated SVG is an *illustrative projection candidate*, not canonical
geometry. Production image/world providers can implement the same private port
without changing Source -> World or Player semantics.
"""

# pyright: reportPrivateUsage=false
# pyright: reportUnusedFunction=false
# ruff: noqa: E501

from __future__ import annotations

import base64
import hashlib
import json
import math
import pathlib
from dataclasses import asdict, dataclass
from html import escape
from typing import Protocol

from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest, _SourceVisualPlan
from wanxiang_substrate.assets.storage import AssetRef, InMemoryObjectStore, ObjectStore


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
    provider_version: str = "1.0.0"

    def data_uri(self) -> str:
        payload = base64.b64encode(self.content).decode("ascii")
        return f"data:{self.media_type};base64,{payload}"


class _SceneImageProvider(Protocol):
    @property
    def provider_id(self) -> str: ...

    @property
    def provider_version(self) -> str: ...

    @property
    def requires_network(self) -> bool: ...

    @property
    def cost_units_per_asset(self) -> int: ...

    @property
    def private_safe(self) -> bool: ...

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset: ...


class _ProceduralSvgSceneProvider:
    """Deterministic SVG fallback so every valid book can be visual, at zero API cost."""

    provider_id = "procedural-svg"
    provider_version = "1.0.0"
    requires_network = False
    cost_units_per_asset = 0
    private_safe = True

    def produce(self, request: _SourceSceneRequest) -> _SceneVisualAsset:
        layout_digest = hashlib.sha256(request.cache_key.encode("utf-8")).digest()
        style_seed = request.style_key or request.cache_key
        style_digest = hashlib.sha256(style_seed.encode()).digest()
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
    style_digest = hashlib.sha256(style_seed.encode("utf-8")).digest()
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
节点来自原文地点；连线仅来自已提取关系，不代表真实地理坐标
</text>
{"".join(edges)}
{"".join(nodes)}
{omitted_label}
</svg>"""
    content = svg.encode("utf-8")
    digest = hashlib.sha256(content).hexdigest()
    return _SceneVisualAsset(
        scene_key=f"atlas-{plan.source_digest[:24]}",
        place_name="世界图谱",
        provider_id="narrative-atlas-v1",
        media_type="image/svg+xml",
        content=content,
        content_sha256=digest,
        cache_key=f"{plan.source_digest}:narrative-atlas-v1",
        illustrative=True,
        style_key=style_seed,
    )


@dataclass(frozen=True, slots=True)
class _VisualMaterialization:
    assets: tuple[_SceneVisualAsset, ...]
    asset_refs: tuple[AssetRef, ...]
    provider_calls: int
    cache_hits: int
    cost_units: int


@dataclass(frozen=True, slots=True)
class _VisualCacheRecord:
    cache_key: str
    scene_key: str
    place_name: str
    provider_id: str
    provider_version: str
    media_type: str
    content_sha256: str
    asset_id: str
    size: int
    illustrative: bool
    style_key: str


class _VisualCacheIndex(Protocol):
    """Metadata index port; blob bytes remain owned by ObjectStore."""

    def get(self, cache_key: str) -> _VisualCacheRecord | None: ...
    def put(self, record: _VisualCacheRecord) -> None: ...


class _InMemoryVisualCacheIndex:
    def __init__(self) -> None:
        self._rows: dict[str, _VisualCacheRecord] = {}

    def get(self, cache_key: str) -> _VisualCacheRecord | None:
        return self._rows.get(cache_key)

    def put(self, record: _VisualCacheRecord) -> None:
        self._rows[record.cache_key] = record


class _LocalJsonVisualCacheIndex:
    """Single-process durable dev index; production may inject a DB/object index."""

    def __init__(self, path: pathlib.Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def _rows(self) -> dict[str, dict[str, object]]:
        if not self._path.exists():
            return {}
        try:
            decoded: object = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        if not isinstance(decoded, dict):
            return {}
        rows: dict[str, dict[str, object]] = {}
        for raw_key, raw_value in decoded.items():
            if isinstance(raw_key, str) and isinstance(raw_value, dict):
                rows[raw_key] = {
                    str(key): value
                    for key, value in raw_value.items()
                    if isinstance(key, str)
                }
        return rows

    @staticmethod
    def _record(raw: dict[str, object]) -> _VisualCacheRecord | None:
        try:
            values = {
                "cache_key": raw["cache_key"],
                "scene_key": raw["scene_key"],
                "place_name": raw["place_name"],
                "provider_id": raw["provider_id"],
                "provider_version": raw["provider_version"],
                "media_type": raw["media_type"],
                "content_sha256": raw["content_sha256"],
                "asset_id": raw["asset_id"],
                "size": raw["size"],
                "illustrative": raw["illustrative"],
                "style_key": raw["style_key"],
            }
        except KeyError:
            return None
        if not all(
            isinstance(values[name], str)
            for name in (
                "cache_key",
                "scene_key",
                "place_name",
                "provider_id",
                "provider_version",
                "media_type",
                "content_sha256",
                "asset_id",
                "style_key",
            )
        ):
            return None
        if not isinstance(values["size"], int) or not isinstance(values["illustrative"], bool):
            return None
        return _VisualCacheRecord(
            cache_key=str(values["cache_key"]),
            scene_key=str(values["scene_key"]),
            place_name=str(values["place_name"]),
            provider_id=str(values["provider_id"]),
            provider_version=str(values["provider_version"]),
            media_type=str(values["media_type"]),
            content_sha256=str(values["content_sha256"]),
            asset_id=str(values["asset_id"]),
            size=int(values["size"]),
            illustrative=bool(values["illustrative"]),
            style_key=str(values["style_key"]),
        )

    def get(self, cache_key: str) -> _VisualCacheRecord | None:
        raw = self._rows().get(cache_key)
        return self._record(raw) if raw is not None else None

    def put(self, record: _VisualCacheRecord) -> None:
        rows = self._rows()
        rows[record.cache_key] = asdict(record)
        temporary = self._path.with_suffix(self._path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
        temporary.replace(self._path)


class _VisualAssetCache:
    """Content-addressed blobs plus replaceable cache-key metadata index."""

    def __init__(
        self,
        store: ObjectStore | None = None,
        index: _VisualCacheIndex | None = None,
    ) -> None:
        self.store = store or InMemoryObjectStore()
        self.index = index or _InMemoryVisualCacheIndex()

    def get(
        self,
        cache_key: str,
        *,
        rights: str = "public",
    ) -> tuple[_SceneVisualAsset, AssetRef] | None:
        metadata = self.index.get(cache_key)
        if metadata is None:
            return None
        ref = AssetRef(
            asset_id=metadata.asset_id,
            content_hash=metadata.content_sha256,
            size=metadata.size,
            content_type=metadata.media_type,
            rights=rights,
        )
        content = self.store.get(ref)
        return (
            _SceneVisualAsset(
                scene_key=metadata.scene_key,
                place_name=metadata.place_name,
                provider_id=metadata.provider_id,
                media_type=metadata.media_type,
                content=content,
                content_sha256=metadata.content_sha256,
                cache_key=metadata.cache_key,
                illustrative=metadata.illustrative,
                style_key=metadata.style_key,
                provider_version=metadata.provider_version,
            ),
            ref,
        )

    def put(self, asset: _SceneVisualAsset, *, rights: str = "public") -> AssetRef:
        ref = self.store.put(asset.content, content_type=asset.media_type, rights=rights)
        self.index.put(
            _VisualCacheRecord(
                cache_key=asset.cache_key,
                scene_key=asset.scene_key,
                place_name=asset.place_name,
                provider_id=asset.provider_id,
                provider_version=asset.provider_version,
                media_type=asset.media_type,
                content_sha256=asset.content_sha256,
                asset_id=ref.asset_id,
                size=ref.size,
                illustrative=asset.illustrative,
                style_key=asset.style_key,
            )
        )
        return ref


def _materialize_visual_plan(
    plan: _SourceVisualPlan,
    provider: _SceneImageProvider | None = None,
    *,
    cache: _VisualAssetCache | None = None,
    allow_network: bool = False,
    max_cost_units: int = 0,
    rights: str | None = None,
    private_source: bool = False,
) -> _VisualMaterialization:
    """Generate only cache misses, under explicit network/cost governance."""
    if plan.status not in {"READY_FOR_ASSET_PROVIDER", "BUDGET_ZERO"}:
        return _VisualMaterialization((), (), 0, 0, 0)

    selected_provider = provider or _ProceduralSvgSceneProvider()
    if selected_provider.requires_network and not allow_network:
        raise ValueError("network visual provider requires explicit allow_network")
    if selected_provider.requires_network and not plan.external_processing_allowed:
        raise ValueError("source rights do not allow external visual processing")
    if private_source and not selected_provider.private_safe:
        raise ValueError("private source requires a private-safe visual provider")

    asset_cache = cache or _VisualAssetCache()
    delivery_rights = rights or plan.delivery_rights
    resolved_assets: list[_SceneVisualAsset] = []
    resolved_refs: list[AssetRef] = []
    misses: list[_SourceSceneRequest] = []
    cached_rows: dict[str, tuple[_SceneVisualAsset, AssetRef]] = {}

    for request in plan.scene_requests:
        provider_cache_key = (
            f"{request.cache_key}:{selected_provider.provider_id}@"
            f"{selected_provider.provider_version}"
        )
        cached = asset_cache.get(provider_cache_key, rights=delivery_rights)
        if cached is None:
            misses.append(request)
        else:
            cached_rows[request.stable_key] = cached

    expected_cost = selected_provider.cost_units_per_asset * len(misses)
    if expected_cost > max_cost_units:
        raise ValueError(f"visual provider cost {expected_cost} exceeds budget {max_cost_units}")

    generated: dict[str, tuple[_SceneVisualAsset, AssetRef]] = {}
    for request in misses:
        asset = selected_provider.produce(request)
        expected_cache_key = (
            f"{request.cache_key}:{selected_provider.provider_id}@"
            f"{selected_provider.provider_version}"
        )
        if asset.provider_id != selected_provider.provider_id:
            raise ValueError("visual provider returned mismatched provider_id")
        if asset.cache_key != expected_cache_key:
            raise ValueError("visual provider returned mismatched cache_key")
        if hashlib.sha256(asset.content).hexdigest() != asset.content_sha256:
            raise ValueError("visual provider returned invalid content digest")
        ref = asset_cache.put(asset, rights=delivery_rights)
        generated[request.stable_key] = (asset, ref)

    for request in plan.scene_requests:
        asset, ref = cached_rows.get(request.stable_key) or generated[request.stable_key]
        resolved_assets.append(asset)
        resolved_refs.append(ref)

    return _VisualMaterialization(
        assets=tuple(resolved_assets),
        asset_refs=tuple(resolved_refs),
        provider_calls=len(misses),
        cache_hits=len(plan.scene_requests) - len(misses),
        cost_units=expected_cost,
    )


def _render_visual_plan(
    plan: _SourceVisualPlan,
    provider: _SceneImageProvider | None = None,
    *,
    allow_network: bool = False,
    max_cost_units: int = 0,
    private_source: bool = False,
) -> tuple[_SceneVisualAsset, ...]:
    """Compatibility helper returning generated assets without exposing cache details."""
    return _materialize_visual_plan(
        plan,
        provider,
        allow_network=allow_network,
        max_cost_units=max_cost_units,
        private_source=private_source,
    ).assets
