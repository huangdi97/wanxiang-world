# Goal G34G Acceptance Report — M31 全平台兼容资格验收

## Status
PASS

## Objective
Freeze the v5.2 platform for real reference worlds: run full tests, migrations,
replay, architecture, SDK, security; generate the backward-compatibility report.

## Delivered
1. Full M31 gate: `uv run python scripts/quality.py` -> 819 passed + 1
   EXTERNAL_BLOCKED skip (live PostgreSQL); ruff/format/pyright/architecture PASS.
2. Gate fixes:
   - migration-head constants updated to `0004_add_world_metadata`
     (release_build, clean_room_certify, g16h/g20b/spatial tests);
   - shared action rate-limiter isolated for API smoke tests via a public
     `reset_action_rate_limiter()` helper (test-hygiene; production behavior
     unchanged).
3. `reports/V5_2_BACKWARD_COMPATIBILITY.md` — evidence: old Event/Snapshot/
   Branch replay (M26 golden hashes), migration 0001->0004 with data intact,
   API routes preserved (17 incl. new constitution/lineage/promotion), SDK
   baseline, golden replay hash unchanged.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` | ruff/format/pyright PASS; pytest 819 passed + 1 skip; architecture PASS |
| `uv run pytest tests/migration -q` | 11 passed |
| `uv run pytest tests/api tests/architecture/test_false_completion.py -q` | 26 passed |
| `uv run python scripts/sdk_baseline.py` | routes=17 ts=5 py=952 |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Full tests/migration/replay/architecture/SDK/security run | PASS |
| Backward compatibility report | PASS |
| M26 baseline explainable PASS | PASS (golden hashes) |
| No P0/P1 architecture gap | PASS |
| Report + ledgers updated | PASS |

## Changed files
- added: reports/G34G_REPORT.md, reports/M31_QUALIFICATION.md,
  reports/V5_2_BACKWARD_COMPATIBILITY.md
- modified: scripts/release_build.py, scripts/clean_room_certify.py,
  apps/api/src/wanxiang_api/routes.py, apps/api/src/wanxiang_api/limits.py,
  tests/integration/test_g16h_release.py, tests/integration/test_g20b_clean_room.py,
  tests/integration/test_spatial_movement.py,
  tests/architecture/test_false_completion.py, tests/api/test_constitution_api.py,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g34g: M31 全平台兼容资格验收`
