"""Observation resolvers through the M1 authority."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.observation.components import announcement_component, visibility_component
from wanxiang_substrate.observation.errors import InvalidVisibility
from wanxiang_substrate.observation.model import VALID_VISIBILITY

ACTION_SET_VISIBILITY = "observation.set_visibility"
ACTION_ANNOUNCE = "observation.announce"
ACTION_INSTANTIATE = "observation.instantiate"


def register_observation_resolvers(registry: ResolverRegistry) -> None:
    registry.register(ACTION_SET_VISIBILITY, _set_visibility)
    registry.register(ACTION_ANNOUNCE, _announce)
    registry.register(ACTION_INSTANTIATE, _instantiate)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _set_visibility(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    entity_id = EntityId(_str(payload, "entity_id"))
    level = _str(payload, "level")
    if level not in VALID_VISIBILITY:
        raise InvalidVisibility(f"invalid visibility level {level!r}")
    group_raw = payload.get("group_id")
    group_id = EntityId(group_raw) if isinstance(group_raw, str) and group_raw else None
    if level == "group" and group_id is None:
        raise InvalidVisibility("group visibility requires a group_id")
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=entity_id,
                components=(visibility_component(entity_id, level, group_id),),
            ),
        )
    )


def _announce(command: CommandEnvelope, state: InMemoryCanonicalState | None) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("announce requires current state")
    from wanxiang_substrate.spatial.query import SpatialQuery

    payload = dict(command.payload)
    actor_id = EntityId(_str(payload, "actor_id"))
    message = _str(payload, "message")
    place = SpatialQuery(state).location(actor_id)
    if place is None:
        raise ValidationRejected("announcer has no position")
    visibility = str(payload.get("visibility") or "public")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=EntityId(f"ann_{actor_id.value}_{place.value}"),
                entity_type="observation.announcement",
                components=(announcement_component(actor_id, message, place, visibility),),
            ),
        )
    )


def _instantiate(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Instantiate a registered deterministic observation fixture."""
    from wanxiang_substrate.observation.fixture import FIXTURE_DELTAS

    payload = dict(command.payload)
    name = _str(payload, "fixture")
    version = payload.get("version", 1)
    if version != 1:
        raise ValidationRejected(f"unsupported fixture version {version!r}")
    builder = FIXTURE_DELTAS.get(name)
    if builder is None:
        raise ValidationRejected(f"unknown fixture {name!r}")
    return builder()
