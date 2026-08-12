"""Observation visibility component schema (versioned)."""

from __future__ import annotations

from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

OBSERVATION_SCHEMA_VERSION = SchemaVersion(1)

OBSERVATION_VISIBILITY_COMPONENT = "observation.visibility"
ANNOUNCEMENT_COMPONENT = "observation.announcement"


def visibility_component(
    entity_id: EntityId, level: str, group_id: EntityId | None = None
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"obs_vis_{entity_id.value}"),
        component_type=OBSERVATION_VISIBILITY_COMPONENT,
        schema_version=OBSERVATION_SCHEMA_VERSION,
        fields={
            "entity_id": entity_id.value,
            "level": level,
            "group_id": group_id.value if group_id else None,
        },
    )


def announcement_component(
    actor_id: EntityId, message: str, place_id: EntityId, visibility: str = "public"
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"ann_{actor_id.value}_{place_id.value}"),
        component_type=ANNOUNCEMENT_COMPONENT,
        schema_version=OBSERVATION_SCHEMA_VERSION,
        fields={
            "actor_id": actor_id.value,
            "message": message,
            "place_id": place_id.value,
            "visibility": visibility,
        },
    )
