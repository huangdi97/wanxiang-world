"""Player-safe projections over canonical state and committed history.

The projection deliberately removes implementation references. It is a read
model only: package metadata, canonical state, and committed events are the
only inputs, and no projection value can be written back to the world.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from collections.abc import Iterable

from wanxiang_domain.event import CommittedEvent
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.assets.book_scene_plan import _plan_book_scene_assets
from wanxiang_substrate.assets.book_scene_visual import (
    _render_visual_plan,
    _render_world_atlas,
    _SceneVisualAsset,
)
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.player_i18n import _copy_for
from wanxiang_substrate.playable.player_projection_support import (
    _change_card,
    _chronicle_card,
    _entity_fields,
    _entity_name,
    _event_card,
    _first_text,
    _first_text_from_entities,
    _is_person,
    _memory_cards,
    _actor_owned_entities,
    _narrative,
    _opportunity_cards,
    _person_card,
    _relation_card,
    _status_label,
)
from wanxiang_substrate.playable.state_diff import CommittedStateDiff


def _scene_clues_for_assets(
    package: WorldPackageDraft,
    assets: tuple[_SceneVisualAsset, ...],
) -> dict[str, tuple[str, ...]]:
    """Recover source clues for generated/deferred assets without provider calls."""

    clues: dict[str, tuple[str, ...]] = {}
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
            clues[asset.scene_key] = request.context_candidates
    return clues


def player_world_detail(
    profile: PlayableWorldProfile,
    package: WorldPackageDraft | None = None,
    *,
    locale: str | None = None,
    include_visual: bool = False,
    visual_assets: tuple[_SceneVisualAsset, ...] | None = None,
    visual_access_allowed: bool = True,
) -> dict[str, object]:
    """Return the detail copy used before a player enters a world."""

    copy = _copy_for(locale)
    # An unavailable source-derived visual entitlement also suppresses draft
    # location/context metadata. Public profile copy remains separate.
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
        clues_by_key = _scene_clues_for_assets(package, assets)
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
                    "clues": list(clues_by_key.get(asset.scene_key, ())),
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


def player_observation(
    profile: PlayableWorldProfile,
    package: WorldPackageDraft | None,
    state: InMemoryCanonicalState,
    events: Iterable[CommittedEvent],
    *,
    actor_id: str = "",
    actor_name: str = "",
    actor_starting_location: str = "",
    diff: CommittedStateDiff | None = None,
    locale: str | None = None,
    events_since_revision: int | None = None,
    visual_assets: tuple[_SceneVisualAsset, ...] | None = None,
    visual_access_allowed: bool = True,
) -> dict[str, object]:
    """Project one observation without exposing IDs, hashes, or raw payloads."""

    copy = _copy_for(locale)
    event_list = tuple(events)
    entities = state.entities()
    names = {entity.entity_id.value: _entity_name(entity, copy) for entity in entities}
    world = player_world_detail(
        profile, package, locale=copy.locale, visual_access_allowed=visual_access_allowed
    )
    setting = world["setting"]
    assert isinstance(setting, dict)
    relations = [_relation_card(item, names, actor_id, copy) for item in state.relations()]
    actor = next((item for item in entities if item.entity_id.value == actor_id), None)
    actor_fields = _entity_fields(actor)
    # The actor's position is not the location of an arbitrary world entity.
    canonical_location = _first_text(actor_fields, ("location", "place"))
    location = canonical_location or actor_starting_location or None
    known_people = [_person_card(entity, copy) for entity in entities if _is_person(entity)]
    # Only explicit co-location is sufficient to call someone "present".
    people = [person for person in known_people if location and person["location"] == location]
    environment = _first_text_from_entities(entities, ("environment", "setting"))
    weather = _first_text_from_entities(entities, ("weather", "climate"))
    current_event = _event_card(entities, names, copy)
    opportunities = _opportunity_cards(entities, copy)
    memories = _memory_cards(entities, actor_id)
    chronicle = [_chronicle_card(event, names, actor_id, copy) for event in event_list[-6:]]
    events_since_leave = [
        _chronicle_card(event, names, actor_id, copy)
        for event in event_list
        if events_since_revision is not None and event.event_seq.value > events_since_revision
    ]
    changes = [_change_card(change, names, copy) for change in (diff.changes if diff else ())]
    world_time = event_list[-1].world_time.ticks if event_list else 0
    player = {
        "name": actor_name or (_entity_name(actor, copy) if actor else copy.text("your_character")),
        "status": _status_label(actor_fields, copy),
        "location": _first_text(actor_fields, ("location", "place"))
        or actor_starting_location
        or None,
        "items": _actor_owned_entities(
            entities, {"item", "object", "material"}, copy, actor_id
        ),
        "goals": _actor_owned_entities(
            entities, {"task", "opportunity", "challenge"}, copy, actor_id
        ),
        "relations": [dict(item) for item in relations if item.get("involves_actor") is True],
        "memories": memories,
    }
    for item in relations:
        item.pop("involves_actor", None)
    scene_visual: dict[str, object] | None = None
    if package is not None and visual_access_allowed:
        plan = _plan_book_scene_assets(package)
        assets = visual_assets
        if assets is None:
            assets = _render_visual_plan(plan)
        clues_by_key = _scene_clues_for_assets(package, assets)
        chosen = next((asset for asset in assets if asset.place_name == location), None)
        grounding = "current_location" if canonical_location else "entry_location"
        if chosen is None and assets:
            chosen = assets[0]
            grounding = "world_preview"
        if chosen is not None:
            scene_visual = {
                "grounding": grounding,
                "place_name": chosen.place_name,
                "media_type": chosen.media_type,
                "data_uri": chosen.data_uri(),
                "content_sha256": chosen.content_sha256,
                "illustrative": chosen.illustrative,
                "clues": list(clues_by_key.get(chosen.scene_key, ())),
            }

    return {
        "world": world,
        "region": setting["region"],
        "visual_scene": scene_visual,
        "time": {"ticks": world_time},
        "location": location,
        "environment": environment,
        "weather": weather,
        "current_event": current_event,
        "present_people": people,
        "known_people": known_people,
        "opportunities": opportunities,
        "narrative": _narrative(current_event, actor_name, copy),
        "player": player,
        "relations": relations,
        "memories": memories,
        "recent_changes": changes,
        "chronicle": chronicle,
        "last_committed_change": chronicle[-1] if chronicle else None,
        "events_since_leave": events_since_leave,
    }
