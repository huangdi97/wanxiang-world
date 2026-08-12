"""Material state-transition resolvers: consume/damage/payload/ownership."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.material.components import (
    INFO_PAYLOAD_COMPONENT,
    info_payload_component,
    item_component,
    ownership_component,
)
from wanxiang_substrate.material.errors import (
    InvalidMaterialState,
    NotCustodian,
    PayloadAlreadyRead,
)
from wanxiang_substrate.material.query import MaterialQuery


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def resolve_consume(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("consume requires current state")
    payload = dict(command.payload)
    item_id = EntityId(_str(payload, "item_id"))
    query = MaterialQuery(state)
    item = query.item(item_id)
    if item is None:
        raise ValidationRejected(f"item {item_id.value} does not exist")
    if item.state != "intact":
        raise InvalidMaterialState(
            f"item {item_id.value} cannot be consumed from state {item.state}"
        )
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=item_id,
                components=(item_component(item_id, item.kind, state="consumed"),),
            ),
        )
    )


def resolve_damage(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("damage requires current state")
    payload = dict(command.payload)
    item_id = EntityId(_str(payload, "item_id"))
    query = MaterialQuery(state)
    item = query.item(item_id)
    if item is None:
        raise ValidationRejected(f"item {item_id.value} does not exist")
    if item.state == "consumed":
        raise InvalidMaterialState("consumed items cannot be damaged")
    if item.state == "damaged":
        raise InvalidMaterialState("item is already damaged")
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(
                entity_id=item_id,
                components=(item_component(item_id, item.kind, state="damaged"),),
            ),
        )
    )


def resolve_seal(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    item_id = EntityId(_str(payload, "item_id"))
    payload_ref = _str(payload, "payload_ref")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=EntityId(f"payload_{item_id.value}"),
                entity_type="material.info_payload",
                components=(info_payload_component(item_id, payload_ref, state="sealed"),),
            ),
        )
    )


def resolve_read(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("read requires current state")
    payload = dict(command.payload)
    item_id = EntityId(_str(payload, "item_id"))
    reader_id = EntityId(_str(payload, "reader_id"))
    query = MaterialQuery(state)
    info = query.payload(item_id)
    if info is None:
        raise ValidationRejected(f"item {item_id.value} has no information payload")
    custodian = query.custodian(item_id)
    if custodian is None or custodian != reader_id:
        raise NotCustodian("only the custodian may read the payload")
    if info.state == "read" and reader_id in info.readers:
        raise PayloadAlreadyRead(f"{reader_id.value} already read this payload")
    readers = tuple(dict.fromkeys((*info.readers, reader_id)))
    entity = state.entity(EntityId(f"payload_{item_id.value}"))
    assert entity is not None
    current = next(
        (c for c in entity.components.values() if c.component_type == INFO_PAYLOAD_COMPONENT), None
    )
    if current is None:
        raise ValidationRejected("payload component missing")
    fields = dict(current.fields)
    fields["state"] = "read"
    fields["readers"] = ",".join(r.value for r in readers)
    updated = ComponentData(
        component_id=current.component_id,
        component_type=INFO_PAYLOAD_COMPONENT,
        schema_version=current.schema_version,
        fields=fields,
    )
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(entity_id=EntityId(f"payload_{item_id.value}"), components=(updated,)),
        )
    )


def resolve_give_ownership(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    item_id = EntityId(_str(payload, "item_id"))
    to_owner = EntityId(_str(payload, "to_owner"))
    return ProposedWorldDelta(
        operations=(
            EntityUpdate(entity_id=item_id, components=(ownership_component(item_id, to_owner),)),
        )
    )
