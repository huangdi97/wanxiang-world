# Goal G15B Acceptance Report — Comprehensive Synthetic Reference World Package

## Status
PASS

## Objective
Build a nontrivial synthetic world outside Core that exercises space, time, material custody, bodies, institutions, cognition, action, host, evidence, challenges and projections together.

## Delivered
- `reference_worlds/synthetic_full/` — synthetic pack (README + content module) via the public path.
- `tests/integration/test_g15b_synthetic_world.py` — 4 tests.
- `reports/SYNTHETIC_REFERENCE_WORLD_BUILD.md`, `reports/G15B_REPORT.md`.

## Findings
- Fresh build/install/instantiate works through public package/runtime contracts (no Core modification).
- Package install/upgrade leaves other worlds intact.
- Content imports only public SDK surfaces (no Core internals).
- Worldness eval cases (persistence, spatial/material/custody, social, cognitive, replay) pass.

## Evidence
- 4 tests passed; ruff/pyright clean.
- The synthetic full world becomes the mandatory regression world for subsequent releases.

## Remaining limitations
- Real copyrighted/historical data not used; all content synthetic (EXTERNAL_BLOCKED for real slices).

## Final checkpoint
- commit: `g15b: comprehensive synthetic reference world package`
