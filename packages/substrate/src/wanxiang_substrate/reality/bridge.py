"""Reality Bridge: normalize, validate and deliver observations (G07A).

The bridge ingests observations from adapters, normalizes units/timestamps/
coordinates, and publishes them on an observation bus. It never mutates
canonical world state.
"""

from __future__ import annotations

from typing import Protocol

from wanxiang_domain.entity import FieldValue

from wanxiang_substrate.reality.errors import InvalidObservation
from wanxiang_substrate.reality.model import (
    NormalizedReading,
    PhysicalObservation,
)


class ObservationAdapter(Protocol):
    """Port for deterministic fake sensors / manual reports."""

    def read(self, at_ticks: int) -> tuple[PhysicalObservation, ...]: ...


class FakeSensorAdapter:
    """Deterministic fake sensor: returns a fixed reading sequence."""

    def __init__(
        self,
        source: str,
        kind: str,
        values: tuple[FieldValue, ...],
        *,
        unit: str = "none",
        confidence: float = 1.0,
    ) -> None:
        self._source = source
        self._kind = kind
        self._values = values
        self._unit = unit
        self._confidence = confidence

    def read(self, at_ticks: int) -> tuple[PhysicalObservation, ...]:
        index = min(at_ticks, max(0, len(self._values) - 1))
        value = self._values[index]
        return (
            PhysicalObservation(
                observation_id=f"obs_{self._source}_{at_ticks}",
                source=self._source,
                kind=self._kind,  # type: ignore[arg-type]
                value=value,
                unit=self._unit,  # type: ignore[arg-type]
                at_ticks=at_ticks,
                confidence=self._confidence,
                provenance=f"sensor:{self._source}",
            ),
        )


class ManualReportAdapter:
    """Human/open-data report adapter (synthetic)."""

    def __init__(self, observations: tuple[PhysicalObservation, ...]) -> None:
        self._observations = observations

    def read(self, at_ticks: int) -> tuple[PhysicalObservation, ...]:
        return tuple(o for o in self._observations if o.at_ticks == at_ticks)


class RealityBridge:
    """Normalizes and publishes observations; never commits world state."""

    def __init__(self) -> None:
        self.adapters: dict[str, ObservationAdapter] = {}
        self._readings: list[NormalizedReading] = []

    def register_adapter(self, name: str, adapter: ObservationAdapter) -> None:
        self.adapters[name] = adapter

    def ingest(self, observation: PhysicalObservation) -> NormalizedReading:
        self._validate(observation)
        reading = self._normalize(observation)
        self._readings.append(reading)
        return reading

    def poll(self, at_ticks: int) -> tuple[NormalizedReading, ...]:
        """Poll all adapters and ingest their observations (deterministic)."""
        result: list[NormalizedReading] = []
        for name in sorted(self.adapters):
            for observation in self.adapters[name].read(at_ticks):
                result.append(self.ingest(observation))
        return tuple(result)

    def readings(self) -> tuple[NormalizedReading, ...]:
        return tuple(self._readings)

    @staticmethod
    def _validate(observation: PhysicalObservation) -> None:
        if observation.at_ticks < 0:
            raise InvalidObservation("negative timestamps are invalid")
        if observation.confidence < 0.0 or observation.confidence > 1.0:
            raise InvalidObservation("confidence out of range")
        if observation.kind == "position" and observation.unit != "meters":
            raise InvalidObservation("position observations must be in meters")

    @staticmethod
    def _normalize(observation: PhysicalObservation) -> NormalizedReading:
        return NormalizedReading(
            observation_id=observation.observation_id,
            source=observation.source,
            kind=observation.kind,
            value=observation.value,
            unit=observation.unit,
            at_ticks=observation.at_ticks,
            confidence=observation.confidence,
        )
