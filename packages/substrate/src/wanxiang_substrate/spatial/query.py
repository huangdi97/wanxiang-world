"""Deterministic spatial queries over canonical state (read-only)."""

from __future__ import annotations

from collections import deque
from collections.abc import Mapping

from wanxiang_domain.entity import EntityState
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.spatial.components import (
    ACCESS_KEY_COMPONENT,
    PLACE_COMPONENT,
    PLACE_GRANT_COMPONENT,
    PORTAL_COMPONENT,
    POSITION_COMPONENT,
)
from wanxiang_substrate.spatial.model import (
    AcousticZone,
    Occupancy,
    PlaceNeighbor,
    PlaceTopology,
    PortalLink,
    SpatialPath,
    SpatialSnapshot,
    VisibilityZone,
)

_PLACE_CMP = EntityId("place")


class SpatialQuery:
    """Read-only spatial graph queries derived from the canonical state."""

    def __init__(self, state: InMemoryCanonicalState) -> None:
        self._state = state
        self._places: dict[EntityId, PlaceTopology] = {}
        self._portals: dict[EntityId, PortalLink] = {}
        self._positions: dict[EntityId, EntityId] = {}
        self._keys: dict[EntityId, frozenset[EntityId]] = {}
        self._scan(state)

    def _scan(self, state: InMemoryCanonicalState) -> None:
        for entity in state.entities():
            for component in entity.components.values():
                if component.component_type == PLACE_COMPONENT:
                    self._places[entity.entity_id] = _place_from(entity, component.fields)
                elif component.component_type == PORTAL_COMPONENT:
                    self._portals[entity.entity_id] = _portal_from(entity, component.fields)
                elif component.component_type == POSITION_COMPONENT:
                    place = component.fields.get("place_id")
                    if isinstance(place, str):
                        self._positions[entity.entity_id] = EntityId(place)
                elif component.component_type == ACCESS_KEY_COMPONENT:
                    key = component.fields.get("key_id")
                    if isinstance(key, str):
                        held = self._keys.get(entity.entity_id, frozenset())
                        self._keys[entity.entity_id] = held | {EntityId(key)}

    # -- snapshot ---------------------------------------------------------

    def snapshot(self) -> SpatialSnapshot:
        return SpatialSnapshot(places=dict(self._places), portals=dict(self._portals))

    def places(self) -> Mapping[EntityId, PlaceTopology]:
        return self._places

    def portals(self) -> Mapping[EntityId, PortalLink]:
        return self._portals

    def location(self, entity_id: EntityId) -> EntityId | None:
        return self._positions.get(entity_id)

    # -- topology ---------------------------------------------------------

    def neighbors(
        self, place_id: EntityId, *, ignore_portal_state: bool = False
    ) -> tuple[PlaceNeighbor, ...]:
        result: list[PlaceNeighbor] = []
        for portal in self._portals.values():
            if place_id not in (portal.endpoint_a, portal.endpoint_b):
                continue
            if not ignore_portal_state and portal.state != "open":
                continue
            result.append(
                PlaceNeighbor(place_id=portal.other_endpoint(place_id), via_portal=portal.portal_id)
            )
        return tuple(sorted(result, key=lambda n: n.place_id.value))

    def _adjacency(self, ignore_locked: bool) -> dict[EntityId, list[PlaceNeighbor]]:
        adjacency: dict[EntityId, list[PlaceNeighbor]] = {pid: [] for pid in self._places}
        for place_id in self._places:
            for portal in self._portals.values():
                if place_id not in (portal.endpoint_a, portal.endpoint_b):
                    continue
                if portal.state == "locked" and not ignore_locked:
                    continue
                if portal.state == "closed" and not ignore_locked:
                    continue
                adjacency[place_id].append(
                    PlaceNeighbor(
                        place_id=portal.other_endpoint(place_id), via_portal=portal.portal_id
                    )
                )
        for place_id in adjacency:
            adjacency[place_id].sort(key=lambda n: n.place_id.value)
        return adjacency

    def path(
        self, start: EntityId, goal: EntityId, *, ignore_locked: bool = False
    ) -> SpatialPath | None:
        """Deterministic BFS shortest path (by portal count) between places."""
        if start not in self._places or goal not in self._places:
            return None
        adjacency = self._adjacency(ignore_locked)
        frontier: deque[tuple[EntityId, list[EntityId]]] = deque([(start, [])])
        visited = {start}
        while frontier:
            current, portals = frontier.popleft()
            for neighbor in adjacency.get(current, []):
                if neighbor.place_id in visited:
                    continue
                new_portals = portals + [neighbor.via_portal]
                if neighbor.place_id == goal:
                    return SpatialPath(portals=tuple(new_portals))
                visited.add(neighbor.place_id)
                frontier.append((neighbor.place_id, new_portals))
        return None

    def reachable(self, start: EntityId, goal: EntityId, *, ignore_locked: bool = False) -> bool:
        return self.path(start, goal, ignore_locked=ignore_locked) is not None

    def can_access_portal(self, portal_id: EntityId, actor_id: EntityId | None) -> bool:
        portal = self._portals.get(portal_id)
        if portal is None:
            return False
        if portal.state != "locked":
            return True
        if actor_id is None:
            return False
        return portal.locked_key is not None and portal.locked_key in self._keys.get(
            actor_id, frozenset()
        )

    # -- occupancy / privacy ---------------------------------------------

    def occupancy(self, place_id: EntityId) -> Occupancy:
        place = self._places.get(place_id)
        used = sum(1 for p in self._positions.values() if p == place_id)
        return Occupancy(place_id=place_id, used=used, limit=place.capacity if place else None)

    def can_enter(self, place_id: EntityId, actor_id: EntityId | None) -> bool:
        place = self._places.get(place_id)
        if place is None:
            return False
        if place.capacity is not None and self.occupancy(place_id).used >= place.capacity:
            return False
        if place.privacy == "public":
            return True
        if actor_id is None:
            return False
        # private/restricted places require an explicit access grant component
        entity = self._state.entity(actor_id)
        if entity is None:
            return False
        return any(
            component.component_type == PLACE_GRANT_COMPONENT
            and component.fields.get("place_id") == place_id.value
            for component in entity.components.values()
        )

    # -- zones (semantic only) -------------------------------------------

    def visibility_zone(self, place_id: EntityId) -> VisibilityZone:
        visible: set[EntityId] = set()
        for neighbor in self.neighbors(place_id):  # open portals only
            visible.add(neighbor.place_id)
        return VisibilityZone(origin=place_id, visible_places=frozenset(visible))

    def acoustic_zone(self, place_id: EntityId) -> AcousticZone:
        audible: set[EntityId] = set()
        for portal in self._portals.values():
            if place_id not in (portal.endpoint_a, portal.endpoint_b):
                continue
            if portal.state == "locked":
                continue
            audible.add(portal.other_endpoint(place_id))
        return AcousticZone(origin=place_id, audible_places=frozenset(audible))


