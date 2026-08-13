# Goal G08A Acceptance Report
## Status
PASS
## Objective
Synthetic mansion living-world qualification.
## Delivered
- `tests/integration/test_m7_mansion.py`: 7 in-world days, takeover/resume,
  day-3 alternate branch (parent never mutated), letter custody/read
  propagation.
## Test evidence
- 700 ticks (7 days) with no-user period; human takeover + release + resume;
  fork divergence leaves parent hash stable.
## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| 7-day persistence/control/knowledge/material/branch | PASS | mansion test |
| No Core hacks | PASS | all via existing substrate |
| Worldness/defects | PASS | deterministic assertions |
## Final checkpoint
- commit: `goal g08a: synthetic mansion living-world qualification`