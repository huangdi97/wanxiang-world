# Goal G05D Acceptance Report
## Status
PASS
## Objective
Projection API with actor/session perspective, rights filters and truth labels,
server-side only.
## Delivered
- `wanxiang_substrate.projection`: ProjectionRequest/Snapshot DTOs,
  ProjectionService (mode gate, sealed redaction, private belief/memory
  exclusion, restricted-place rights, truth labels).
## Test evidence
- debug requires admin; sealed payload redacted; private belief never leaks;
  restricted place redacted without permission, visible with grant.
## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Raw canonical state not returned by default | PASS | DTO contract |
| Rights/knowledge filters server-side | PASS | filter tests |
| Debug requires privilege | PASS | UnauthorizedProjection test |
| Truth/provenance labels surfaced | PASS | label assertions |
## External blockers
None.
## Final checkpoint
- commit: `goal g05d: projection api & perspective/rights filters`