def _place_from(entity: EntityState, fields: Mapping[str, object]) -> PlaceTopology:
    region = fields.get("region_id")
    name = fields.get("name")
    capacity = fields.get("capacity")
    privacy = fields.get("privacy", "public")
    return PlaceTopology(
        place_id=entity.entity_id,
        region_id=EntityId(region) if isinstance(region, str) else entity.entity_id,
        name=name if isinstance(name, str) else entity.entity_id.value,
        capacity=capacity if isinstance(capacity, int) and not isinstance(capacity, bool) else None,
        privacy=privacy if isinstance(privacy, str) else "public",  # type: ignore[arg-type]
    )


def _portal_from(entity: EntityState, fields: Mapping[str, object]) -> PortalLink:
    a = fields.get("endpoint_a")
    b = fields.get("endpoint_b")
    state = fields.get("state", "open")
    locked_key = fields.get("locked_key")
    label = fields.get("label")
    return PortalLink(
        portal_id=entity.entity_id,
        endpoint_a=EntityId(a) if isinstance(a, str) else entity.entity_id,
        endpoint_b=EntityId(b) if isinstance(b, str) else entity.entity_id,
        state=state if isinstance(state, str) else "open",  # type: ignore[arg-type]
        locked_key=EntityId(locked_key) if isinstance(locked_key, str) else None,
        label=label if isinstance(label, str) else None,
    )
