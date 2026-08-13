# ADR-0035: Persistent Lifecycle Design (G06A)
- Status: accepted
- Date: 2026-08-13

## Context
G06A needs persistent lifecycle modes with pause/advance/background semantics
and deterministic virtual-clock drivers.

## Decision
1. Lifecycle modes (PAUSED..BATCH_SIMULATION) follow a deterministic transition
   table; invalid transitions raise.
2. Mode is committed as a canonical `host.lifecycle` entity so it persists and
   replays; PAUSED never advances world time.
3. Virtual-clock drivers use `temporal.advance`; no wall-clock loops in tests.

## Consequences
- Lifecycle persists independently of sessions; restart recovers mode
  deterministically.