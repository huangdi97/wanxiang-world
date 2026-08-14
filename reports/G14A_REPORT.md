# Goal G14A Acceptance Report — Concurrency, Race, Idempotency & Lost-update Adversarial Qualification

## Status
PASS

## Objective
Attack concurrent command submission and revision semantics to prove multi-client activity cannot fork reality accidentally or duplicate effects.

## Delivered
- `tests/integration/test_g14a_concurrency.py` — 5 deterministic adversarial tests (no reliance on thread timing).
- `reports/CONCURRENCY_ADVERSARIAL.md` — strategy, scenarios, performance tradeoffs, evidence.
- `reports/G14A_REPORT.md`.

## Findings
- No lost update: second writer with stale revision gets explicit StaleRevision; no invalid event appended.
- Duplicate command id across a simulated restart produces exactly one semantic effect (duplicate=True, same event).
- Out-of-order delivery fails explicitly and recovers.
- Independent instances/branches progress without cross-contamination (distinct streams and hashes).

## Evidence
- `uv run pytest tests/integration/test_g14a_concurrency.py -q` -> 5 passed.
- Quality gate remains green (428 tests at M10 checkpoint; G14A adds 5 adversarial tests).

## Remaining limitations
- Thread-level interleaving is not simulated (deterministic revision semantics cover the adversarial cases);
  real multi-process coordination is out of scope for the modular monolith profile.

## Final checkpoint
- commit: `g14a: concurrency, race, idempotency & lost-update adversarial qualification`
