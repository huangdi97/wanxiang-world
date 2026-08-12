"""Material component schema (versioned) on the M1 component model."""

from __future__ import annotations

from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

MATERIAL_SCHEMA_VERSION = SchemaVersion(1)

ITEM_COMPONENT = "material.item"
CONTAINER_COMPONENT = "material.container"
CUSTODY_COMPONENT = "material.custody"
OWNERSHIP_COMPONENT = "material.ownership"
CONTAINED_COMPONENT = "material.contained"
INFO_PAYLOAD_COMPONENT = "material.info_payload"


def item_component(item_id: EntityId, kind: str, state: str = "intact") -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"item_{item_id.value}"),
        component_type=ITEM_COMPONENT,
        schema_version=MATERIAL_SCHEMA_VERSION,
        fields={"item_id": item_id.value, "kind": kind, "state": state},
    )


def container_component(
    container_id: EntityId, capacity: int, accepts_kinds: tuple[str, ...] = ()
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"container_{container_id.value}"),
        component_type=CONTAINER_COMPONENT,
        schema_version=MATERIAL_SCHEMA_VERSION,
        fields={
            "container_id": container_id.value,
            "capacity": capacity,
            "accepts": ",".join(accepts_kinds),
        },
    )


def custody_component(item_id: EntityId, custodian_id: EntityId) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"custody_{item_id.value}"),
        component_type=CUSTODY_COMPONENT,
        schema_version=MATERIAL_SCHEMA_VERSION,
        fields={"item_id": item_id.value, "custodian_id": custodian_id.value},
    )


def ownership_component(item_id: EntityId, owner_id: EntityId) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"owner_{item_id.value}"),
        component_type=OWNERSHIP_COMPONENT,
        schema_version=MATERIAL_SCHEMA_VERSION,
        fields={"item_id": item_id.value, "owner_id": owner_id.value},
    )


def contained_component(item_id: EntityId, container_id: EntityId) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"in_{item_id.value}"),
        component_type=CONTAINED_COMPONENT,
        schema_version=MATERIAL_SCHEMA_VERSION,
        fields={"item_id": item_id.value, "container_id": container_id.value},
    )


def info_payload_component(
    item_id: EntityId, payload_ref: str, state: str = "sealed"
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"payload_{item_id.value}"),
        component_type=INFO_PAYLOAD_COMPONENT,
        schema_version=MATERIAL_SCHEMA_VERSION,
        fields={
            "item_id": item_id.value,
            "payload_ref": payload_ref,
            "state": state,
            "readers": "",
        },
    )
