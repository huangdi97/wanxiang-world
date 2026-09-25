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
    _named_entities,
    _narrative,
    _opportunity_cards,
    _person_card,
    _relation_card,
    _status_label,
)
from wanxiang_substrate.playable.state_diff import CommittedStateDiff


def player_world_detail(
    profile: PlayableWorldProfile,
    package: WorldPackageDraft | None = None,
    *,
    locale: str | None = None,
) -> dict[str, object]:
    """Return the detail copy used before a player enters a world."""

    copy = _copy_for(locale)
    draft = package.draft if package is not None else None
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
    diff: CommittedStateDiff | None = None,
    locale: str | None = None,
    events_since_revision: int | None = None,
) -> dict[str, object]:
    """Project one observation without exposing IDs, hashes, or raw payloads."""

    copy = _copy_for(locale)
    event_list = tuple(events)
    entities = state.entities()
    names = {entity.entity_id.value: _entity_name(entity, copy) for entity in entities}
    world = player_world_detail(profile, package, locale=copy.locale)
    setting = world["setting"]
    assert isinstance(setting, dict)
    people = [_person_card(entity, copy) for entity in entities if _is_person(entity)]
    relations = [_relation_card(item, names, actor_id, copy) for item in state.relations()]
    actor = next((item for item in entities if item.entity_id.value == actor_id), None)
    actor_fields = _entity_fields(actor)
    location = _first_text(actor_fields, ("location", "place")) or _first_text_from_entities(
        entities, ("location", "place")
    )
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
        "location": _first_text(actor_fields, ("location", "place")),
        "items": _named_entities(entities, {"item", "object", "material"}, copy),
        "goals": _named_entities(entities, {"task", "opportunity", "challenge"}, copy),
        "relations": [dict(item) for item in relations if item.get("involves_actor") is True],
        "memories": memories,
    }
    for item in relations:
        item.pop("involves_actor", None)
    return {
        "world": world,
        "region": setting["region"],
        "time": {"ticks": world_time},
        "location": location,
        "environment": environment,
        "weather": weather,
        "current_event": current_event,
        "present_people": people,
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
