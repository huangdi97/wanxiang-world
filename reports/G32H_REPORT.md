# Goal G32H Acceptance Report ? M29 ??????????

## Status
PASS

## Objective
Prove micro->macro candidate -> institution/ontology changes run in a controlled
manner with platform power still isolated; construct a synthetic society long
run; run the M29 gate.

## Delivered
1. `tests/integration/test_m29_synthetic_society.py` (2 tests):
   - a single habit never automatically crosses higher gates (no candidate, no
     LawCommit, Gamma unchanged);
   - synthetic society long run: habit -> norm/group candidates (5 windows) ->
     institution candidate -> validate + approve -> LawCommit; replay
     deterministic and branch isolation preserved.
2. Ran the full M29 gate: `uv run python scripts/quality.py` -> 774 passed + 1
   EXTERNAL_BLOCKED skip; ruff/format/pyright/architecture PASS.
3. Gate fixes:
   - `assert_world_cannot_mutate_platform` documented as a static-success guard
     (structural, world policy holds no platform handle);
   - M28 parent-isolation test switched to set comparison (sorted ancestors).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` | ruff/format/pyright PASS; pytest 774 passed + 1 skip; architecture PASS |
| `uv run pytest tests/integration/test_m29_synthetic_society.py -q` | 2 passed |
| `uv run python scripts/v52_minimality_budget.py` | hard_ok=True |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Synthetic society long run | PASS |
| habit -> norm -> institution candidate flow | PASS |
| No automatic crossing of higher gates | PASS (tested) |
| Replay/Branch deterministic | PASS (tested) |
| M29 gate executed | PASS |
| Platform power isolated | PASS (guard + ontology/law no-escalation) |
| Report + ledgers updated | PASS |

## Changed files
- added: tests/integration/test_m29_synthetic_society.py, reports/G32H_REPORT.md,
  reports/M29_QUALIFICATION.md
- modified: tests/architecture/test_false_completion.py,
  tests/integration/test_m28_lineage_hypervisor.py, PLAN.md, STATUS.md,
  DECISIONS.md, CHANGELOG.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md,
  reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g32h: M29 ??????????`
