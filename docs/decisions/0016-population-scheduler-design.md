# ADR-0016: Population Resolution & Autonomous Scheduler Design (G02F)

- Status: accepted
- Date: 2026-08-13

## Context

G02F needs the world to continue deterministically without user input via
multi-resolution activation and a multi-rate autonomous scheduler.

## Decision

1. Population resolution levels and rates are versioned components; the
   scheduler derives its event queue from them deterministically.
2. The scheduler submits commands (advance clock, rest, complete duty) through
   the M1 Commit Authority with deterministic command ids and bounded budgets.
3. Scheduler runs are recorded as canonical state for deterministic restore.
4. WorldRuntime caches derived state (validated against the event-store head)
   so long autonomous runs avoid O(n^2) replay; `StateReader` owns the cache.

## Consequences

- Deterministic 72-hour micro-town runs with no user input; bounded queue growth.
- Long runs are fast (validated cache); out-of-band DB writes still detected.
