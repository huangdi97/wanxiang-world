# ADR-0037: Crash Recovery, Checkpoint & Resource Budget Design (G06C)
- Status: accepted
- Date: 2026-08-13

## Context
G06C needs crash recovery that preserves canonical hash, validated checkpoints,
explicit in-flight policy and budgets so runaways cannot monopolize the loop.

## Decision
1. Crash boundary is committed events; in-flight uncommitted commands are
   discarded, never half-committed.
2. Startup restores the latest valid snapshot or falls back to event replay;
   corrupt snapshots fail explicitly.
3. ResourceBudget caps commands/ticks/model-calls per loop.

## Consequences
- Restart preserves canonical semantic hash; budgets bound autonomous loops.