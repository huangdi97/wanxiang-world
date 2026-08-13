"""Skill resolvers through the M1 authority."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.skills.components import (
    SKILL_INSTANCE_COMPONENT,
    skill_instance_component,
)

ACTION_START_SKILL = "skill.start"
ACTION_SET_SKILL_STATE = "skill.set_state"


def register_skill_resolvers(registry: ResolverRegistry) -> None:
    registry.register(ACTION_START_SKILL, _start_skill)
    registry.register(ACTION_SET_SKILL_STATE, _set_skill_state)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _int(payload: Mapping[str, object], key: str, default: int = 0) -> int:
    value = payload.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be an integer")
    return value


def _start_skill(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    instance_id = EntityId(_str(payload, "instance_id"))
    skill_id = EntityId(_str(payload, "skill_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=instance_id,
                entity_type="skill.instance",
                components=(
                    skill_instance_component(instance_id, skill_id, actor_id, state="idle"),
                ),
            ),
        )
    )


def _set_skill_state(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("set skill state requires current state")
    payload = dict(command.payload)
    instance_id = EntityId(_str(payload, "instance_id"))
    new_state = _str(payload, "state")
    current_index = _int(payload, "current_step_index", 0)
    completed = str(payload.get("completed_steps") or "")
    entity = state.entity(instance_id)
    if entity is None:
        raise ValidationRejected(f"skill instance {instance_id.value} does not exist")
    current = next(
        (c for c in entity.components.values() if c.component_type == SKILL_INSTANCE_COMPONENT),
        None,
    )
    if current is None:
        raise ValidationRejected(f"entity {instance_id.value} is not a skill instance")
    fields = dict(current.fields)
    fields["state"] = new_state
    fields["current_step_index"] = current_index
    fields["completed_steps"] = completed
    updated = ComponentData(
        component_id=current.component_id,
        component_type=SKILL_INSTANCE_COMPONENT,
        schema_version=current.schema_version,
        fields=fields,
    )
    return ProposedWorldDelta(
        operations=(EntityUpdate(entity_id=instance_id, components=(updated,)),)
    )
