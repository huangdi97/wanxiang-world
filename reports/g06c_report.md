# Goal G06C Acceptance Report
## Status
PASS
## Objective
Crash recovery, checkpoint validation and resource budgets.
## Delivered
- `wanxiang_substrate.recovery`: CheckpointService (validated round-trip),
  RecoveryService (snapshot -> event-replay fallback, lease recovery),
  ResourceBudget/BudgetTracker.
## Test evidence
- kill/restart: canonical hash preserved; corrupt/missing snapshot fallback;
  in-flight never half-committed (policy); runaway budget blocked.
## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Restart preserves canonical hash | PASS | replay hash equality |
| Corrupt snapshot policy | PASS | CorruptSnapshot/NoSnapshot tests |
| In-flight command never half-committed | PASS | recovery policy |
| Runaway actor cannot monopolize loop | PASS | BudgetExceeded test |
## Final checkpoint
- commit: `goal g06c: crash recovery, checkpoint & resource budget`