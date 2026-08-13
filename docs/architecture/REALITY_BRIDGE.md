# Reality Bridge (G07A)
Ownership: `wanxiang_substrate.reality`.

## PhysicalObservation
`PhysicalObservation` carries source, kind, unit, timestamp, coordinates,
accuracy, confidence, raw payload ref and rights/provenance. It is always
observation data, never canonical truth.

## Adapters
`ObservationAdapter` port; `FakeSensorAdapter` (deterministic value sequence)
and `ManualReportAdapter` (synthetic reports) implement it.

## Bridge
`RealityBridge` ingests observations, validates (units/confidence/timestamps),
normalizes, and publishes `NormalizedReading`s on the observation bus. It never
mutates canonical world state.