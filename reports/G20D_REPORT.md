# Goal G20D Acceptance Report ? Black-box External Author + Reference World Final Acceptance

## Status
PASS

## Objective
Perform a black-box final acceptance as three external personas (package author, operator, end
user) plus product-surface smoke, using only public docs/SDK/UI/API and release artifacts.

## Delivered
- `scripts/blackbox_final_acceptance.py` ? automated 4-persona black-box acceptance writing
  `reports/BLACKBOX_FINAL_ACCEPTANCE.md`.
- `tests/integration/test_g20d_blackbox_acceptance.py` ? 4 regression tests.
- `reports/BLACKBOX_FINAL_ACCEPTANCE.md`, `reports/G20D_REPORT.md`.

## Findings (all PASS)
- Author: external sample pack built with public SDK only, published + installed via public registry
  lifecycle, custom domain action ran; no Core modification.
- Operator: private/staging deploy via documented ops tooling; backup/restore round-trip with replay
  hash preserved.
- End user: entered synthetic living world, exited/rejoined (session-independent persistence),
  branched with divergent action (parent truth unchanged), replayed to the same hash.
- Surfaces: 10 API routes, 0 write-API violations, branch-aware projection smoke (21 items).

## Decision
Black-box platform claim proven. No internal shortcuts or DB edits used; no P0/P1 usability blocker.

## Evidence
- `uv run python scripts/blackbox_final_acceptance.py` -> exit 0, all 4 personas PASS.
- `uv run pytest tests/integration/test_g20d_blackbox_acceptance.py -q` -> 4 passed.
- Full M17 gate green (628+ pytest, ruff/pyright/architecture PASS).

## Final checkpoint
- commit: `g20d: black-box external author + reference world final acceptance`
