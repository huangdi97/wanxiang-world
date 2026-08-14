# Reality / Digital-twin Streaming & Observation Fusion Research (G19I)

## Prototype
- `SensorReading` ? sensor identity, observed/received clocks, value, confidence, privacy, source.
- `StreamIngestor` ? dedupe, clock-skew and staleness rejection (stale > skew priority), causality
  ordering by observed_at, reject list with reasons.
- `ObservationFusion` ? experimental confidence-weighted fusion; fused observations are always
  NON-authoritative and carry provenance (reading ids) + privacy (private propagates).
- `RealityReplay` ? branch-safe, pure replay of an observation log (deterministic digest).
- `SyntheticSensorStream` ? deterministic substitute for real authorized feeds (EXTERNAL_BLOCKED slice).

## Results
| Check | Result |
|---|---|
| Stale/skewed/duplicate/invalid observations rejected per policy | PASS |
| Low-confidence observations down-weighted (not silently trusted) | PASS |
| Observation history replay reproducible (pure, order-sensitive) | PASS |
| Privacy propagates through fusion | PASS |
| Synthetic stream stands in for real feed; authority boundaries preserved | PASS |
| Flag OFF -> no core regression | PASS |

## Decision
**KEEP_EXPERIMENTAL** ? the ingestion/fusion seam is sound; real authorized sensor feeds and hardware
are EXTERNAL_BLOCKED. Promotion requires fusion parity + a privacy audit on a real feed.

## Evidence
- `uv run pytest tests/integration/test_g19i_reality_stream.py -q` -> 8 passed.
- ruff/pyright clean; architecture PASS at the M16 gate.
