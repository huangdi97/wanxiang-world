# ADR-0012: Temporal Substrate Design (G02B)

- Status: accepted
- Date: 2026-08-13

## Context

G02B needs monotonic world time, calendars, schedules and recurring constraints
independent of wall clock, without hidden cron mutations.

## Decision

1. World time is a `WorldClock` component (ticks + paused) advanced only by
   explicit commands; backward transitions are structured failures.
2. Schedules/deadlines/recurrence are versioned entity components; queries are
   read-only projections; time-triggered changes are committed events.
3. Recurrence expansion is deterministic and bounded (horizon + cap).
4. No new persisted table; M1 replay unchanged.

## Consequences

- Deterministic, wall-clock-independent, replayable temporal state.
- Autonomous population scheduling (G02F) builds on these primitives.
