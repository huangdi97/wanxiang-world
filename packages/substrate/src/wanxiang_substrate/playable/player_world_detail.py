"""Player-safe world detail projection used before a player enters a world.

The projection is a read model over the source-derived package draft and the
derived visual catalog. It never writes back to canonical state or History.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.assets.book_scene_visual import (
    _render_visual_plan,
    _render_world_atlas,
    _SceneVisualAsset,
)
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.player_i18n import _copy_for
from wanxiang_substrate.playable.player_spatial_projection import (
    _spatial_capability,
    _SpatialAssetMap,
    _SpatialProjectionFrameMap,
)


def _scene_support_for_assets(
    package: WorldPackageDraft,
    assets: tuple[_SceneVisualAsset, ...],
) -> dict[str, tuple[tuple[str, ...], int]]:
    """Recover safe source support without exposing raw locators to Player."""

    support: dict[str, tuple[tuple[str, ...], int]] = {}
    for asset in assets:
        targeted = _plan_book_scene_assets(
            package,
            max_preview_scenes=1,
            preferred_places=(asset.place_name,),
        )
        request = next(
            (
                item
                for item in targeted.scene_requests
                if item.stable_key == asset.scene_key and item.place_name == asset.place_name
            ),
            None,
        )
        if request is not None:
            support[asset.scene_key] = (request.context_candidates, len(request.source_refs))
    return support


def player_world_detail(
    profile: PlayableWorldProfile,
    package: WorldPackageDraft | None = None,
    *,
    locale: str | None = None,
    include_visual: bool = False,
    visual_assets: tuple[_SceneVisualAsset, ...] | None = None,
    spatial_assets: _SpatialAssetMap | None = None,
    spatial_frames: _SpatialProjectionFrameMap | None = None,
    visual_access_allowed: bool = True,
) -> dict[str, object]:
    """Return the detail copy used before a player enters a world."""

    copy = _copy_for(locale)
    # Visual entitlement also gates source-derived draft context.
    draft = package.draft if package is not None and visual_access_allowed else None
    places = tuple(getattr(draft, "places", ()) or ())
    metadata = draft.compiler_metadata if draft is not None else {}

    def draft_text(*keys: str) -> str | None:
        for key in keys:
            value = metadata.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return None

    character_count = len(tuple(getattr(draft, "character_profiles", ()) or ()))
    if not character_count:
        character_count = len(tuple(getattr(draft, "entities", ()) or ()))
    visual: dict[str, object] | None = None
    if include_visual and package is not None and visual_access_allowed:
        plan = _plan_book_scene_assets(package)
        assets = visual_assets
        if assets is None:
            assets = _render_visual_plan(plan)
        support_by_key = _scene_support_for_assets(package, assets)
        generated_places = {asset.place_name for asset in assets}
        atlas = _render_world_atlas(plan)
        visual = {
            "status": plan.status,
            "places": [
                {"name": place, "generated": place in generated_places}
                for place in plan.place_names
            ],
            "atlas": (
                {
                    "kind": "atlas",
                    "place_name": atlas.place_name,
                    "media_type": atlas.media_type,
                    "data_uri": atlas.data_uri(),
                    "content_sha256": atlas.content_sha256,
                    "illustrative": atlas.illustrative,
                }
                if atlas is not None
                else None
            ),
            "scenes": [
                {
                    "place_name": asset.place_name,
                    "media_type": asset.media_type,
                    "data_uri": asset.data_uri(),
                    "content_sha256": asset.content_sha256,
                    "illustrative": asset.illustrative,
                    "provider_id": asset.provider_id,
                    "provider_version": asset.provider_version,
                    "presentation_kind": asset.presentation_kind,
                    "clues": list(support_by_key.get(asset.scene_key, ((), 0))[0]),
                    "source_evidence_count": support_by_key.get(asset.scene_key, ((), 0))[1],
                    "spatial": _spatial_capability(
                        asset.scene_key,
                        spatial_assets,
                        spatial_frames,
                    ),
                }
                for asset in assets
            ],
            "topology": [
                {
                    "from": relation.source_place,
                    "to": relation.target_place,
                    "relation_type": relation.relation_type,
                    "confidence": relation.confidence,
                }
                for relation in plan.topology_relations
            ],
        }

    return {
        "profile_id": profile.profile_id,
        "name": profile.display_name or copy.text("default_world_name"),
        "description": profile.description or copy.text("default_world_description"),
        "tags": list(profile.tags),
        "status": copy.text("world_ready"),
        "mode": copy.text("mode_character"),
        "counts": {
            "characters": character_count,
            "events": len(tuple(getattr(draft, "events", ()) or ())),
        },
        "scenario": {
            "name": profile.scenario_name or copy.text("default_scenario_name"),
            "opening": profile.opening_hint or copy.text("default_opening"),
        },
        "visual": visual,
        "setting": {
            "region": draft_text("region", "world_region"),
            "location": places[0] if places else None,
            "era": draft_text("era", "period", "historical_period"),
            "environment": draft_text("environment", "setting", "world_environment"),
            "time": draft_text("time", "world_time", "scenario_initial_time"),
            "happening": draft_text("happening", "current_event", "opening_event"),
        },
    }
