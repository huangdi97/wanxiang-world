"""G07A-G07B: reality bridge normalization + observation fusion."""

from __future__ import annotations

import pytest
from wanxiang_substrate.reality.bridge import (
    FakeSensorAdapter,
    ManualReportAdapter,
    RealityBridge,
)
from wanxiang_substrate.reality.errors import InvalidObservation
from wanxiang_substrate.reality.fusion import FusionPolicy, ObservationFusion
from wanxiang_substrate.reality.model import NormalizedReading, PhysicalObservation


@pytest.mark.unit
def test_fake_sensor_reads_deterministic_sequence() -> None:
    bridge = RealityBridge()
    bridge.register_adapter(
        "temp", FakeSensorAdapter("temp_sensor", "weather", (20, 21, 22), unit="celsius")
    )
    readings = bridge.poll(at_ticks=2)
    assert len(readings) == 1
    assert readings[0].value == 22
    assert readings[0].unit == "celsius"


@pytest.mark.unit
def test_invalid_observation_rejected() -> None:
    bridge = RealityBridge()
    with pytest.raises(InvalidObservation):
        bridge.ingest(
            PhysicalObservation(
                observation_id="obs_bad",
                source="sensor",
                kind="position",
                value="1.0,2.0",
                unit="none",  # position requires meters
                confidence=1.0,
            )
        )


@pytest.mark.unit
def test_observation_is_never_canonical_truth() -> None:
    bridge = RealityBridge()
    reading = bridge.ingest(
        PhysicalObservation(
            observation_id="obs_1",
            source="human",
            kind="count",
            value=3,
            at_ticks=10,
            confidence=0.6,
            provenance="report:manual",
        )
    )
    # The reading is data on the bus, with provenance; it is not world state.
    assert isinstance(reading, NormalizedReading)
    assert bridge.readings()[0].source == "human"
    assert bridge.readings()[0].confidence == 0.6


@pytest.mark.unit
def test_fusion_deduplicates_and_fuses_consistent() -> None:
    fusion = ObservationFusion(FusionPolicy(confidence_threshold=0.7))
    readings = (
        NormalizedReading("o1", "s1", "count", 5, "count", 10, 0.8),
        NormalizedReading("o2", "s1", "count", 5, "count", 11, 0.9),
    )
    results = fusion.fuse(readings)
    assert len(results) == 1
    assert results[0].outcome == "proposal"
    assert results[0].value == 5
    assert results[0].confidence == 0.9


@pytest.mark.unit
def test_fusion_keeps_conflicting_inputs_as_conflict_set() -> None:
    fusion = ObservationFusion(FusionPolicy(confidence_threshold=0.7, conflict_window_ticks=5))
    readings = (
        NormalizedReading("o1", "s1", "count", 5, "count", 10, 0.9),
        NormalizedReading("o2", "s1", "count", 9, "count", 12, 0.8),
    )
    results = fusion.fuse(readings)
    assert len(results) == 1
    assert results[0].outcome == "conflict"
    # Both source observations are preserved in the conflict set provenance.
    assert results[0].sources == ("s1",)
    assert results[0].value is None


@pytest.mark.unit
def test_low_confidence_observation_deferred_to_claim() -> None:
    fusion = ObservationFusion(FusionPolicy(confidence_threshold=0.9))
    readings = (NormalizedReading("o1", "s1", "count", 5, "count", 10, 0.5),)
    results = fusion.fuse(readings)
    assert results[0].outcome == "claim_candidate"
    assert "review" in results[0].rationale


@pytest.mark.unit
def test_manual_report_adapter_filters_by_ticks() -> None:
    adapter = ManualReportAdapter(
        (
            PhysicalObservation("m1", "human", "status", "ok", at_ticks=5, confidence=1.0),
            PhysicalObservation("m2", "human", "status", "ok", at_ticks=8, confidence=1.0),
        )
    )
    assert len(adapter.read(5)) == 1
