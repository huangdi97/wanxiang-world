"""PhysicalObservation contract and bus value objects (G07A).

Physical observations are never canonical truth: they carry source, units,
accuracy/confidence and raw payload references, and are delivered on an
observation bus for fusion/validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.entity import FieldValue
from wanxiang_domain.errors import ContractError

ObservationKind = Literal["position", "weather", "count", "text", "status"]
Unit = Literal["ticks", "meters", "celsius", "count", "none"]

VALID_KINDS = ("position", "weather", "count", "text", "status")
VALID_UNITS = ("ticks", "meters", "celsius", "count", "none")


@dataclass(frozen=True, slots=True)
class PhysicalObservation:
    """A normalized physical observation with provenance (never direct truth)."""

    observation_id: str
    source: str
    kind: ObservationKind
    value: FieldValue
    unit: Unit = "none"
    at_ticks: int = 0
    coordinates: tuple[float, float] = (0.0, 0.0)
    accuracy: float = 0.0
    confidence: float = 1.0
    raw_ref: str = ""
    rights: str = "public"
    provenance: str = ""

    def __post_init__(self) -> None:
        if not self.observation_id or not self.source:
            raise ContractError("observation requires id and source")
        if self.kind not in VALID_KINDS:
            raise ContractError(f"invalid observation kind {self.kind!r}")
        if self.unit not in VALID_UNITS:
            raise ContractError(f"invalid observation unit {self.unit!r}")
        if self.at_ticks < 0:
            raise ContractError("at_ticks must be non-negative")
        if not (0.0 <= self.accuracy <= 1.0):
            raise ContractError("accuracy must be within [0,1]")
        if not (0.0 <= self.confidence <= 1.0):
            raise ContractError("confidence must be within [0,1]")


@dataclass(frozen=True, slots=True)
class NormalizedReading:
    """A normalized reading produced by the reality bridge."""

    observation_id: str
    source: str
    kind: str
    value: FieldValue
    unit: str
    at_ticks: int
    confidence: float
