# Goal G08B Acceptance Report
## Status
PASS (local); real Red Chamber data EXTERNAL_BLOCKED
## Objective
Red Chamber source-gated reference slice.
## Delivered
- `sources/red_chamber/` manifest template + README; Source Gate positive/
  negative tests (approved synthetic compiles; rights-denied cannot enter
  canonical compilation).
## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Source Gate positive/negative fixture | PASS | m7 qualification test |
| Unapproved text cannot enter canonical package | PASS | gate rejection test |
| Real literary data | EXTERNAL_BLOCKED | no rights-cleared corpus; template only |
| No fabricated facts | PASS | no invented content |
## Final checkpoint
- commit: `goal g08b: red chamber source-gated reference slice`