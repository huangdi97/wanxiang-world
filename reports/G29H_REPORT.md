# Goal G29H Acceptance Report ? M26 ??????

## Status
PASS

## Objective
Prove the repo completed the subtraction baseline before v5.2 semantic work and
that old capabilities are unbroken: run the M26 milestone gate, fix every
internal FAIL, and freeze the new architecture map + baseline hash.

## Delivered
1. Ran the full M26 gate (`milestones/M26_QUALIFICATION.md` requirements).
2. Fixed the two gate FAILs found by the full regression:
   - pyright: `WorldRuntimePort.submit_command` parameter name renamed
     `envelope` -> `command` so pyright protocol matching accepts the
     application `WorldRuntime` implementation (38 errors -> 0).
   - SDK contract: restored the `SnapshotStore` deprecated alias
     (`recovery.checkpoint.SnapshotStore = CheckpointStore`, re-exported) so the
     public SDK surface has no breaking removal; regenerated
     `reports/sdk_api_baseline.json` + `SDK_API_BASELINE.md` (additions:
     CheckpointStore, WorldRuntimePort, WorldCreateResult - non-breaking).
3. `reports/M26_QUALIFICATION.md` ? full gate evidence.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` | ruff check PASS; ruff format PASS; pyright 0 errors; pytest 664 passed + 1 EXTERNAL_BLOCKED skip (live PostgreSQL); architecture conformance PASS |
| `uv run pytest tests/architecture/test_v52_baseline_fixtures.py tests/architecture/test_v52_minimality_budget.py tests/architecture/test_v51_forensics.py tests/architecture/test_v51_dependency_topology.py -q` | 14 passed |
| `uv run pytest tests/integration/test_g17a_sdk_contract.py -q` | 3 passed |
| `uv run python scripts/v52_minimality_budget.py` | hard_ok=True; 264 files / 21,901 LOC / 10 regs / 0 mgrs / 15 svcs / 2 engines / 23 ports / 0 cycles / 1 commit path |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=842 |

## Frozen anchors
- Architecture map: `reports/V5_1_PACKAGE_DEPENDENCY_GRAPH.md` (regenerated,
  acyclic; substrate = domain+runtime after G29E).
- v5.2 baseline combined hash: `f27b77249f14c6ef5b8b1b10689e69659e9405d6ccf6f0c75d3f4be952c47ecf`
  (G29A fixtures unchanged and still reproducible).
- Migration head: `0002_add_event_seq_index` (unchanged; migration tests green).

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| M26 milestone gate executed | PASS |
| Internal FAILs fixed | PASS (pyright protocol param; SDK baseline alias + regen) |
| Old full regression | PASS (664 + 1 skip) |
| Architecture map + baseline hash frozen | PASS |
| Minimality report exists | PASS (V5_2_MINIMALITY_BUDGET.md) |
| Disposition table has no unclassified core module | PASS (V5_2_CODE_DISPOSITION_ACTUAL.md) |
| Report + ledgers updated | PASS |

## Changed files
- modified: packages/substrate/src/wanxiang_substrate/runtime_port.py,
  packages/substrate/src/wanxiang_substrate/recovery/checkpoint.py,
  packages/substrate/src/wanxiang_substrate/recovery/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md
- added: reports/G29H_REPORT.md, reports/M26_QUALIFICATION.md

## Local commit
- Message: `g29h: M26 ??????`
