# Persistent Lifecycle (G06A)
Ownership: `wanxiang_substrate.lifecycle`.

## Modes
PAUSED, REALTIME, ACCELERATED, EVENT_DRIVEN, BACKGROUND_SIMULATION,
FULL_AUTONOMY, BATCH_SIMULATION. PAUSED never advances world time.

## Transitions
A deterministic transition table permits/forbids mode changes
(`can_transition`); invalid transitions raise `InvalidLifecycleTransition`.

## Persistence
Lifecycle mode is committed as a canonical `host.lifecycle` entity through the
authority, so it persists across process restarts and replays deterministically
(`LifecycleService.current`).

## Virtual clock drivers
`LifecycleService.advance(ticks)` and `advance_to` drive the deterministic
world clock via `temporal.advance`; `catch_up(target)` is the explicit
post-downtime catch-up policy. No wall-clock loops in tests.