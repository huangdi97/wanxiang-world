"""Pure body/condition value objects and invariants (framework-free)."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from wanxiang_domain.errors import ContractError

Facet = Literal["health", "energy", "sleep", "pain", "mobility"]
MobilityCapability = Literal["unrestricted", "reduced", "immobile"]

MIN_VALUE = 0
MAX_VALUE = 100
MOVE_THRESHOLD = 40  # mobility >= this allows unrestricted movement
FATIGUE_THRESHOLD = 20  # energy < this means fatigued


@dataclass(frozen=True, slots=True)
class BodyCondition:
    """Bounded body condition facets (0..100 each)."""

    health: int = 100
    energy: int = 100
    sleep: int = 100
    pain: int = 0
    mobility: int = 100

    def __post_init__(self) -> None:
        for name in ("health", "energy", "sleep", "pain", "mobility"):
            value = getattr(self, name)
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or not (MIN_VALUE <= value <= MAX_VALUE)
            ):
                raise ContractError(f"{name} must be an integer in [{MIN_VALUE}, {MAX_VALUE}]")

    def mobility_capability(self) -> MobilityCapability:
        if self.mobility < MOVE_THRESHOLD:
            return "immobile" if self.mobility == 0 else "reduced"
        return "unrestricted"

    def is_fatigued(self) -> bool:
        return self.energy < FATIGUE_THRESHOLD

    def is_sleepy(self) -> bool:
        return self.sleep < FATIGUE_THRESHOLD

    def with_facet(self, name: Facet, value: int) -> BodyCondition:
        if name not in ("health", "energy", "sleep", "pain", "mobility"):
            raise ContractError(f"unknown facet {name!r}")
        return replace(self, **{name: value})


def visible_facets(condition: BodyCondition, private: frozenset[Facet]) -> dict[str, int]:
    """Public projection of a condition, excluding private facets."""
    return {
        name: getattr(condition, name)
        for name in ("health", "energy", "sleep", "pain", "mobility")
        if name not in private
    }
