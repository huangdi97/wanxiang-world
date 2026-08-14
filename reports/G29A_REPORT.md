# Goal G29A Acceptance Report ? ???????? M25 ????

## Status
PASS

## Objective
Freeze the reproducible pre-v5.2 baseline and verify that prior M0?M25 completion
claims correspond to real code, migrations, tests and reports ? before any v5.2
semantic work begins.

## Delivered
- `reports/V5_2_BASELINE_AUDIT.md` ? full baseline freeze: git head/branch, environment,
  quality-gate results, pre-existing defects found and fixed (D1?D4), golden fixtures,
  production inventory, backward-compatibility anchors.
- `tests/fixtures/v5_2_baseline/` ? deterministic golden fixtures: events, snapshot,
  branch, worldpack, api, manifest (combined semantic hash `f27b7724...`).
- `scripts/generate_v52_baseline_fixtures.py` ? deterministic fixture generator
  (stable across repeated runs; random commit metadata normalized).
- `tests/architecture/test_v52_baseline_fixtures.py` ? 6 reproducibility tests (PASS).
- Deleted the two empty stub packages `packages/evidence` and `packages/model_providers`
  and all their references (pyproject extraPaths, architecture guards, dependency
  graph golden edges, bootstrap test, uv.lock) ? a v5.2 preparation change validated
  by full regression (KEEP/MERGE/ADAPT matrix: DELETE with zero call sites).
- Repaired the v5.2 preparation edit that had corrupted `scripts/architecture_check.py`
  and `scripts/architecture_forensics.py` (restored `packages/observability` and
  `packages/substrate` forbidden-import entries; removed only the two stub entries).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` | ruff check PASS; ruff format PASS; pyright 0 errors; pytest 649 passed + 1 EXTERNAL_BLOCKED skip (live PostgreSQL); architecture conformance PASS |
| `uv run pytest tests/architecture/test_v52_baseline_fixtures.py -q` | 6 passed |
| `uv run pytest tests/unit/runtime/test_golden_replay.py tests/integration/test_g13e_history.py tests/integration/test_m1_acceptance.py tests/integration/test_persistence_sqlite.py -q` | 26 passed (M17 critical set) |
| `uv run python scripts/generate_v52_baseline_fixtures.py` (x2) | identical combined hash `f27b77249f14c6ef5b8b1b10689e69659e9405d6ccf6f0c75d3f4be952c47ecf` |
| `uv run python scripts/v51_metrics.py` | 263 files / 21,822 LOC / 524 classes / 186 funcs; 11 registries, 0 managers, 15 services, 3 engines |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| M17/M25 reports + git history read; current commit/branch recorded | PASS |
| Full existing quality suite executed and recorded | PASS (green after D1?D4 fixes) |
| Old Event stream / Snapshot / WorldPack / Branch / API fixtures frozen | PASS |
| Production LOC / package / registry / manager / service / engine counts recorded | PASS |
| v5.2 baseline manifest + semantic hash generated | PASS |
| No TODO/placeholder/mock-only path introduced; no new Commit Boundary bypass | PASS |
| No new duplicate Registry/Manager/Engine/State/Event/Branch abstraction | PASS |
| No persisted schema change (migration head unchanged `0002`) | PASS (not applicable) |
| PLAN/STATUS/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG + final acceptance matrix + minimality ledger updated | PASS |
| External source data (Red Chamber) | EXTERNAL_BLOCKED (unchanged; handled in G35A) |

## Changed files
- added: README_FIRST_V5_2_CN.md, 00?10 v5.2 program docs, docs/spec/WANXIANG_v5_2_MASTER_SPEC.md,
  goals/G29A..G37G, milestones/M26..M34, CODEX_??????_??.txt,
  WANXIANG_V5_2_M26_M34_??????_ALL_IN_ONE_??.md, scripts/generate_v52_baseline_fixtures.py,
  tests/architecture/test_v52_baseline_fixtures.py, tests/fixtures/v5_2_baseline/*,
  reports/V5_2_BASELINE_AUDIT.md, reports/G29A_REPORT.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md,
  reports/V5_2_CODE_MINIMALITY_LEDGER.md
- deleted: packages/evidence/*, packages/model_providers/*
- modified: PACK_MANIFEST.md, pyproject.toml, uv.lock, scripts/architecture_check.py,
  scripts/architecture_forensics.py, scripts/false_completion_scan.py,
  scripts/v51_dependency_graph.py, scripts/v51_metrics.py,
  tests/architecture/test_v51_dependency_topology.py,
  tests/architecture/test_v51_forensics.py, tests/unit/test_bootstrap.py,
  PLAN.md, STATUS.md, DECISIONS.md, BLOCKERS.md, KNOWN_FAILURES.md, CHANGELOG.md

## Risks / remaining
- The v5.1 program ended with M18 (G21A?G21D) completed; M19?M25 gates were not
  executed in the v5.1 batch. G29A freezes the *actual* current state (M25 claims are
  the v5.0/M17 final certification plus v5.1 M18 partial), which is now the honest
  v5.2 start line. M26?M34 will be executed in order from here.
- 140 tracked `.md` files carry UTF-8 BOMs (cosmetic; see KNOWN_FAILURES).

## Local commit
- Message: `g29a: ???????? M25 ????`
