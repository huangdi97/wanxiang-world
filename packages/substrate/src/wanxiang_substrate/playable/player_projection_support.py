"""Localized field and event helpers for the Player projection."""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import Any

from wanxiang_domain.delta import (
    EntityCreate,
    EntityDelete,
    EntityUpdate,
    RelationCreate,
    RelationDelete,
)
from wanxiang_domain.entity import EntityState, FieldValue
from wanxiang_domain.event import CommittedEvent

from wanxiang_substrate.assets.book_scene_context import _place_identity

from wanxiang_substrate.playable.player_i18n import _PlayerCopy
from wanxiang_substrate.playable.state_diff import DiffChange

_STATUS_KEYS = {
    "awake": "status_awake",
    "alert": "status_alert",
    "resting": "status_resting",
    "calm": "status_calm",
    "tense": "status_tense",
}
_CATEGORY_KEYS = {
    "actor": "category_actor",
    "location": "category_location",
    "relation": "category_relation",
    "item": "category_item",
    "task": "category_task",
    "knowledge": "category_knowledge",
    "organization": "category_organization",
    "family": "category_organization",
    "state": "category_state",
}


def _entity_fields(entity: EntityState | None) -> dict[str, FieldValue]:
    if entity is None:
        return {}
    fields: dict[str, FieldValue] = {}
    for component in entity.components.values():
        for key, value in component.fields.items():
            fields[f"{component.component_type}.{key}".casefold()] = value
    return fields


def _entity_name(entity: EntityState | None, copy: _PlayerCopy) -> str:
    if entity is None:
        return copy.text("entity_world")
    fields = _entity_fields(entity)
    value = _first_text(fields, ("display_name", "name", "title"))
    if value:
        return value
    return (
        copy.text("entity_person")
        if _is_person(entity)
        else copy.text(_CATEGORY_KEYS.get(entity.entity_type, "entity_world"))
    )


def _is_person(entity: EntityState) -> bool:
    names = {entity.entity_type.casefold()}
    names.update(component.component_type.casefold() for component in entity.components.values())
    return bool(names & {"actor", "person", "character", "agent"})


def _first_text(fields: dict[str, FieldValue], tokens: tuple[str, ...]) -> str | None:
    for key, value in fields.items():
        if any(token in key for token in tokens) and isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _first_text_from_entities(
    entities: tuple[EntityState, ...], tokens: tuple[str, ...]
) -> str | None:
    for entity in entities:
        value = _first_text(_entity_fields(entity), tokens)
        if value:
            return value
    return None


_LOCATION_LEAVES = {"location", "current_location", "place", "current_place"}


def _location_text(fields: dict[str, FieldValue]) -> str | None:
    """Exact leaf names only: place_of_birth must never claim current presence."""
    for key, value in fields.items():
        leaf = key.rsplit(".", 1)[-1]
        if leaf in _LOCATION_LEAVES and isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _status_label(fields: dict[str, FieldValue], copy: _PlayerCopy) -> str | None:
    value = _first_text(fields, ("status.value", "status"))
    return copy.text(_STATUS_KEYS[value]) if value in _STATUS_KEYS else value


def _person_card(entity: EntityState, copy: _PlayerCopy) -> dict[str, object]:
    fields = _entity_fields(entity)
    return {
        "name": _entity_name(entity, copy),
        "role": _first_text(fields, ("role", "occupation")),
        "status": _status_label(fields, copy),
        "location": _location_text(fields),
    }


def _same_location(left: object, right: object) -> bool:
    """Source-equivalent location labels represent one place, never a fuzzy match."""
    return (
        isinstance(left, str)
        and isinstance(right, str)
        and bool(left.strip())
        and bool(right.strip())
        and _place_identity(left) == _place_identity(right)
    )


def _known_people_cards(
    people: tuple[EntityState, ...],
    relations: tuple[Any, ...],
    actor_id: str,
    location: str | None,
    copy: _PlayerCopy,
) -> list[dict[str, object]]:
    """Expose only co-located or actor-related people; remote state stays hidden."""
    present_ids = {
        person.entity_id.value
        for person in people
        if _same_location(_person_card(person, copy)["location"], location)
    }
    related_ids: set[str] = set()
    if actor_id:
        for relation in relations:
            source_id = relation.source_id.value
            target_id = relation.target_id.value
            if source_id == actor_id:
                related_ids.add(target_id)
            elif target_id == actor_id:
                related_ids.add(source_id)
    allowed_ids = present_ids | related_ids
    allowed_ids.discard(actor_id)
    cards: list[dict[str, object]] = []
    for person in people:
        person_id = person.entity_id.value
        if person_id not in allowed_ids:
            continue
        card = _person_card(person, copy)
        if person_id not in present_ids:
            card["location"] = None
            card["status"] = None
        cards.append(card)
    return cards


