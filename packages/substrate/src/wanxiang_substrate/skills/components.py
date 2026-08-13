"""Skill instance component schema (versioned)."""

from __future__ import annotations

from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

SKILL_SCHEMA_VERSION = SchemaVersion(1)

SKILL_INSTANCE_COMPONENT = "skill.instance"


def skill_instance_component(
    instance_id: EntityId,
    skill_id: EntityId,
    actor_id: EntityId,
    state: str = "idle",
    current_step_index: int = 0,
    completed_steps: tuple[str, ...] = (),
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"skill_{instance_id.value}"),
        component_type=SKILL_INSTANCE_COMPONENT,
        schema_version=SKILL_SCHEMA_VERSION,
        fields={
            "instance_id": instance_id.value,
            "skill_id": skill_id.value,
            "actor_id": actor_id.value,
            "state": state,
            "current_step_index": current_step_index,
            "completed_steps": ",".join(completed_steps),
        },
    )
