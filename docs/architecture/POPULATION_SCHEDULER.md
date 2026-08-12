# Population Resolution & Autonomous Scheduler (G02F)

Ownership: `wanxiang_substrate.population` (multi-rate autonomous scheduler).

## Model

- `PopulationLevel`: focus / lightweight / duty / aggregate with per-actor rates.
- `SchedulerEvent`: deterministic heap ordering (due ticks, priority, actor id,
  action, seq tie-break).
- `SchedulerConfig`: per-tick and total event budgets.

## Scheduler

`AutonomousScheduler` advances world time (via `temporal.advance` commands) and
submits commands through the M1 Commit Authority with no user input:
- focus/lightweight actors rest at their resolution rate;
- duty actors complete their due institution duties first;
- all command ids are derived deterministically (no duplicate effects);
- budgets (per-tick / total) are enforced with `SchedulerBudgetExceeded`;
- the run (seed/horizon/events) is recorded as committed canonical state so a
  later run resumes deterministically.

Determinism: the same initial snapshot + seed + config reproduces the same
event sequence and final canonical hash.

## Application optimization

`WorldRuntime` now uses a validated `StateReader` cache (per instance/branch,
checked against the event-store head) so autonomous long runs are not O(n^2);
out-of-band writes are never masked (invalidated on mismatch or via
`invalidate_state_cache`).

## Compatibility

- Population state rides on versioned components (`population` schema v1); no
  new migration; M1 replay untouched.
