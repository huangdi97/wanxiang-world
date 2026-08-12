"""Deterministic institution/authority queries over canonical state."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.institution.components import (
    DUTY_COMPONENT,
    MEMBERSHIP_COMPONENT,
    PERMISSION_COMPONENT,
    ROLE_COMPONENT,
    SANCTION_COMPONENT,
)
from wanxiang_substrate.institution.model import (
    DelegatedPermission,
    Duty,
    Membership,
    PermissionDecision,
    Role,
)


class InstitutionQuery:
    """Read-only institution projection over the canonical state."""

    def __init__(self, state: InMemoryCanonicalState, now_ticks: int = 0) -> None:
        self._roles: dict[EntityId, Role] = {}
        self._memberships: dict[EntityId, Membership] = {}
        self._permissions: dict[EntityId, DelegatedPermission] = {}
        self._duties: dict[EntityId, Duty] = {}
        self._sanctions: list[tuple[str, str, int]] = []
        self._now = now_ticks
        self._scan(state)

    def _scan(self, state: InMemoryCanonicalState) -> None:
        for entity in state.entities():
            for component in entity.components.values():
                kind = component.component_type
                if kind == ROLE_COMPONENT:
                    role_id = _eid(component.fields, "role_id", entity.entity_id)
                    self._roles[role_id] = Role(
                        role_id=role_id,
                        name=str(component.fields.get("name") or role_id.value),
                        permissions=tuple(
                            p
                            for p in str(component.fields.get("permissions") or "").split(",")
                            if p
                        ),
                    )
                elif kind == MEMBERSHIP_COMPONENT:
                    membership = _membership_from(component.fields, entity.entity_id)
                    if membership is not None:
                        self._memberships[membership.membership_id] = membership
                elif kind == PERMISSION_COMPONENT:
                    permission = _permission_from(component.fields, entity.entity_id)
                    if permission is not None:
                        self._permissions[permission.permission_id] = permission
                elif kind == DUTY_COMPONENT:
                    duty = _duty_from(component.fields, entity.entity_id)
                    if duty is not None:
                        self._duties[duty.duty_id] = duty
                elif kind == SANCTION_COMPONENT:
                    actor = component.fields.get("actor_id")
                    reason = component.fields.get("reason")
                    ticks = component.fields.get("ticks", 0)
                    if isinstance(actor, str) and isinstance(reason, str):
                        self._sanctions.append(
                            (actor, reason, ticks if isinstance(ticks, int) else 0)
                        )

    def set_now(self, ticks: int) -> None:
        self._now = ticks

    def roles(self, actor_id: EntityId) -> tuple[Role, ...]:
        return tuple(
            self._roles[m.role_id]
            for m in self._memberships.values()
            if m.actor_id == actor_id and m.is_active_at(self._now) and m.role_id in self._roles
        )

    def memberships(self, actor_id: EntityId) -> tuple[Membership, ...]:
        return tuple(m for m in self._memberships.values() if m.actor_id == actor_id)

    def check_permission(
        self, actor_id: EntityId, permission: str, target: str = ""
    ) -> PermissionDecision:
        """Permission decision with rule references and provenance."""
        rule_refs: list[str] = []
        provenance: list[str] = []
        for role in self.roles(actor_id):
            if role.grants(permission):
                rule_refs.append(f"role:{role.name}")
                provenance.append(f"membership:{role.role_id.value}")
        for delegated in self._permissions.values():
            if (
                delegated.actor_id == actor_id
                and delegated.permission == permission
                and (not target or delegated.target == target)
                and delegated.is_active_at(self._now)
            ):
                rule_refs.append("delegated_permission")
                provenance.append(f"granted_by:{delegated.granter_id.value}")
        return PermissionDecision(
            allow=bool(rule_refs),
            permission=permission,
            target=target,
            rule_refs=tuple(dict.fromkeys(rule_refs)),
            provenance=tuple(dict.fromkeys(provenance)),
            reason="allowed by role/delegation"
            if rule_refs
            else "no active role or delegation grants this permission",
        )

    def duty(self, duty_id: EntityId) -> Duty | None:
        return self._duties.get(duty_id)

    def duties(self, actor_id: EntityId) -> tuple[Duty, ...]:
        return tuple(d for d in self._duties.values() if d.actor_id == actor_id)

    def due_duties(self, actor_id: EntityId, at_ticks: int | None = None) -> tuple[Duty, ...]:
        now = at_ticks if at_ticks is not None else self._now
        return tuple(
            d for d in self.duties(actor_id) if d.due_ticks <= now and d.state == "pending"
        )

    def sanctions(self, actor_id: EntityId) -> tuple[tuple[str, int], ...]:
        return tuple(
            (reason, ticks) for actor, reason, ticks in self._sanctions if actor == actor_id.value
        )


def _eid(fields: Mapping[str, object], key: str, fallback: EntityId) -> EntityId:
    value = fields.get(key)
    return EntityId(value) if isinstance(value, str) and value else fallback


def _int(fields: Mapping[str, object], key: str, default: int = 0) -> int:
    value = fields.get(key, default)
    return value if isinstance(value, int) and not isinstance(value, bool) else default


def _membership_from(fields: Mapping[str, object], entity_id: EntityId) -> Membership | None:
    membership_id = _eid(fields, "membership_id", entity_id)
    actor = fields.get("actor_id")
    role = fields.get("role_id")
    institution = fields.get("institution_id")
    if not isinstance(actor, str) or not isinstance(role, str) or not isinstance(institution, str):
        return None
    end_raw = fields.get("end_ticks")
    end = end_raw if isinstance(end_raw, int) else None
    return Membership(
        membership_id=membership_id,
        actor_id=EntityId(actor),
        role_id=EntityId(role),
        institution_id=EntityId(institution),
        start_ticks=_int(fields, "start_ticks"),
        end_ticks=end,
    )


def _permission_from(
    fields: Mapping[str, object], entity_id: EntityId
) -> DelegatedPermission | None:
    permission_id = _eid(fields, "permission_id", entity_id)
    actor = fields.get("actor_id")
    permission = fields.get("permission")
    target = fields.get("target", "")
    granter = fields.get("granter_id")
    if (
        not isinstance(actor, str)
        or not isinstance(permission, str)
        or not isinstance(granter, str)
    ):
        return None
    end_raw = fields.get("end_ticks")
    end = end_raw if isinstance(end_raw, int) else None
    return DelegatedPermission(
        permission_id=permission_id,
        actor_id=EntityId(actor),
        permission=permission,
        target=str(target),
        granter_id=EntityId(granter),
        start_ticks=_int(fields, "start_ticks"),
        end_ticks=end,
    )


def _duty_from(fields: Mapping[str, object], entity_id: EntityId) -> Duty | None:
    duty_id = _eid(fields, "duty_id", entity_id)
    actor = fields.get("actor_id")
    duty_type = fields.get("duty_type")
    if not isinstance(actor, str) or not isinstance(duty_type, str):
        return None
    return Duty(
        duty_id=duty_id,
        actor_id=EntityId(actor),
        duty_type=duty_type,
        due_ticks=_int(fields, "due_ticks"),
        state=str(fields.get("state") or "pending"),  # type: ignore[arg-type]
    )