def _actor_relation_cards(relations: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {key: value for key, value in item.items() if key != "involves_actor"}
        for item in relations
        if item.get("involves_actor") is True
    ]


def _relation_card(
    relation: Any, names: dict[str, str], actor_id: str, copy: _PlayerCopy
) -> dict[str, object]:
    return {
        "from": names.get(relation.source_id.value, copy.text("relation_someone")),
        "to": names.get(relation.target_id.value, copy.text("relation_someone")),
        "label": relation.relation_type,
        "involves_actor": actor_id in {relation.source_id.value, relation.target_id.value},
    }


_OWNER_TOKENS = ("actor_id", "owner_id", "holder_id", "assignee_id")


def _private_owners(entity: EntityState) -> set[str]:
    """All explicit owner fields; conflicting owners must never widen access."""

    fields = _entity_fields(entity)
    return {
        value.strip()
        for key, value in fields.items()
        if any(token in key for token in _OWNER_TOKENS) and isinstance(value, str) and value.strip()
    }


def _visible_to_actor(entity: EntityState, actor_id: str) -> bool:
    """World-level records are public; owner-scoped records belong only to their owner."""

    owners = _private_owners(entity)
    return not owners or (bool(actor_id) and owners == {actor_id})


def _event_card(
    entities: tuple[EntityState, ...],
    names: dict[str, str],
    copy: _PlayerCopy,
    actor_id: str,
) -> dict[str, object] | None:
    """Only a canonical event is a current event; tasks are not happenings."""
    for entity in entities:
        if entity.entity_type.casefold() == "event" and _visible_to_actor(entity, actor_id):
            fields = _entity_fields(entity)
            return {
                "name": _entity_name(entity, copy),
                "description": _first_text(fields, ("description", "summary", "text")),
                "status": _status_label(fields, copy),
            }
    _ = names
    return None


def _opportunity_cards(
    entities: tuple[EntityState, ...],
    copy: _PlayerCopy,
    actor_id: str,
) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for entity in entities:
        if entity.entity_type.casefold() in {
            "task",
            "opportunity",
            "challenge",
        } and _visible_to_actor(entity, actor_id):
            fields = _entity_fields(entity)
            result.append(
                {
                    "name": _entity_name(entity, copy),
                    "status": _status_label(fields, copy),
                    "description": _first_text(fields, ("description", "summary", "text")),
                }
            )
    return result


def _actor_owned_entities(
    entities: tuple[EntityState, ...], types: set[str], copy: _PlayerCopy, actor_id: str
) -> list[str]:
    """A world object is not the player's inventory without explicit ownership."""
    if not actor_id:
        return []
    return [
        _entity_name(entity, copy)
        for entity in entities
        if entity.entity_type.casefold() in types and _private_owners(entity) == {actor_id}
    ]


def _chronicle_card(
    event: CommittedEvent,
    actor_id: str,
    copy: _PlayerCopy,
) -> dict[str, object]:
    operations = event.delta.operations
    summary = copy.text("chronicle_progress")
    if event.actor_id is not None and event.actor_id.value == actor_id:
        summary = copy.text("chronicle_action")
    elif any(isinstance(item, EntityCreate) for item in operations):
        summary = copy.text("chronicle_new_fact")
    elif any(isinstance(item, EntityUpdate) for item in operations):
        summary = copy.text("chronicle_status_change")
    elif any(isinstance(item, RelationCreate) for item in operations):
        summary = copy.text("chronicle_new_relation")
    elif any(isinstance(item, (EntityDelete, RelationDelete)) for item in operations):
        summary = copy.text("chronicle_ended_fact")
    return {"time": event.world_time.ticks, "summary": summary}


def _change_card(change: DiffChange, names: dict[str, str], copy: _PlayerCopy) -> dict[str, object]:
    fields = dict(change.after)
    subject = names.get(change.subject_id, copy.text("entity_world"))
    status = next(
        (value for key, value in fields.items() if key.casefold().endswith("status.value")),
        None,
    )
    category = copy.text(_CATEGORY_KEYS.get(change.category, "category_state"))
    if isinstance(status, str):
        status_key = _STATUS_KEYS.get(status)
        shown_status = copy.text(status_key) if status_key else status
        summary = copy.render("change_status", subject=subject, status=shown_status)
    elif change.kind == "removed":
        summary = copy.render("change_removed", subject=subject, category=category)
    else:
        summary = copy.render("change_updated", subject=subject, category=category)
    return {"kind": change.kind, "category": category, "summary": summary}


def _narrative(current_event: dict[str, object] | None, actor_name: str, copy: _PlayerCopy) -> str:
    if current_event and current_event.get("name"):
        return copy.render("narrative_event", event=current_event["name"])
    if actor_name:
        return copy.render("narrative_actor", actor=actor_name)
    return copy.text("narrative_waiting")
