"""Reality / digital-twin streaming & observation fusion research (G19I, experimental).

Sensor readings are OBSERVATIONS, never canonical truth: they carry sensor
identity, confidence, provenance and privacy, and the reality bridge only
proposes fused observations (non-authoritative) that Commit Authority may
ignore. Clock skew, staleness and duplicates are handled at ingestion; fusion
is deterministic and the observation log replays reproducibly. Synthetic
streams stand in for real authorized feeds (EXTERNAL_BLOCKED slice).
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class SensorReading:
    reading_id: str
    sensor_id: str
    object_ref: str  # reality object reference, mapped to a semantic entity later
    observed_at: float  # sensor clock
    received_at: float  # ingestion clock
    value: tuple[tuple[str, float], ...]
    confidence: float
    privacy: str = "public"  # public | private
    source: str = "synthetic"

    def age(self) -> float:
        return self.received_at - self.observed_at


@dataclass(frozen=True, slots=True)
class FusedObservation:
    object_ref: str
    time: float
    value: tuple[tuple[str, float], ...]
    provenance: tuple[str, ...]
    confidence: float
    non_authoritative: bool = True
    privacy: str = "public"


class SensorStream(Protocol):
    def readings(self) -> tuple[SensorReading, ...]: ...


class SyntheticSensorStream:
    """Deterministic synthetic stream (no hardware/paid feed required)."""

    def __init__(self, readings: Sequence[SensorReading] = ()) -> None:
        self._readings = tuple(readings)

    def readings(self) -> tuple[SensorReading, ...]:
        return self._readings


@dataclass(frozen=True, slots=True)
class ObservationLog:
    readings: tuple[SensorReading, ...]  # ordered by observed_at

    def digest(self) -> str:
        canonical = json.dumps(
            [
                {
                    "reading_id": r.reading_id,
                    "sensor_id": r.sensor_id,
                    "object_ref": r.object_ref,
                    "observed_at": r.observed_at,
                    "value": sorted(r.value),
                    "confidence": r.confidence,
                    "privacy": r.privacy,
                }
                for r in self.readings
            ],
            sort_keys=True,
        )
        return hashlib.sha256(canonical.encode()).hexdigest()


class StreamIngestor:
    """Ingests readings: dedupe, clock-skew and staleness checks, time ordering."""

    def __init__(self, max_skew: float = 5.0, max_age: float = 30.0) -> None:
        self._max_skew = max_skew
        self._max_age = max_age
        self._accepted: list[SensorReading] = []
        self._rejected: list[tuple[str, str]] = []
        self._seen: set[str] = set()

    def ingest(self, reading: SensorReading) -> bool:
        if reading.reading_id in self._seen:
            self._rejected.append((reading.reading_id, "duplicate"))
            return False
        self._seen.add(reading.reading_id)
        if reading.age() > self._max_age:
            self._rejected.append((reading.reading_id, "stale"))
            return False
        if abs(reading.age()) > self._max_skew:
            self._rejected.append((reading.reading_id, "clock-skew"))
            return False
        if not 0.0 <= reading.confidence <= 1.0:
            self._rejected.append((reading.reading_id, "invalid-confidence"))
            return False
        self._accepted.append(reading)
        return True

    def log(self) -> ObservationLog:
        # Causality ordering by observed_at, not arrival order.
        ordered = sorted(self._accepted, key=lambda r: (r.observed_at, r.reading_id))
        return ObservationLog(readings=tuple(ordered))

    def rejected(self) -> tuple[tuple[str, str], ...]:
        return tuple(self._rejected)

    def accepted_count(self) -> int:
        return len(self._accepted)


class ObservationFusion:
    """Experimental confidence-weighted fusion; output is never authoritative."""

    def fuse(self, readings: Sequence[SensorReading]) -> tuple[FusedObservation, ...]:
        by_object: dict[str, list[SensorReading]] = {}
        for reading in readings:
            by_object.setdefault(reading.object_ref, []).append(reading)
        fused: list[FusedObservation] = []
        for object_ref in sorted(by_object):
            group = by_object[object_ref]
            weights = {r.reading_id: r.confidence for r in group}
            keys = sorted({k for r in group for k, _ in r.value})
            values: list[tuple[str, float]] = []
            for key in keys:
                total_w = 0.0
                weighted = 0.0
                for reading in group:
                    for k, v in reading.value:
                        if k == key:
                            total_w += weights[reading.reading_id]
                            weighted += v * weights[reading.reading_id]
                if total_w <= 0.0:
                    continue
                values.append((key, weighted / total_w))
            time = max(r.observed_at for r in group)
            provenance = tuple(sorted(r.reading_id for r in group))
            confidence = max(weights.values())
            privacy = "private" if any(r.privacy == "private" for r in group) else "public"
            fused.append(
                FusedObservation(
                    object_ref=object_ref,
                    time=time,
                    value=tuple(values),
                    provenance=provenance,
                    confidence=confidence,
                    non_authoritative=True,
                    privacy=privacy,
                )
            )
        return tuple(fused)


class RealityReplay:
    """Branch-safe replay: fusing an observation log is pure and reproducible."""

    def __init__(self, fusion: ObservationFusion | None = None) -> None:
        self._fusion = fusion if fusion is not None else ObservationFusion()

    def replay(self, log: ObservationLog) -> tuple[FusedObservation, ...]:
        return self._fusion.fuse(log.readings)
