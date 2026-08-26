"""Typed, read-only organization lifecycle projection records (G93E)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.institution.model import (
    DelegatedPermission,
    Membership,
    PermissionDecision,
    Role,
)

OrganizationAction = Literal[
    "create",
    "join",
    "leave",
    "role_change",
    "grant_permission",
    "revoke_permission",
    "dissolve",
    "split",
]
OrganizationStatus = Literal["forming", "active", "dissolved", "split"]
ORGANIZATION_ACTIONS = (
    "create",
    "join",
    "leave",
    "role_change",
    "grant_permission",
    "revoke_permission",
    "dissolve",
    "split",
)


@dataclass(frozen=True, slots=True)
class OrganizationResource:
    """A typed resource held by an organization projection."""

    resource_id: EntityId
    kind: str
    quantity: int

    def __post_init__(self) -> None:
        if not self.resource_id.value or not self.kind.strip():
            raise ContractError("organization resource requires id and kind")
        if type(self.quantity) is not int or self.quantity <= 0:
            raise ContractError("organization resource quantity must be positive")


@dataclass(frozen=True, slots=True)
class OrganizationLifecycleEvent:
    """Evidence-bound event consumed by a lifecycle proposal."""

    event_ref: str
    organization_id: EntityId
    action: OrganizationAction
    initiator_id: EntityId
    at_ticks: int
    subject_actor_id: EntityId | None = None
    membership_id: EntityId | None = None
    role_id: EntityId | None = None
    from_role_id: EntityId | None = None
    to_role_id: EntityId | None = None
    permission_id: EntityId | None = None
    permission: str | None = None
    target: str | None = None
    end_ticks: int | None = None
    child_organization_id: EntityId | None = None
    child_member_ids: tuple[EntityId, ...] = ()
    child_resources: tuple[OrganizationResource, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.event_ref.strip() or not self.organization_id.value:
            raise ContractError("organization event requires identity")
        if self.action not in ORGANIZATION_ACTIONS:
            raise ContractError(f"invalid organization action {self.action!r}")
        if not self.initiator_id.value or self.at_ticks < 0:
            raise ContractError("organization event initiator or time is invalid")
        if self.end_ticks is not None and self.end_ticks < self.at_ticks:
            raise ContractError("organization permission end precedes its start")
        if len(set(self.evidence_refs)) != len(self.evidence_refs):
            raise ContractError("organization event evidence refs must be unique")
        if any(not ref.strip() for ref in self.evidence_refs):
            raise ContractError("organization event evidence refs cannot be blank")
        if len(set(self.child_member_ids)) != len(self.child_member_ids):
            raise ContractError("organization split members must be unique")
        resource_ids = tuple(item.resource_id for item in self.child_resources)
        if len(set(resource_ids)) != len(resource_ids):
            raise ContractError("organization split resources must be unique")
        if self.action == "create" and (
            self.subject_actor_id != self.initiator_id
            or self.membership_id is None
            or self.role_id is None
        ):
            raise ContractError("organization create requires its founder and role")
        if self.action == "join" and (
            self.subject_actor_id is None or self.membership_id is None or self.role_id is None
        ):
            raise ContractError("organization join requires member, membership and role")
        if (
            self.action in ("leave", "role_change", "grant_permission", "revoke_permission")
            and self.subject_actor_id is None
        ):
            raise ContractError("organization action requires a subject actor")
        if self.action == "role_change" and (
            self.from_role_id is None
            or self.to_role_id is None
            or self.from_role_id == self.to_role_id
        ):
            raise ContractError("organization role change requires distinct roles")
        if self.action in ("grant_permission", "revoke_permission") and self.permission_id is None:
            raise ContractError("organization permission action requires permission id")
        if self.action == "grant_permission" and (not self.permission or not self.target):
            raise ContractError("organization permission grant requires permission and target")
        if self.action == "split" and (
            self.child_organization_id is None
            or not self.child_member_ids
            or self.child_organization_id == self.organization_id
        ):
            raise ContractError("organization split requires a distinct child and members")


@dataclass(frozen=True, slots=True)
class OrganizationLifecycleState:
    """Projection assembled from institution records; never a second world store."""

    organization_id: EntityId
    status: OrganizationStatus = "forming"
    roles: tuple[Role, ...] = ()
    memberships: tuple[Membership, ...] = ()
    permissions: tuple[DelegatedPermission, ...] = ()
    resources: tuple[OrganizationResource, ...] = ()
    history_refs: tuple[str, ...] = ()
    parent_organization_id: EntityId | None = None
    child_organization_ids: tuple[EntityId, ...] = ()

    def __post_init__(self) -> None:
        if not self.organization_id.value:
            raise ContractError("organization projection requires an id")
        if self.status not in ("forming", "active", "dissolved", "split"):
            raise ContractError(f"invalid organization status {self.status!r}")
        _unique_ids(tuple(role.role_id for role in self.roles), "organization roles")
        _unique_ids(
            tuple(item.membership_id for item in self.memberships), "organization memberships"
        )
        _unique_ids(
            tuple(item.permission_id for item in self.permissions), "organization permissions"
        )
        _unique_ids(tuple(item.resource_id for item in self.resources), "organization resources")
        _unique_ids(self.child_organization_ids, "organization children")
        if self.organization_id in self.child_organization_ids:
            raise ContractError("organization cannot be its own child")
        role_ids = {role.role_id for role in self.roles}
        if any(item.institution_id != self.organization_id for item in self.memberships):
            raise ContractError("membership belongs to a different organization")
        if any(item.role_id not in role_ids for item in self.memberships):
            raise ContractError("membership references an unknown role")
        if len(set(self.history_refs)) != len(self.history_refs):
            raise ContractError("organization history refs must be unique")
        if any(not ref.strip() for ref in self.history_refs):
            raise ContractError("organization history refs cannot be blank")

    def active_members(self, at_ticks: int = 0) -> tuple[EntityId, ...]:
        if self.status == "dissolved":
            return ()
        return tuple(
            sorted(
                {item.actor_id for item in self.memberships if item.is_active_at(at_ticks)},
                key=lambda actor: actor.value,
            )
        )

    def is_active_member(self, actor_id: EntityId, at_ticks: int = 0) -> bool:
        return actor_id in self.active_members(at_ticks)

    def roles_for(self, actor_id: EntityId, at_ticks: int = 0) -> tuple[Role, ...]:
        role_ids = {
            item.role_id
            for item in self.memberships
            if item.actor_id == actor_id and item.is_active_at(at_ticks)
        }
        return tuple(
            sorted(
                (role for role in self.roles if role.role_id in role_ids),
                key=lambda r: r.role_id.value,
            )
        )

    def active_permissions(
        self, actor_id: EntityId, at_ticks: int = 0
    ) -> tuple[DelegatedPermission, ...]:
        if not self.is_active_member(actor_id, at_ticks):
            return ()
        active = set(self.active_members(at_ticks))
        return tuple(
            sorted(
                (
                    item
                    for item in self.permissions
                    if item.actor_id == actor_id
                    and item.is_active_at(at_ticks)
                    and (item.granter_id == self.organization_id or item.granter_id in active)
                ),
                key=lambda item: item.permission_id.value,
            )
        )

    def orphan_permissions(self, at_ticks: int = 0) -> tuple[DelegatedPermission, ...]:
        active = set(self.active_members(at_ticks))
        return tuple(
            sorted(
                (
                    item
                    for item in self.permissions
                    if item.actor_id not in active
                    or (item.granter_id != self.organization_id and item.granter_id not in active)
                ),
                key=lambda item: item.permission_id.value,
            )
        )

    def effective_permissions(self, actor_id: EntityId, at_ticks: int = 0) -> tuple[str, ...]:
        values = {
            permission
            for role in self.roles_for(actor_id, at_ticks)
            for permission in role.permissions
        }
        values.update(item.permission for item in self.active_permissions(actor_id, at_ticks))
        return tuple(sorted(values))

    def check_permission(
        self, actor_id: EntityId, permission: str, target: str = "", at_ticks: int = 0
    ) -> PermissionDecision:
        rules: list[str] = []
        provenance: list[str] = []
        for role in self.roles_for(actor_id, at_ticks):
            if role.grants(permission):
                rules.append(f"role:{role.name}")
                provenance.append(f"membership:{role.role_id.value}")
        for item in self.active_permissions(actor_id, at_ticks):
            if item.permission == permission and (not target or item.target == target):
                rules.append("delegated_permission")
                provenance.append(f"granted_by:{item.granter_id.value}")
        return PermissionDecision(
            allow=bool(rules),
            permission=permission,
            target=target,
            rule_refs=tuple(dict.fromkeys(rules)),
            provenance=tuple(dict.fromkeys(provenance)),
            reason="allowed by organization role/delegation"
            if rules
            else "no active organization role or delegation grants this permission",
        )


def _unique_ids(values: tuple[EntityId, ...], label: str) -> None:
    if len(set(values)) != len(values):
        raise ContractError(f"{label} must be unique")
