"""Deterministic material queries over canonical state (read-only)."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.material.components import (
    CONTAINED_COMPONENT,
    CONTAINER_COMPONENT,
    CUSTODY_COMPONENT,
    INFO_PAYLOAD_COMPONENT,
    ITEM_COMPONENT,
    OWNERSHIP_COMPONENT,
)
from wanxiang_substrate.material.model import (
    ContainerSpec,
    Containment,
    Custody,
    InfoPayload,
    MaterialItem,
    Ownership,
)


def _entity_id(fields: Mapping[str, object], key: str, fallback: EntityId) -> EntityId:
    value = fields.get(key)
    if isinstance(value, str) and value:
        return EntityId(value)
    return fallback


class MaterialQuery:
    """Read-only material graph over the canonical state."""

    def __init__(self, state: InMemoryCanonicalState) -> None:
        self._items: dict[EntityId, MaterialItem] = {}
        self._containers: dict[EntityId, ContainerSpec] = {}
        self._custody: dict[EntityId, Custody] = {}
        self._ownership: dict[EntityId, Ownership] = {}
        self._contained: dict[EntityId, Containment] = {}
        self._payloads: dict[EntityId, InfoPayload] = {}
        self._scan(state)

    def _scan(self, state: InMemoryCanonicalState) -> None:
        for entity in state.entities():
            for component in entity.components.values():
                kind = component.component_type
                fields = component.fields
                if kind == ITEM_COMPONENT:
                    item_id = _entity_id(fields, "item_id", entity.entity_id)
                    self._items[item_id] = MaterialItem(
                        item_id=item_id,
                        kind=str(fields.get("kind") or "item"),
                        state=str(fields.get("state") or "intact"),  # type: ignore[arg-type]
                    )
                elif kind == CONTAINER_COMPONENT:
                    cid = _entity_id(fields, "container_id", entity.entity_id)
                    capacity = fields.get("capacity", 1)
                    accepts_raw = fields.get("accepts", "")
                    accepts = (
                        tuple(k for k in accepts_raw.split(",") if k)
                        if isinstance(accepts_raw, str)
                        else ()
                    )
                    self._containers[cid] = ContainerSpec(
                        container_id=cid,
                        capacity=capacity if isinstance(capacity, int) else 1,
                        accepts_kinds=accepts,
                    )
                elif kind == CUSTODY_COMPONENT:
                    item_id = _entity_id(fields, "item_id", entity.entity_id)
                    custodian = fields.get("custodian_id")
                    if isinstance(custodian, str):
                        self._custody[item_id] = Custody(item_id, EntityId(custodian))
                elif kind == OWNERSHIP_COMPONENT:
                    item_id = _entity_id(fields, "item_id", entity.entity_id)
                    owner = fields.get("owner_id")
                    if isinstance(owner, str):
                        self._ownership[item_id] = Ownership(item_id, EntityId(owner))
                elif kind == CONTAINED_COMPONENT:
                    item_id = _entity_id(fields, "item_id", entity.entity_id)
                    container = fields.get("container_id")
                    if isinstance(container, str):
                        self._contained[item_id] = Containment(item_id, EntityId(container))
                elif kind == INFO_PAYLOAD_COMPONENT:
                    item_id = _entity_id(fields, "item_id", entity.entity_id)
                    payload_ref = fields.get("payload_ref")
                    if isinstance(payload_ref, str):
                        readers_raw = fields.get("readers", "")
                        readers = (
                            tuple(EntityId(r) for r in readers_raw.split(",") if r)
                            if isinstance(readers_raw, str)
                            else ()
                        )
                        self._payloads[item_id] = InfoPayload(
                            item_id=item_id,
                            payload_ref=payload_ref,
                            state=str(fields.get("state") or "sealed"),  # type: ignore[arg-type]
                            readers=readers,
                        )

    def item(self, item_id: EntityId) -> MaterialItem | None:
        return self._items.get(item_id)

    def container(self, container_id: EntityId) -> ContainerSpec | None:
        return self._containers.get(container_id)

    def custodian(self, item_id: EntityId) -> EntityId | None:
        custody = self._custody.get(item_id)
        if custody is not None:
            return custody.custodian_id
        contained = self._contained.get(item_id)
        if contained is not None:
            return self.custodian_of_container(contained.container_id)
        return None

    def custodian_of_container(self, container_id: EntityId) -> EntityId | None:
        for custody in self._custody.values():
            if custody.item_id == container_id:
                return custody.custodian_id
        contained = self._contained.get(container_id)
        if contained is not None:
            return self.custodian_of_container(contained.container_id)
        return None

    def owner(self, item_id: EntityId) -> EntityId | None:
        ownership = self._ownership.get(item_id)
        return ownership.owner_id if ownership is not None else None

    def container_of(self, item_id: EntityId) -> EntityId | None:
        contained = self._contained.get(item_id)
        return contained.container_id if contained is not None else None

    def contents(self, container_id: EntityId, *, recursive: bool = False) -> tuple[EntityId, ...]:
        direct = tuple(
            sorted(
                (
                    item_id
                    for item_id, c in self._contained.items()
                    if c.container_id == container_id
                ),
                key=lambda i: i.value,
            )
        )
        if not recursive:
            return direct
        result: list[EntityId] = list(direct)
        for item_id in direct:
            result.extend(self.contents(item_id, recursive=True))
        return tuple(sorted(set(result), key=lambda i: i.value))

    def container_occupancy(self, container_id: EntityId) -> tuple[int, int]:
        used = len(self.contents(container_id))
        spec = self._containers.get(container_id)
        return used, spec.capacity if spec is not None else 0

    def is_full(self, container_id: EntityId) -> bool:
        used, capacity = self.container_occupancy(container_id)
        return capacity > 0 and used >= capacity

    def payload(self, item_id: EntityId) -> InfoPayload | None:
        return self._payloads.get(item_id)

    def in_chain(self, item_id: EntityId, possible_ancestor: EntityId) -> bool:
        """True if `possible_ancestor` is the item itself or inside its chain."""
        current: EntityId | None = item_id
        seen: set[EntityId] = set()
        while current is not None and current not in seen:
            if current == possible_ancestor:
                return True
            seen.add(current)
            contained = self._contained.get(current)
            current = contained.container_id if contained is not None else None
        return False
