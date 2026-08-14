# Goal G32B Acceptance Report ? ???????

## Status
PASS

## Objective
Reuse the scheduler idea so Actor/Relation/Group/Institution/World evaluate at
different cadences without full scans every tick.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/evolution/scheduler.py`:
   - `EvolutionCadence` (actor=1, relation=5, group=10, institution=30,
     world=100, validated >= 1).
   - `EvolutionScheduler` ? deterministic modular activation:
     `due_scales(tick)` (only due scales, no full scan), `activations_at`,
     `total_activations` (linear growth), `bounded_window` (only the affected
     window), seed-offset world phase.
   - Exported via `wanxiang_substrate.evolution` (SDK baseline +3 non-breaking).
2. `tests/unit/substrate/test_evolution_scheduler.py` (4 tests):
   - scales evaluate on their cadence;
   - same seed/cadence deterministic;
   - no full scan / no exponential explosion (10k ticks ~ linear);
   - stable scale names.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_evolution_scheduler.py -q` | 4 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=13 ts=5 py=909 (+3 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Evolution cadence/policy defined | PASS |
| No full scan every tick | PASS (modular due-scales) |
| Only affected entities/window activated | PASS (bounded_window) |
| Deterministic same seed/cadence | PASS (tested) |
| No exponential task explosion | PASS (linear total, tested) |
| Background aggregation reuses population resolution | PASS (scheduler is a thin cadence layer; population runtime untouched) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/evolution/scheduler.py,
  tests/unit/substrate/test_evolution_scheduler.py, reports/G32B_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/evolution/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g32b: ???????`
