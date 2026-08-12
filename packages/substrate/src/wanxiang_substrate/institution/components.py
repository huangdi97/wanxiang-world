"""Institution component schema (versioned) on the M1 component model."""

from __future__ import annotations

from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

INSTITUTION_SCHEMA_VERSION = SchemaVersion(1)

ROLE_COMPONENT = "institution.role"
MEMBERSHIP_COMPONENT = "institution.membership"
PERMISSION_COMPONENT = "institution.permission"
DUTY_COMPONENT = "institution.duty"
SANCTION_COMPONENT = "institution.sanction"


def role_component(role_id: EntityId, name: str, permissions: tuple[str, ...]) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"role_{role_id.value}"),
        component_type=ROLE_COMPONENT,
        schema_version=INSTITUTION_SCHEMA_VERSION,
        fields={"role_id": role_id.value, "name": name, "permissions": ",".join(permissions)},
    )


def membership_component(
    membership_id: EntityId,
    actor_id: EntityId,
    role_id: EntityId,
    institution_id: EntityId,
    start_ticks: int,
    end_ticks: int | None = None,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"membership_{membership_id.value}"),
        component_type=MEMBERSHIP_COMPONENT,
        schema_version=INSTITUTION_SCHEMA_VERSION,
        fields={
            "membership_id": membership_id.value,
            "actor_id": actor_id.value,
            "role_id": role_id.value,
            "institution_id": institution_id.value,
            "start_ticks": start_ticks,
            "end_ticks": end_ticks,
        },
    )


def permission_component(
    permission_id: EntityId,
    actor_id: EntityId,
    permission: str,
    target: str,
    granter_id: EntityId,
    start_ticks: int,
    end_ticks: int | None = None,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"permission_{permission_id.value}"),
        component_type=PERMISSION_COMPONENT,
        schema_version=INSTITUTION_SCHEMA_VERSION,
        fields={
            "permission_id": permission_id.value,
            "actor_id": actor_id.value,
            "permission": permission,
            "target": target,
            "granter_id": granter_id.value,
            "start_ticks": start_ticks,
            "end_ticks": end_ticks,
        },
    )


def duty_component(
    duty_id: EntityId,
    actor_id: EntityId,
    duty_type: str,
    due_ticks: int,
    state: str = "pending",
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"duty_{duty_id.value}"),
        component_type=DUTY_COMPONENT,
        schema_version=INSTITUTION_SCHEMA_VERSION,
        fields={
            "duty_id": duty_id.value,
            "actor_id": actor_id.value,
            "duty_type": duty_type,
            "due_ticks": due_ticks,
            "state": state,
        },
    )


def sanction_component(
    sanction_id: EntityId, actor_id: EntityId, reason: str, ticks: int
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"sanction_{sanction_id.value}"),
        component_type=SANCTION_COMPONENT,
        schema_version=INSTITUTION_SCHEMA_VERSION,
        fields={
            "sanction_id": sanction_id.value,
            "actor_id": actor_id.value,
            "reason": reason,
            "ticks": ticks,
        },
    )
