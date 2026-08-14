"""G19I: reality/digital-twin streaming & observation fusion research.

- Stale/skewed/duplicate observations are rejected per policy.
- Low-confidence observations are down-weighted, not silently trusted.
- Observation history replay is reproducible (branch-safe, deterministic).
- Privacy propagates through fusion; synthetic streams stand in for real feeds.
- Research flag off => no core regression.
"""

from __future__ import annotations

import pytest
from wanxiang_research.flags import DEFAULT_FLAGS
from wanxiang_research.reality_stream import (
    ObservationFusion,
    ObservationLog,
    RealityReplay,
    SensorReading,
    StreamIngestor,
    SyntheticSensorStream,
)


def _reading(
    reading_id: str = "r1",
    object_ref: str = "obj",
    observed_at: float = 10.0,
    received_at: float | None = None,
    value: tuple[tuple[str, float], ...] = (("temp", 21.0),),
    confidence: float = 0.9,
    privacy: str = "public",
) -> SensorReading:
    if received_at is None:
        received_at = observed_at
    return SensorReading(
        reading_id=reading_id,
        sensor_id=f"sensor_{reading_id}",
        object_ref=object_ref,
        observed_at=observed_at,
        received_at=received_at,
        value=value,
        confidence=confidence,
        privacy=privacy,
    )


def test_stale_duplicate_and_invalid_readings_rejected() -> None:
    ingestor = StreamIngestor(max_skew=5.0, max_age=30.0)
    stale = _reading("r_stale", observed_at=10.0, received_at=100.0)
    assert ingestor.ingest(stale) is False
    dup = _reading("r1")
    assert ingestor.ingest(dup) is True
    assert ingestor.ingest(_reading("r1")) is False  # duplicate
    bad_conf = _reading("r_bad", confidence=1.5)
    assert ingestor.ingest(bad_conf) is False
    reasons = dict(ingestor.rejected())
    assert reasons["r_stale"] == "stale"
    assert reasons["r1"] == "duplicate"
    assert reasons["r_bad"] == "invalid-confidence"


def test_clock_skew_rejected() -> None:
    ingestor = StreamIngestor(max_skew=5.0)
    skewed = _reading("r_skew", observed_at=100.0, received_at=10.0)
    assert ingestor.ingest(skewed) is False
    assert dict(ingestor.rejected())["r_skew"] == "clock-skew"


def test_out_of_order_readings_ordered_by_observed_at() -> None:
    ingestor = StreamIngestor()
    ingestor.ingest(_reading("r_late", observed_at=30.0))
    ingestor.ingest(_reading("r_early", observed_at=5.0))
    ingestor.ingest(_reading("r_mid", observed_at=20.0))
    log = ingestor.log()
    assert [r.reading_id for r in log.readings] == ["r_early", "r_mid", "r_late"]


def test_low_confidence_observation_down_weighted() -> None:
    ingestor = StreamIngestor()
    ingestor.ingest(_reading("r_high", value=(("temp", 10.0),), confidence=0.9))
    ingestor.ingest(_reading("r_low", value=(("temp", 0.0),), confidence=0.1))
    fused = ObservationFusion().fuse(ingestor.log().readings)
    assert len(fused) == 1
    assert fused[0].value == (("temp", pytest.approx(9.0)),)
    assert fused[0].non_authoritative is True


def test_observation_replay_reproducible() -> None:
    readings = (
        _reading("r1", observed_at=5.0, value=(("temp", 20.0),)),
        _reading("r2", observed_at=10.0, value=(("temp", 21.0),), confidence=0.8),
        _reading("r3", observed_at=8.0, value=(("temp", 19.0),), confidence=0.6),
    )
    log = ObservationLog(readings=readings)
    replay = RealityReplay()
    first = replay.replay(log)
    second = replay.replay(log)
    assert first == second
    assert log.digest() == log.digest()
    # Reordering the log changes the digest: replay is order-sensitive and pure.
    assert log.digest() != ObservationLog(readings=tuple(reversed(readings))).digest()


def test_privacy_propagates_to_fused_observation() -> None:
    ingestor = StreamIngestor()
    ingestor.ingest(_reading("r_pub", privacy="public"))
    ingestor.ingest(_reading("r_priv", privacy="private", observed_at=11.0))
    fused = ObservationFusion().fuse(ingestor.log().readings)
    assert len(fused) == 1
    assert fused[0].privacy == "private"


def test_synthetic_stream_stands_in_for_real_feed() -> None:
    stream = SyntheticSensorStream(
        (
            _reading("s1", object_ref="room", observed_at=1.0),
            _reading("s2", object_ref="room", observed_at=2.0, confidence=0.7),
        )
    )
    ingestor = StreamIngestor()
    for reading in stream.readings():
        assert ingestor.ingest(reading) is True
    fused = ObservationFusion().fuse(ingestor.log().readings)
    assert fused[0].object_ref == "room"
    # Real authorized feeds require hardware/auth and are EXTERNAL_BLOCKED; the
    # deterministic synthetic contract above remains the reproducible baseline.
    assert all(o.non_authoritative for o in fused)


def test_flag_off_no_core_regression() -> None:
    assert DEFAULT_FLAGS.is_enabled("reality_digital_twin") is False
    from wanxiang_substrate.compiler.compiler import StructuredCompiler
    from wanxiang_substrate.sources.fixture import approved_source

    assert StructuredCompiler().compile("stable_2", {"src": approved_source()}).ok
