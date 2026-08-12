"""Spatial component schema (versioned) mapped onto the M1 component model.

Spatial state rides on existing versioned entity components; no new persisted
table is required, so M1 event replay is untouched.
"""

from __future__ import annotations

from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

SPATIAL_SCHEMA_VERSION = SchemaVersion(1)

REGION_COMPONENT = "spatial.region"
PLACE_COMPONENT = "spatial.place"
PORTAL_COMPONENT = "spatial.portal"
POSITION_COMPONENT = "spatial.position"
ACCESS_KEY_COMPONENT = "spatial.access_key"
PLACE_GRANT_COMPONENT = "spatial.place_grant"


def region_component(name: str) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"cmp_region_{name}"),
        component_type=REGION_COMPONENT,
        schema_version=SPATIAL_SCHEMA_VERSION,
        fields={"name": name},
    )


def place_component(
    region_id: EntityId,
    name: str,
    capacity: int | None = None,
    privacy: str = "public",
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"cmp_place_{name}"),
        component_type=PLACE_COMPONENT,
        schema_version=SPATIAL_SCHEMA_VERSION,
        fields={
            "region_id": region_id.value,
            "name": name,
            "capacity": capacity,
            "privacy": privacy,
        },
    )


def portal_component(
    endpoint_a: EntityId,
    endpoint_b: EntityId,
    state: str = "open",
    locked_key: EntityId | None = None,
    label: str | None = None,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"cmp_portal_{endpoint_a.value}_{endpoint_b.value}"),
        component_type=PORTAL_COMPONENT,
        schema_version=SPATIAL_SCHEMA_VERSION,
        fields={
            "endpoint_a": endpoint_a.value,
            "endpoint_b": endpoint_b.value,
            "state": state,
            "locked_key": locked_key.value if locked_key else None,
            "label": label,
        },
    )


def position_component(entity_id: EntityId, place_id: EntityId) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"pos_{entity_id.value}"),
        component_type=POSITION_COMPONENT,
        schema_version=SPATIAL_SCHEMA_VERSION,
        fields={"place_id": place_id.value},
    )


def access_key_component(key_id: EntityId) -> ComponentData:
    """Component marking that an actor holds the given key entity."""
    return ComponentData(
        component_id=ComponentId(f"hold_key_{key_id.value}"),
        component_type=ACCESS_KEY_COMPONENT,
        schema_version=SPATIAL_SCHEMA_VERSION,
        fields={"key_id": key_id.value},
    )


def place_grant_component(place_id: EntityId) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"grant_{place_id.value}"),
        component_type=PLACE_GRANT_COMPONENT,
        schema_version=SPATIAL_SCHEMA_VERSION,
        fields={"place_id": place_id.value},
    )
