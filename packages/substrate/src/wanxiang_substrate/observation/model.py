"""Pure observation value objects and perception rules (framework-free)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId, EventId

VisibilityLevel = Literal["public", "group", "private"]
VALID_VISIBILITY = ("public", "group", "private")

Channel = Literal["visual", "acoustic", "textual"]


def channel_confidence(channel: Channel) -> float:
    """Deterministic confidence per perception channel (not truth)."""
    return {"visual": 1.0, "acoustic": 0.8, "textual": 0.9}[channel]


@dataclass(frozen=True, slots=True)
class ObservationFact:
    """A derived fact about what happened (not canonical truth, not belief)."""

    kind: str
    subject: str
    place: EntityId
    fields: tuple[tuple[str, str], ...] = ()

    def field(self, key: str) -> str | None:
        for k, v in self.fields:
            if k == key:
                return v
        return None


@dataclass(frozen=True, slots=True)
class Observation:
    """An observation an actor could perceive, with provenance and rules."""

    observation_id: str
    observer_id: EntityId
    source_event_id: EventId
    observed_at: int
    place: EntityId
    channel: Channel
    fact: ObservationFact
    confidence: float
    rule_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence <= 1.0):
            raise ContractError("observation confidence must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class EntityVisibility:
    """Visibility marking on an entity's actions."""

    entity_id: EntityId
    level: VisibilityLevel
    group_id: EntityId | None = None

    def __post_init__(self) -> None:
        if self.level not in VALID_VISIBILITY:
            raise ContractError(f"invalid visibility level {self.level!r}")
        if self.level == "group" and self.group_id is None:
            raise ContractError("group visibility requires a group id")
