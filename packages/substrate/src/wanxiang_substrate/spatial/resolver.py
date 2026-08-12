"""Spatial resolvers: route movement/portal changes through the M1 authority."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.body.errors import BodyConstraintViolation
from wanxiang_substrate.body.query import BodyQuery
from wanxiang_substrate.institution.errors import PermissionDeniedByInstitution
from wanxiang_substrate.institution.query import InstitutionQuery
from wanxiang_substrate.spatial.components import (
    PORTAL_COMPONENT,
    position_component,
)
from wanxiang_substrate.spatial.errors import (
    LocationNotReachable,
    PlaceAtCapacity,
    PortalClosed,
    PortalLocked,
    SpatialAccessDenied,
)
from wanxiang_substrate.spatial.model import validate_portal_state
from wanxiang_substrate.spatial.query import SpatialQuery

ACTION_MOVE = "spatial.move"
ACTION_SET_PORTAL_STATE = "spatial.set_portal_state"
ACTION_INSTANTIATE = "spatial.instantiate"


def register_spatial_resolvers(registry: ResolverRegistry) -> None:
    """Register spatial actions on a resolver registry (deterministic)."""
    registry.register(ACTION_MOVE, _resolve_move)
    registry.register(ACTION_SET_PORTAL_STATE, _resolve_set_portal_state)
    registry.register(ACTION_INSTANTIATE, _resolve_instantiate)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _resolve_move(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("movement requires current state")
    payload = dict(command.payload)
    entity_id = EntityId(_str(payload, "entity_id"))
    target_id = EntityId(_str(payload, "target_place_id"))

    query = SpatialQuery(state)
    actor_id = EntityId(command.actor_id.value) if command.actor_id else None
    if actor_id is not None and not BodyQuery(state).can_move(actor_id):
        raise BodyConstraintViolation(f"actor {actor_id.value} cannot move (body condition)")
    if state.entity(entity_id) is None:
        raise ValidationRejected(f"entity {entity_id.value} does not exist")
    current = query.location(entity_id)
    if current is None:
        raise ValidationRejected(f"entity {entity_id.value} has no position")
    if query.places().get(target_id) is None:
        raise ValidationRejected(f"target place {target_id.value} does not exist")
    if current == target_id:
        raise ValidationRejected("entity is already at the target place")

    # Route over the full topology first, then enforce portal state per edge.
    spatial_path = query.path(current, target_id, ignore_locked=True)
    if spatial_path is None:
        raise LocationNotReachable(f"no path from {current.value} to {target_id.value}")
    for portal_id in spatial_path.portals:
        portal = query.portals().get(portal_id)
        if portal is None:
            raise LocationNotReachable(f"portal {portal_id.value} is missing")
        if portal.state == "locked":
            if not query.can_access_portal(portal_id, actor_id):
                raise PortalLocked(f"portal {portal_id.value} is locked")
        elif portal.state == "closed":
            raise PortalClosed(f"portal {portal_id.value} is closed")
    target_place = query.places().get(target_id)
    if target_place is not None and target_place.privacy == "restricted":
        allowed = (
            actor_id is not None
            and InstitutionQuery(state).check_permission(actor_id, f"enter.{target_id.value}").allow
        )
        if not allowed:
            raise PermissionDeniedByInstitution(
                f"actor cannot enter restricted place {target_id.value}"
            )
    else:
        if not query.can_enter(target_id, actor_id):
            occupancy = query.occupancy(target_id)
            if occupancy.is_full:
                raise PlaceAtCapacity(
                    f"place {target_id.value} is at capacity ({occupancy.used}/{occupancy.limit})"
                )
            raise SpatialAccessDenied(f"actor cannot enter place {target_id.value}")

    return ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=entity_id,
                components=(position_component(entity_id, target_id),),
            ),
        )
    )


def _resolve_set_portal_state(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("portal state change requires current state")
    payload = dict(command.payload)
    portal_id = EntityId(_str(payload, "portal_id"))
    new_state = validate_portal_state(payload.get("new_state"))

    portal_entity = state.entity(portal_id)
    if portal_entity is None:
        raise ValidationRejected(f"portal {portal_id.value} does not exist")
    current = next(
        (
            component
            for component in portal_entity.components.values()
            if component.component_type == PORTAL_COMPONENT
        ),
        None,
    )
    if current is None:
        raise ValidationRejected(f"entity {portal_id.value} is not a portal")
    fields = dict(current.fields)
    fields["state"] = new_state
    updated = ComponentData(
        component_id=current.component_id,
        component_type=PORTAL_COMPONENT,
        schema_version=current.schema_version,
        fields=fields,
    )
    return ProposedWorldDelta(
        operations=(EntityUpdate(entity_id=portal_id, components=(updated,)),)
    )


def _resolve_instantiate(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Instantiate a registered deterministic fixture through the authority."""
    from wanxiang_substrate.spatial.fixture import FIXTURE_DELTAS

    payload = dict(command.payload)
    name = _str(payload, "fixture")
    version = payload.get("version", 1)
    if version != 1:
        raise ValidationRejected(f"unsupported fixture version {version!r}")
    builder = FIXTURE_DELTAS.get(name)
    if builder is None:
        raise ValidationRejected(f"unknown fixture {name!r}")
    return builder()
