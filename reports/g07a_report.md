# Goal G07A Acceptance Report
## Status
PASS
## Objective
PhysicalObservation contract + Reality Bridge with normalization and provenance.
## Delivered
- `wanxiang_substrate.reality`: PhysicalObservation, ObservationAdapter port,
  FakeSensorAdapter, ManualReportAdapter, RealityBridge (validate/normalize/poll).
## Test evidence
- deterministic sensor sequence; invalid observation rejected; observations are
  never canonical truth (bus readings with provenance); manual adapter filter.
## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Observation never direct truth | PASS | bus reading test |
| Normalization/validation | PASS | invalid observation test |
| Source/rights/provenance attached | PASS | model fields |
## Final checkpoint
- commit: `goal g07a: physical observation & reality bridge`