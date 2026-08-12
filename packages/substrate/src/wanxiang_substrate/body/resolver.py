"""Body resolvers: deterministic condition transitions through M1 authority."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.body.components import (
    condition_component,
    condition_visibility_component,
    medication_component,
)
from wanxiang_substrate.body.errors import InvalidConditionRange
from wanxiang_substrate.body.model import MAX_VALUE, MIN_VALUE, BodyCondition
from wanxiang_substrate.body.query import BodyQuery

ACTION_EXERT = "body.exert"
ACTION_REST = "body.rest"
ACTION_APPLY_CONDITION = "body.apply_condition"
ACTION_MEDICATE = "body.medicate"
ACTION_INSTANTIATE = "body.instantiate"
ACTION_SET_VISIBILITY = "body.set_visibility"


def register_body_resolvers(registry: ResolverRegistry) -> None:
    registry.register(ACTION_EXERT, _exert)
    registry.register(ACTION_REST, _rest)
    registry.register(ACTION_APPLY_CONDITION, _apply_condition)
    registry.register(ACTION_MEDICATE, _medicate)
    registry.register(ACTION_INSTANTIATE, _instantiate)
    registry.register(ACTION_SET_VISIBILITY, _set_visibility)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _int(payload: Mapping[str, object], key: str) -> int:
    value = payload.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be an integer")
    return value


def _condition_update(actor_id: EntityId, condition: BodyCondition) -> EntityUpdate:
    return EntityUpdate(
        entity_id=actor_id,
        components=(
            condition_component(
                health=condition.health,
                energy=condition.energy,
                sleep=condition.sleep,
                pain=condition.pain,
                mobility=condition.mobility,
            ),
        ),
    )


def _exert(command: CommandEnvelope, state: InMemoryCanonicalState | None) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("exert requires current state")
    payload = dict(command.payload)
    actor_id = EntityId(_str(payload, "actor_id"))
    cost = _int(payload, "energy_cost")
    if cost < 0:
        raise InvalidConditionRange("energy cost must be non-negative")
    condition = BodyQuery(state).condition(actor_id)
    if condition is None:
        raise ValidationRejected(f"actor {actor_id.value} has no body condition")
    new_energy = max(MIN_VALUE, condition.energy - cost)
    return ProposedWorldDelta(
        operations=(_condition_update(actor_id, condition.with_facet("energy", new_energy)),)
    )


def _rest(command: CommandEnvelope, state: InMemoryCanonicalState | None) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("rest requires current state")
    payload = dict(command.payload)
    actor_id = EntityId(_str(payload, "actor_id"))
    ticks = _int(payload, "ticks")
    if ticks < 0:
        raise InvalidConditionRange("rest ticks must be non-negative")
    condition = BodyQuery(state).condition(actor_id)
    if condition is None:
        raise ValidationRejected(f"actor {actor_id.value} has no body condition")
    restored_energy = min(MAX_VALUE, condition.energy + ticks)
    restored_sleep = min(MAX_VALUE, condition.sleep + ticks)
    updated = condition.with_facet("energy", restored_energy).with_facet("sleep", restored_sleep)
    return ProposedWorldDelta(operations=(_condition_update(actor_id, updated),))


def _apply_condition(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    actor_id = EntityId(_str(payload, "actor_id"))
    values: dict[str, int] = {}
    for name in ("health", "energy", "sleep", "pain", "mobility"):
        raw = payload.get(name)
        if isinstance(raw, int) and not isinstance(raw, bool):
            if not (MIN_VALUE <= raw <= MAX_VALUE):
                raise InvalidConditionRange(f"{name} must be in [{MIN_VALUE}, {MAX_VALUE}]")
            values[name] = raw
    condition = BodyCondition(**values)
    return ProposedWorldDelta(operations=(_condition_update(actor_id, condition),))


def _medicate(command: CommandEnvelope, state: InMemoryCanonicalState | None) -> ProposedWorldDelta:
    payload = dict(command.payload)
    actor_id = EntityId(_str(payload, "actor_id"))
    medication_id = EntityId(_str(payload, "medication_id"))
    effect = _str(payload, "effect")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=EntityId(f"med_{medication_id.value}"),
                entity_type="body.medication",
                components=(medication_component(medication_id, effect, actor_id),),
            ),
        )
    )


def _instantiate(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Instantiate a registered deterministic body fixture via the authority."""
    from wanxiang_substrate.body.fixture import FIXTURE_DELTAS

    payload = dict(command.payload)
    name = _str(payload, "fixture")
    version = payload.get("version", 1)
    if version != 1:
        raise ValidationRejected(f"unsupported fixture version {version!r}")
    builder = FIXTURE_DELTAS.get(name)
    if builder is None:
        raise ValidationRejected(f"unknown fixture {name!r}")
    return builder()


def _set_visibility(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    actor_id = EntityId(_str(payload, "actor_id"))
    private = payload.get("private")
    facets = tuple(str(f) for f in private.split(",") if f) if isinstance(private, str) else ()
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=actor_id,
                components=(condition_visibility_component(facets),),
            ),
        )
    )
