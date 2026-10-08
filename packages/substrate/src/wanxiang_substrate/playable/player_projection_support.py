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


def _status_label(fields: dict[str, FieldValue], copy: _PlayerCopy) -> str | None:
    value = _first_text(fields, ("status.value", "status"))
    return copy.text(_STATUS_KEYS[value]) if value in _STATUS_KEYS else value


def _person_card(entity: EntityState, copy: _PlayerCopy) -> dict[str, object]:
    fields = _entity_fields(entity)
    return {
        "name": _entity_name(entity, copy),
        "role": _first_text(fields, ("role", "occupation")),
        "status": _status_label(fields, copy),
        "location": _first_text(fields, ("location", "place")),
    }


def _relation_card(
    relation: Any, names: dict[str, str], actor_id: str, copy: _PlayerCopy
) -> dict[str, object]:
    return {
        "from": names.get(relation.source_id.value, copy.text("relation_someone")),
        "to": names.get(relation.target_id.value, copy.text("relation_someone")),
        "label": relation.relation_type,
        "involves_actor": actor_id in {relation.source_id.value, relation.target_id.value},
    }


def _event_card(
    entities: tuple[EntityState, ...], names: dict[str, str], copy: _PlayerCopy
) -> dict[str, object] | None:
    for entity in entities:
        if entity.entity_type.casefold() in {"event", "task", "opportunity", "challenge"}:
            fields = _entity_fields(entity)
            return {
                "name": _entity_name(entity, copy),
                "description": _first_text(fields, ("description", "summary", "text")),
                "status": _status_label(fields, copy),
            }
    _ = names
    return None


def _opportunity_cards(
    entities: tuple[EntityState, ...], copy: _PlayerCopy
) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for entity in entities:
        if entity.entity_type.casefold() in {"task", "opportunity", "challenge"}:
            fields = _entity_fields(entity)
            result.append(
                {
                    "name": _entity_name(entity, copy),
                    "status": _status_label(fields, copy),
                    "description": _first_text(fields, ("description", "summary", "text")),
                }
            )
    return result


def _memory_cards(entities: tuple[EntityState, ...], actor_id: str) -> list[str]:
    result: list[str] = []
    for entity in entities:
        kinds = {entity.entity_type.casefold()}
        kinds.update(
            component.component_type.casefold() for component in entity.components.values()
        )
        if not any("memory" in kind or "knowledge" in kind or "belief" in kind for kind in kinds):
            continue
        fields = _entity_fields(entity)
        owner = _first_text(fields, ("actor_id", "owner_id"))
        if owner and owner != actor_id:
            continue
        text = _first_text(fields, ("content", "text", "summary", "description"))
        if text:
            result.append(text)
    return result


def _named_entities(
    entities: tuple[EntityState, ...], types: set[str], copy: _PlayerCopy
) -> list[str]:
    return [
        _entity_name(entity, copy) for entity in entities if entity.entity_type.casefold() in types
    ]


def _chronicle_card(
    event: CommittedEvent, names: dict[str, str], actor_id: str, copy: _PlayerCopy
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
    _ = names
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
