"""Movement time on the spatial graph (G36B).

Deterministic travel time over a SpatialPath: base ticks per portal plus any
per-portal surcharge from a MovementProfile. Pure; no write path.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.spatial.model import SpatialPath


@dataclass(frozen=True, slots=True)
class MovementProfile:
    """Travel cost policy: base ticks per portal + per-portal surcharges."""

    profile_id: str
    base_ticks_per_portal: int = 1
    portal_surcharges: tuple[tuple[str, int], ...] = ()

    def __post_init__(self) -> None:
        if not self.profile_id:
            raise ContractError("movement profile requires an id")
        if self.base_ticks_per_portal <= 0:
            raise ContractError("base_ticks_per_portal must be positive")
        for _portal_id, cost in self.portal_surcharges:
            if cost < 0:
                raise ContractError("portal surcharge must be non-negative")

    def surcharge(self, portal_id: str) -> int:
        for candidate, cost in self.portal_surcharges:
            if candidate == portal_id:
                return cost
        return 0

    def travel_time(self, path: SpatialPath) -> int:
        """Total deterministic travel ticks for a path."""
        if not path.portals:
            return 0
        total = 0
        for portal_id in path.portals:
            total += self.base_ticks_per_portal + self.surcharge(portal_id.value)
        return total


def travel_time(path: SpatialPath, *, base_ticks_per_portal: int = 1) -> int:
    """Default movement time: base ticks per portal on the path."""
    return MovementProfile(
        profile_id="default",
        base_ticks_per_portal=base_ticks_per_portal,
    ).travel_time(path)
