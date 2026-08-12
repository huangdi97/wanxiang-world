"""Pure spatial value objects and invariants (framework-free)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

PortalState = Literal["open", "closed", "locked"]
PrivacyLevel = Literal["public", "private", "restricted"]


def validate_portal_state(value: object) -> PortalState:
    if value not in ("open", "closed", "locked"):
        raise ContractError(f"invalid portal state {value!r}")
    return value  # type: ignore[return-value]


def validate_privacy(value: object) -> PrivacyLevel:
    if value not in ("public", "private", "restricted"):
        raise ContractError(f"invalid privacy level {value!r}")
    return value  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class PlaceTopology:
    """Semantic topology of a place (a world entity, not a render coordinate)."""

    place_id: EntityId
    region_id: EntityId
    name: str
    capacity: int | None = None
    privacy: PrivacyLevel = "public"

    def __post_init__(self) -> None:
        if self.capacity is not None and self.capacity < 0:
            raise ContractError("place capacity must be non-negative")
        validate_privacy(self.privacy)
        if not self.name:
            raise ContractError("place name must be non-empty")


@dataclass(frozen=True, slots=True)
class PortalLink:
    """An edge between two places with state and optional key requirement."""

    portal_id: EntityId
    endpoint_a: EntityId
    endpoint_b: EntityId
    state: PortalState = "open"
    locked_key: EntityId | None = None
    label: str | None = None

    def __post_init__(self) -> None:
        if self.endpoint_a == self.endpoint_b:
            raise ContractError("portal endpoints must differ")
        validate_portal_state(self.state)

    def other_endpoint(self, place_id: EntityId) -> EntityId:
        if place_id == self.endpoint_a:
            return self.endpoint_b
        if place_id == self.endpoint_b:
            return self.endpoint_a
        raise ContractError(
            f"place {place_id.value} is not an endpoint of portal {self.portal_id.value}"
        )


@dataclass(frozen=True, slots=True)
class PlaceNeighbor:
    """A place reachable in one portal hop, with the traversed portal."""

    place_id: EntityId
    via_portal: EntityId


@dataclass(frozen=True, slots=True)
class SpatialPath:
    """Deterministic path result: portal sequence between two places."""

    portals: tuple[EntityId, ...]

    @property
    def cost(self) -> int:
        return len(self.portals)


@dataclass(frozen=True, slots=True)
class SpatialSnapshot:
    """Read-model of the spatial graph extracted from canonical state."""

    places: dict[EntityId, PlaceTopology]
    portals: dict[EntityId, PortalLink]

    def place(self, place_id: EntityId) -> PlaceTopology | None:
        return self.places.get(place_id)

    def portal(self, portal_id: EntityId) -> PortalLink | None:
        return self.portals.get(portal_id)


@dataclass(frozen=True, slots=True)
class Occupancy:
    """Used/limit occupancy of a place at a point in world time."""

    place_id: EntityId
    used: int
    limit: int | None

    @property
    def is_full(self) -> bool:
        return self.limit is not None and self.used >= self.limit


@dataclass(frozen=True, slots=True)
class VisibilityZone:
    """Places visible from a place via open portals (semantic, not rendering)."""

    origin: EntityId
    visible_places: frozenset[EntityId]


@dataclass(frozen=True, slots=True)
class AcousticZone:
    """Places where sound carries (through open or closed, not locked, portals)."""

    origin: EntityId
    audible_places: frozenset[EntityId]


@dataclass(frozen=True, slots=True)
class AccessPolicy:
    """Explicit policy object for a place or portal (never scattered booleans)."""

    target: EntityId
    required_permission: str
    allowed_actors: frozenset[EntityId] = frozenset()
    note: str | None = None
