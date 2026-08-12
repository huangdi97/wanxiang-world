"""Body/condition component schema (versioned) on the M1 component model."""

from __future__ import annotations

from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

BODY_SCHEMA_VERSION = SchemaVersion(1)

BODY_CONDITION_COMPONENT = "body.condition"
MEDICATION_COMPONENT = "body.medication"
CONDITION_VISIBILITY_COMPONENT = "body.condition_visibility"


def condition_component(
    health: int = 100,
    energy: int = 100,
    sleep: int = 100,
    pain: int = 0,
    mobility: int = 100,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId("body_condition"),
        component_type=BODY_CONDITION_COMPONENT,
        schema_version=BODY_SCHEMA_VERSION,
        fields={
            "health": health,
            "energy": energy,
            "sleep": sleep,
            "pain": pain,
            "mobility": mobility,
        },
    )


def medication_component(
    medication_id: EntityId, effect: str, actor_id: EntityId, active: bool = True
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"med_{medication_id.value}"),
        component_type=MEDICATION_COMPONENT,
        schema_version=BODY_SCHEMA_VERSION,
        fields={
            "medication_id": medication_id.value,
            "effect": effect,
            "actor_id": actor_id.value,
            "active": active,
        },
    )


def condition_visibility_component(private_facets: tuple[str, ...]) -> ComponentData:
    return ComponentData(
        component_id=ComponentId("condition_visibility"),
        component_type=CONDITION_VISIBILITY_COMPONENT,
        schema_version=BODY_SCHEMA_VERSION,
        fields={"private": ",".join(private_facets)},
    )
