# Goal G21A Acceptance Report — v5.0/M17 Baseline Freeze & Repository Inventory

## Status
PASS

## Objective
Freeze reproducible pre-v5.1 evidence so consolidation cannot accidentally destroy a working M0–M17 implementation.

## Delivered
- `reports/V5_1_PRE_MIGRATION_BASELINE.md` — git/schema/fixture/API/test baseline with hashes and exact commands.
- `reports/V5_1_CODE_MINIMALITY_LEDGER.md` — initialized with before metrics and flagged consolidation candidates.
- `reports/V5_1_TRACEABILITY_MATRIX.md` — initialized with the G21A row.
- `reports/G21A_REPORT.md` — this report.
- `scripts/v51_metrics.py` — deterministic, reusable code-minimality metrics generator.
- Committed the v5.1 program pack (program docs, v5.1-R1 master spec, Goal contracts G21A–G28I, milestone gates M18–M25) as part of the baseline checkpoint so the program is reproducible from a single commit.

## Baseline regression (reproducible evidence)
- `uv run python scripts/quality.py` -> ruff PASS, ruff format PASS, pyright 0 errors, pytest 640 passed + 1 EXTERNAL_BLOCKED skip, architecture PASS. (Matches M17 final gate exactly.)
- `uv run pytest tests/unit/runtime/test_golden_replay.py tests/integration/test_g13e_history.py tests/integration/test_m1_acceptance.py tests/integration/test_persistence_sqlite.py -q` -> 26 passed. Golden v5.0 fixture readable and replay hash `7d17aba7…` stable.

## Inventory highlights
- Production: 265 files / 21,832 LOC across 10 packages + apps/api; tests 155 files (~16,280 LOC).
- Migrations head: `0002_add_event_seq_index`; SQLite default; PostgreSQL EXTERNAL_BLOCKED.
- Public API: 10 routes; SDK TS 22 tests; Python stable public names 832 (reports/SDK_API_BASELINE.md).
- Golden fixture sha256 `C158F47D…`; synthetic reference world sha256 `01168CF3…`.
- BLOCKERS.md / KNOWN_FAILURES.md empty; external blockers carried from M17 (renderers/XR, licensed source data, live PostgreSQL, real providers/sensors).

## Findings (feed-forward to G21B/G21C)
- `packages/evidence` and `packages/model_providers` are empty stub packages (5 LOC, no public names) — candidates for DELETE or consolidation.
- 26 flagged registry/manager/service/engine names across substrate/runtime/research/apps — consolidation candidates for G21C/G21F.
- No production code was changed in this Goal; the freeze is documentation + one metrics script.

## Verification
- Baseline regression repeats successfully.
- Golden v5.0 event/snapshot/package fixtures readable by current code (26 tests).
- Hash manifest deterministic (computed via Get-FileHash/known replay hashes).
- Ruff/Pyright/architecture checks PASS.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake introduced.
- No new direct canonical-state mutation path introduced.
- Traceability and code-minimality ledgers current.

## PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix
| Item | Status |
|---|---|
| Baseline freeze | PASS |
| Golden fixture replay | PASS |
| Code-minimality ledger initialized | PASS |
| M17 external blockers (real renderers/XR, licensed source data, live PG, real providers) | EXTERNAL_BLOCKED |
| M16 research tracks | EXPERIMENTAL (unchanged) |

## Remaining risks
- Baseline relies on repo-local uv cache for reproduction (user cache was sandbox-blocked in this environment; not a product issue).
- Live PostgreSQL / real-source / real-provider qualification remains EXTERNAL_BLOCKED as before.

## Changed files
- added: scripts/v51_metrics.py; reports/V5_1_PRE_MIGRATION_BASELINE.md; reports/V5_1_CODE_MINIMALITY_LEDGER.md; reports/V5_1_TRACEABILITY_MATRIX.md; reports/G21A_REPORT.md; v5.1 program pack files (committed as part of the checkpoint).

## Local commit
- Commit message: `v5.1 g21a: v5.0/m17 baseline freeze & repository inventory`
- Commit SHA: recorded below after commit.
