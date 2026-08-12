# Temporal Substrate (G02B)

Ownership: `wanxiang_substrate.temporal` (world clock, schedules, deadlines,
recurrence); framework-free domain semantics.

## Model

- `WorldClock`: monotonic tick counter, `paused` flag; advance is by explicit
  command (`temporal.advance`/`temporal.advance_to`), never wall-clock.
- `Calendar`: day length in ticks + named day cycle (synthetic, no timezone
  dependencies).
- `Appointment`: actor, activity, start/end ticks, state, optional
  `TimeWindowConstraint` (must fit in window).
- `Deadline`: target, due ticks, state (pending/met/missed).
- `RecurringEvent`: anchor + interval with deterministic, bounded
  `occurrences(horizon, cap)` expansion.

## Authority

Time changes and schedule definitions are resolvers producing
`ProposedWorldDelta` through the M1 Commit Authority:
- `temporal.advance` (monotonic; negative -> `BackwardTimeError`),
- `temporal.advance_to`,
- `temporal.schedule_appointment` (overlap -> `ScheduleConflict`; window
  violation -> `TimeWindowViolation`),
- `temporal.set_deadline`, `temporal.define_recurring`,
  `temporal.mark_appointment_done`, `temporal.instantiate`.

No hidden cron or wall-clock mutation: all time-triggered changes are committed
events.

## Compatibility

- Temporal state rides on versioned components (`temporal` schema v1); no new
  migration; M1 replay untouched.
- Restore-from-snapshot and persistence restart reproduce due events exactly
  once.
