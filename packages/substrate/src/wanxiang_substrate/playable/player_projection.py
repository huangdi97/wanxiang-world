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
    _SceneVisualAsset,
)
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.playable.models import PlayableWorldProfile
from wanxiang_substrate.playable.player_i18n import _copy_for
from wanxiang_substrate.playable.player_projection_support import (
    _actor_owned_entities,
    _actor_relation_cards,
    _change_card,
    _chronicle_card,
    _entity_fields,
    _entity_name,
    _event_card,
    _first_text,
    _first_text_from_entities,
    _is_person,
    _known_people_cards,
    _memory_cards,
    _narrative,
    _opportunity_cards,
    _person_card,
    _relation_card,
    _status_label,
)
from wanxiang_substrate.playable.player_spatial_projection import (
    _spatial_capability,
    _SpatialAssetMap,
    _SpatialProjectionFrameMap,
)
from wanxiang_substrate.playable.player_world_detail import (
    _scene_support_for_assets,
    player_world_detail,
)
from wanxiang_substrate.playable.state_diff import CommittedStateDiff


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
    spatial_assets: _SpatialAssetMap | None = None,
    spatial_frames: _SpatialProjectionFrameMap | None = None,
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
    state_relations = state.relations()
    relations = [_relation_card(item, names, actor_id, copy) for item in state_relations]
    actor = next((item for item in entities if item.entity_id.value == actor_id), None)
    actor_fields = _entity_fields(actor)
    canonical_location = _first_text(actor_fields, ("location", "place"))
    location = canonical_location or actor_starting_location or None
    person_entities = tuple(entity for entity in entities if _is_person(entity))
    person_cards = [_person_card(entity, copy) for entity in person_entities]
    people = [person for person in person_cards if location and person["location"] == location]
    known_people = _known_people_cards(person_entities, state_relations, actor_id, location, copy)
    environment = _first_text_from_entities(entities, ("environment", "setting"))
    weather = _first_text_from_entities(entities, ("weather", "climate"))
    current_event = _event_card(entities, names, copy, actor_id)
    opportunities = _opportunity_cards(entities, copy, actor_id)
    memories = _memory_cards(entities, actor_id)
    chronicle = [_chronicle_card(event, actor_id, copy) for event in event_list[-6:]]
    events_since_leave = [
        _chronicle_card(event, actor_id, copy)
        for event in event_list
        if events_since_revision is not None and event.revision.value > events_since_revision
    ]
    changes = [_change_card(change, names, copy) for change in (diff.changes if diff else ())]
    world_time = event_list[-1].world_time.ticks if event_list else 0
    actor_relations = _actor_relation_cards(relations)
    player = {
        "name": actor_name or (_entity_name(actor, copy) if actor else copy.text("your_character")),
        "status": _status_label(actor_fields, copy),
        "location": _first_text(actor_fields, ("location", "place"))
        or actor_starting_location
        or None,
        "items": _actor_owned_entities(entities, {"item", "object", "material"}, copy, actor_id),
        "goals": _actor_owned_entities(
            entities, {"task", "opportunity", "challenge"}, copy, actor_id
        ),
        "relations": actor_relations,
        "memories": memories,
    }
    scene_visual: dict[str, object] | None = None
    if package is not None and visual_access_allowed:
        plan = _plan_book_scene_assets(package)
        assets = visual_assets
        if assets is None:
            assets = _render_visual_plan(plan)
        support_by_key = _scene_support_for_assets(package, assets)
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
                "provider_id": chosen.provider_id,
                "provider_version": chosen.provider_version,
                "presentation_kind": chosen.presentation_kind,
                "clues": list(support_by_key.get(chosen.scene_key, ((), 0))[0]),
                "source_evidence_count": support_by_key.get(chosen.scene_key, ((), 0))[1],
                "spatial": _spatial_capability(
                    chosen.scene_key,
                    spatial_assets,
                    spatial_frames,
                ),
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
        "relations": actor_relations,
        "memories": memories,
        "recent_changes": changes,
        "chronicle": chronicle,
        "last_committed_change": chronicle[-1] if chronicle else None,
        "events_since_leave": events_since_leave,
    }
