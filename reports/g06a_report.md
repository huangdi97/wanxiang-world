# Goal G06A Acceptance Report
## Status
PASS
## Objective
Persistent lifecycle with pause/advance/background and deterministic virtual
clock drivers.
## Delivered
- `wanxiang_substrate.lifecycle`: 7 modes, deterministic transition table,
  canonical `host.lifecycle` persistence, LifecycleService (set_mode/advance/
  catch_up), budget-gated background.
## Test evidence
- unit: every allowed/forbidden transition; integration: background advances
  without active session; pause stops advancement; lifecycle recovers
  deterministically; catch-up after downtime; budget blocks runaway loop.
## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Transition permissions | PASS | unit tests |
| Background advance without session | PASS | integration test |
| Pause stops advancement | PASS | integration test |
| Lifecycle persists/recovers | PASS | canonical entity + replay |
| Budget respected | PASS | BudgetExceeded test |
## Final checkpoint
- commit: `goal g06a: persistent lifecycle, pause, advance & background`