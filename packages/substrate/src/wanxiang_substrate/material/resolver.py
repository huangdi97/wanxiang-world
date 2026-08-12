"""Material resolvers: items/containers/transfer/move through the M1 authority."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.material.components import (
    MATERIAL_SCHEMA_VERSION,
    contained_component,
    container_component,
    custody_component,
    item_component,
)
from wanxiang_substrate.material.errors import (
    ContainerFull,
    ContainmentCycle,
    InvalidMaterialState,
    NotCustodian,
)
from wanxiang_substrate.material.query import MaterialQuery
from wanxiang_substrate.material.resolver_ops import (
    resolve_consume,
    resolve_damage,
    resolve_give_ownership,
    resolve_read,
    resolve_seal,
)

ACTION_CREATE_ITEM = "material.create_item"
ACTION_CREATE_CONTAINER = "material.create_container"
ACTION_TRANSFER = "material.transfer"
ACTION_MOVE_INTO = "material.move_into_container"
ACTION_CONSUME = "material.consume"
ACTION_DAMAGE = "material.damage"
ACTION_SEAL = "material.seal_payload"
ACTION_READ = "material.read_payload"
ACTION_GIVE_OWNERSHIP = "material.give_ownership"
ACTION_INSTANTIATE = "material.instantiate"


def register_material_resolvers(registry: ResolverRegistry) -> None:
    registry.register(ACTION_CREATE_ITEM, _create_item)
    registry.register(ACTION_CREATE_CONTAINER, _create_container)
    registry.register(ACTION_TRANSFER, _transfer)
    registry.register(ACTION_MOVE_INTO, _move_into)
    registry.register(ACTION_CONSUME, resolve_consume)
    registry.register(ACTION_DAMAGE, resolve_damage)
    registry.register(ACTION_SEAL, resolve_seal)
    registry.register(ACTION_READ, resolve_read)
    registry.register(ACTION_GIVE_OWNERSHIP, resolve_give_ownership)
    registry.register(ACTION_INSTANTIATE, _instantiate)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _int(payload: Mapping[str, object], key: str, default: int = 1) -> int:
    value = payload.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be an integer")
    return value


def _material_kind(query: MaterialQuery, item_id: EntityId) -> str | None:
    item = query.item(item_id)
    if item is not None:
        return item.kind
    if query.container(item_id) is not None:
        return "container"
    return None


def _create_item(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    item_id = EntityId(_str(payload, "item_id"))
    kind = _str(payload, "kind")
    components: list[ComponentData] = [item_component(item_id, kind)]
    owner = payload.get("owner_id")
    if isinstance(owner, str):
        components.append(
            ComponentData(
                component_id=ComponentId(f"owner_{item_id.value}"),
                component_type="material.ownership",
                schema_version=MATERIAL_SCHEMA_VERSION,
                fields={"item_id": item_id.value, "owner_id": owner},
            )
        )
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=item_id, entity_type="material.item", components=tuple(components)
            ),
        )
    )


def _create_container(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    container_id = EntityId(_str(payload, "container_id"))
    capacity = _int(payload, "capacity")
    accepts_raw = payload.get("accepts")
    accepts = tuple(k for k in str(accepts_raw).split(",") if k) if accepts_raw else ()
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=container_id,
                entity_type="material.container",
                components=(container_component(container_id, capacity, accepts),),
            ),
        )
    )


def _transfer(command: CommandEnvelope, state: InMemoryCanonicalState | None) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("transfer requires current state")
    payload = dict(command.payload)
    item_id = EntityId(_str(payload, "item_id"))
    from_custodian = EntityId(_str(payload, "from_custodian"))
    to_custodian = EntityId(_str(payload, "to_custodian"))
    query = MaterialQuery(state)
    item = query.item(item_id)
    if item is None:
        raise ValidationRejected(f"item {item_id.value} does not exist")
    if item.state == "consumed":
        raise InvalidMaterialState("consumed items cannot be transferred")
    if query.custodian(item_id) != from_custodian:
        raise NotCustodian(f"item {item_id.value} is not held by {from_custodian.value}")
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(entity_id=item_id, components=(custody_component(item_id, to_custodian),)),
        )
    )


def _move_into(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("move requires current state")
    payload = dict(command.payload)
    item_id = EntityId(_str(payload, "item_id"))
    container_id = EntityId(_str(payload, "container_id"))
    entity = state.entity(item_id)
    if entity is None:
        raise ValidationRejected(f"entity {item_id.value} does not exist")
    query = MaterialQuery(state)
    kind = _material_kind(query, item_id)
    if kind is None:
        raise ValidationRejected(f"entity {item_id.value} is neither an item nor a container")
    spec = query.container(container_id)
    if spec is None:
        raise ValidationRejected(f"container {container_id.value} does not exist")
    if not spec.accepts(kind):
        raise ValidationRejected(f"container {container_id.value} does not accept kind {kind!r}")
    if query.is_full(container_id):
        raise ContainerFull(f"container {container_id.value} is full")
    if query.in_chain(container_id, item_id):
        raise ContainmentCycle("cannot place an item into its own descendant container")
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=item_id, components=(contained_component(item_id, container_id),)
            ),
        )
    )


def _instantiate(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Instantiate a registered deterministic material fixture via the authority."""
    from wanxiang_substrate.material.fixture import FIXTURE_DELTAS

    payload = dict(command.payload)
    name = _str(payload, "fixture")
    version = payload.get("version", 1)
    if version != 1:
        raise ValidationRejected(f"unsupported fixture version {version!r}")
    builder = FIXTURE_DELTAS.get(name)
    if builder is None:
        raise ValidationRejected(f"unknown fixture {name!r}")
    return builder()
