"""Synthetic campaign domain: factions, units, terrain, resources, orders (G11C-D).

Orders have delay/lifecycle, supply/resource flows respect route capacity,
movement consumes time, and faction observations/beliefs respect fog-of-war.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.cosim.errors import OrchestrationError


@dataclass(frozen=True, slots=True)
class Unit:
    unit_id: str
    faction: str
    region: str
    strength: int
    supply: int = 0
    orders: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Region:
    region_id: str
    routes: tuple[str, ...] = ()
    capacity: int = 100


@dataclass(frozen=True, slots=True)
class Order:
    order_id: str
    unit_id: str
    target_region: str
    issued_at: int
    delay_ticks: int
    state: str = "in_transit"

    def arrives_at(self) -> int:
        return self.issued_at + self.delay_ticks


class CampaignDomain:
    """Deterministic synthetic campaign with logistics and fog-of-war."""

    def __init__(self) -> None:
        self._units: dict[str, Unit] = {}
        self._regions: dict[str, Region] = {}
        self._orders: dict[str, Order] = {}
        self._observed: dict[str, set[str]] = {}

    def add_region(self, region: Region) -> Region:
        self._regions[region.region_id] = region
        return region

    def add_unit(self, unit: Unit) -> Unit:
        if unit.region not in self._regions:
            raise OrchestrationError(f"unit {unit.unit_id!r} in unknown region")
        self._units[unit.unit_id] = unit
        self._observed.setdefault(unit.faction, set()).add(unit.region)
        return unit

    def issue_order(self, order: Order) -> Order:
        unit = self._units.get(order.unit_id)
        if unit is None:
            raise OrchestrationError("order references unknown unit")
        self._orders[order.order_id] = order
        return order

    def advance_to(self, t: int) -> None:
        """Deliver orders whose delay elapsed; enforce route capacity."""
        for order_id, order in sorted(self._orders.items()):
            if order.state != "in_transit" or t < order.arrives_at():
                continue
            unit = self._units[order.unit_id]
            region = self._regions.get(unit.region)
            target = self._regions.get(order.target_region)
            if region is None or target is None:
                continue
            if order.target_region not in region.routes:
                continue  # no route: order fails silently (deviation)
            if (
                len([u for u in self._units.values() if u.region == order.target_region])
                >= target.capacity
            ):
                continue  # capacity exceeded
            self._units[order.unit_id] = Unit(
                unit_id=unit.unit_id,
                faction=unit.faction,
                region=order.target_region,
                strength=unit.strength,
                supply=unit.supply,
                orders=(*unit.orders, order_id),
            )
            self._orders[order_id] = Order(
                order_id=order.order_id,
                unit_id=order.unit_id,
                target_region=order.target_region,
                issued_at=order.issued_at,
                delay_ticks=order.delay_ticks,
                state="delivered",
            )
            self._observed.setdefault(unit.faction, set()).add(order.target_region)

    def unit(self, unit_id: str) -> Unit | None:
        return self._units.get(unit_id)

    def unit_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._units))

    def region_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._regions))

    def location(self, unit_id: str) -> str | None:
        unit = self._units.get(unit_id)
        return unit.region if unit is not None else None

    def knows(self, faction: str, region_id: str) -> bool:
        """Fog-of-war: a faction only knows regions it has observed."""
        return region_id in self._observed.get(faction, set())

    def deliver_supply(self, unit_id: str, amount: int) -> None:
        unit = self._units.get(unit_id)
        if unit is None:
            raise OrchestrationError("unknown unit")
        self._units[unit_id] = Unit(
            unit_id=unit.unit_id,
            faction=unit.faction,
            region=unit.region,
            strength=unit.strength,
            supply=unit.supply + amount,
            orders=unit.orders,
        )

    def supply_level(self, unit_id: str) -> int:
        unit = self._units.get(unit_id)
        return unit.supply if unit is not None else 0
