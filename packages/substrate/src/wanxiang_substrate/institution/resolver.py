"""Institution resolvers: roles/membership/permissions/duties through M1 authority."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.institution.components import (
    DUTY_COMPONENT,
    duty_component,
    membership_component,
    permission_component,
    role_component,
    sanction_component,
)
from wanxiang_substrate.institution.errors import DutyAlreadyComplete
from wanxiang_substrate.institution.query import InstitutionQuery

ACTION_DEFINE_ROLE = "institution.define_role"
ACTION_GRANT_ROLE = "institution.grant_role"
ACTION_GRANT_PERMISSION = "institution.grant_permission"
ACTION_ASSIGN_DUTY = "institution.assign_duty"
ACTION_COMPLETE_DUTY = "institution.complete_duty"
ACTION_APPLY_SANCTION = "institution.apply_sanction"
ACTION_INSTANTIATE = "institution.instantiate"


def register_institution_resolvers(registry: ResolverRegistry) -> None:
    registry.register(ACTION_DEFINE_ROLE, _define_role)
    registry.register(ACTION_GRANT_ROLE, _grant_role)
    registry.register(ACTION_GRANT_PERMISSION, _grant_permission)
    registry.register(ACTION_ASSIGN_DUTY, _assign_duty)
    registry.register(ACTION_COMPLETE_DUTY, _complete_duty)
    registry.register(ACTION_APPLY_SANCTION, _apply_sanction)
    registry.register(ACTION_INSTANTIATE, _instantiate)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _int(payload: Mapping[str, object], key: str, default: int | None = None) -> int | None:
    value = payload.get(key, default)
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be an integer")
    return value


def _define_role(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    role_id = EntityId(_str(payload, "role_id"))
    name = _str(payload, "name")
    permissions_raw = payload.get("permissions")
    permissions = tuple(p for p in str(permissions_raw).split(",") if p) if permissions_raw else ()
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=role_id,
                entity_type="institution.role",
                components=(role_component(role_id, name, permissions),),
            ),
        )
    )


def _grant_role(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    membership_id = EntityId(_str(payload, "membership_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    role_id = EntityId(_str(payload, "role_id"))
    institution_id = EntityId(_str(payload, "institution_id"))
    start = _int(payload, "start_ticks", 0)
    end = _int(payload, "end_ticks")
    assert start is not None
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=membership_id,
                entity_type="institution.membership",
                components=(
                    membership_component(
                        membership_id, actor_id, role_id, institution_id, start, end
                    ),
                ),
            ),
        )
    )


def _grant_permission(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    permission_id = EntityId(_str(payload, "permission_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    permission = _str(payload, "permission")
    target = _str(payload, "target")
    granter_id = EntityId(_str(payload, "granter_id"))
    start = _int(payload, "start_ticks", 0)
    end = _int(payload, "end_ticks")
    assert start is not None
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=permission_id,
                entity_type="institution.permission",
                components=(
                    permission_component(
                        permission_id, actor_id, permission, target, granter_id, start, end
                    ),
                ),
            ),
        )
    )


def _assign_duty(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    duty_id = EntityId(_str(payload, "duty_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    duty_type = _str(payload, "duty_type")
    due = _int(payload, "due_ticks")
    assert due is not None
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=duty_id,
                entity_type="institution.duty",
                components=(duty_component(duty_id, actor_id, duty_type, due),),
            ),
        )
    )


def _complete_duty(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("completing duty requires current state")
    payload = dict(command.payload)
    duty_id = EntityId(_str(payload, "duty_id"))
    query = InstitutionQuery(state)
    duty = query.duty(duty_id)
    if duty is None:
        raise ValidationRejected(f"duty {duty_id.value} does not exist")
    if duty.state == "done":
        raise DutyAlreadyComplete(f"duty {duty_id.value} is already complete")
    entity = state.entity(duty_id)
    assert entity is not None
    current = next(
        (c for c in entity.components.values() if c.component_type == DUTY_COMPONENT), None
    )
    if current is None:
        raise ValidationRejected(f"entity {duty_id.value} is not a duty")
    fields = dict(current.fields)
    fields["state"] = "done"
    updated = ComponentData(
        component_id=current.component_id,
        component_type=DUTY_COMPONENT,
        schema_version=current.schema_version,
        fields=fields,
    )
    return ProposedWorldDelta(operations=(EntityUpdate(entity_id=duty_id, components=(updated,)),))


def _apply_sanction(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    sanction_id = EntityId(_str(payload, "sanction_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    reason = _str(payload, "reason")
    ticks = _int(payload, "ticks")
    assert ticks is not None
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=sanction_id,
                entity_type="institution.sanction",
                components=(sanction_component(sanction_id, actor_id, reason, ticks),),
            ),
        )
    )


def _instantiate(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Instantiate a registered deterministic institution fixture via the authority."""
    from wanxiang_substrate.institution.fixture import FIXTURE_DELTAS

    payload = dict(command.payload)
    name = _str(payload, "fixture")
    version = payload.get("version", 1)
    if version != 1:
        raise ValidationRejected(f"unsupported fixture version {version!r}")
    builder = FIXTURE_DELTAS.get(name)
    if builder is None:
        raise ValidationRejected(f"unknown fixture {name!r}")
    return builder()
