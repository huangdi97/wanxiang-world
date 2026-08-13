# Crash Recovery, Checkpoint & Resource Budget (G06C)
Ownership: `wanxiang_substrate.recovery`.

## Crash consistency
The crash boundary is committed events. In-flight uncommitted commands are
never partially applied (`discard_uncommitted` policy).

## Recovery
`RecoveryService.recover` restores the latest valid checkpoint, or falls back
to event replay when the snapshot is missing/corrupt (explicit policy), and
recovers/expires stale leases.

## Checkpoints
`CheckpointService.save/restore` validates revision + semantic-hash round-trip;
corrupt snapshots fail explicitly (`CorruptSnapshot`).

## Budgets
`ResourceBudget`/`BudgetTracker` cap commands/ticks/model-calls per loop so a
runaway actor or scheduler cannot monopolize execution (`BudgetExceeded`).