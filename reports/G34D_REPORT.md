# Goal G34D Acceptance Report — 旧 Event Snapshot Branch 向后回放

## Status
PASS

## Objective
Prove v5.2 is compatible with old world history using the M26 golden samples:
restore old snapshot, replay old events, fork old branch under v5.2; new
fields arrive via legacy defaults/adapter.

## Delivered
`tests/integration/test_g34d_backward_replay.py` (4 tests) against
`tests/fixtures/v5_2_baseline/`:
- replay old events (events.json) -> semantic hash matches the baseline golden;
- restore old snapshot (snapshot.json) -> hash matches; equals event replay
  (no data-clearing shortcut);
- fork old branch (branch.json parent + child) under v5.2 -> parent hash
  unchanged; child replay matches the recorded golden;
- new fields arrive via legacy defaults (old events resolve to the legacy
  VersionContext; replay deterministic under the current engine).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/integration/test_g34d_backward_replay.py -q` | 4 passed |
| `uv run pytest tests/architecture/test_v52_baseline_fixtures.py -q` | 6 passed (fixtures reproducible) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed file) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Restore old snapshot | PASS (hash matches baseline) |
| Replay old events | PASS |
| Fork old branch under v5.2 | PASS (parent unchanged) |
| New fields via legacy defaults/adapter | PASS |
| Semantic hash consistent with baseline | PASS |
| No data-clearing shortcut | PASS (snapshot == event replay) |
| Report + ledgers updated | PASS |

## Changed files
- added: tests/integration/test_g34d_backward_replay.py, reports/G34D_REPORT.md
- modified: PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g34d: 旧 Event Snapshot Branch 向后回放`
