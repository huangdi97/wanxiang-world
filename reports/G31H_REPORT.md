# Goal G31H Acceptance Report ? M28 Lineage Hypervisor ????

## Status
PASS

## Objective
Prove multiple worlds/worldlines and derivation relationships are isolated and
traceable; run the M28 gate; generate lineage graph fixture + visualization.

## Delivered
1. Ran the full M28 gate: `uv run python scripts/quality.py` -> 747 passed + 1
   EXTERNAL_BLOCKED skip (live PostgreSQL); ruff/format/pyright/architecture PASS.
2. Gate fixes surfaced by the full regression:
   - `packages/persistence` had imported `wanxiang_substrate.lineage` (a new
     persistence->substrate inversion). Fixed by moving the lineage graph model
     to `wanxiang_domain.lineage`; `wanxiang_substrate.lineage.graph` is now a
     thin re-export; persistence imports domain (allowed).
   - Migration head constant updates: `EXPECTED_MIGRATION_HEAD` (release_build)
     and `MIGRATION_HEAD` (clean_room_certify) -> `0003_add_lineage`; three
     release/clean-room/spatial tests updated.
   - Budget anchor: registry_classes 10 -> 11 (PresenceRegistry, M28).
3. Lineage graph fixture + visualization:
   - `scripts/generate_lineage_fixture.py` (deterministic) ->
     `tests/fixtures/v5_2_lineage_graph.json` + `reports/V5_2_LINEAGE_GRAPH.md`
     (mermaid diagram + tables, 4 nodes / 3 edges incl. a promotion edge).
   - `tests/architecture/test_v52_lineage_fixture.py` (3 tests): fixture
     regenerates stably, hash matches content, fixture is a valid lineage DAG.
4. `tests/integration/test_m28_lineage_hypervisor.py` (2 tests):
   - parent not modified by child or promotion (parent hash/events unchanged);
   - multi-instance replay independent (same local id, different hashes).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` | ruff/format/pyright PASS; pytest 747 passed + 1 skip; architecture PASS |
| `uv run pytest tests/integration/test_m28_lineage_hypervisor.py tests/architecture/test_v52_lineage_fixture.py -q` | 5 passed |
| `uv run python scripts/generate_lineage_fixture.py` | fixture + visualization written (deterministic) |
| `uv run python scripts/v52_minimality_budget.py` | hard_ok=True; registries 11; 0 cycles; 1 commit path |
| `uv run python scripts/v51_forensics.py` | commit_paths 1 |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| M28 gate executed | PASS |
| Parent not modified by child/promotion | PASS (tested) |
| Multi-instance replay independent | PASS (tested) |
| Lineage graph fixture + visualization | PASS |
| No persistence->substrate inversion | PASS (fixed; topology green) |
| Migration head consistency (0003) | PASS (constants + tests updated) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/domain/src/wanxiang_domain/lineage.py,
  scripts/generate_lineage_fixture.py, tests/fixtures/v5_2_lineage_graph.json,
  tests/architecture/test_v52_lineage_fixture.py,
  tests/integration/test_m28_lineage_hypervisor.py,
  reports/V5_2_LINEAGE_GRAPH.md, reports/G31H_REPORT.md,
  reports/M28_QUALIFICATION.md
- modified: packages/substrate/src/wanxiang_substrate/lineage/graph.py,
  packages/persistence/src/wanxiang_persistence/lineage_repository.py,
  scripts/release_build.py, scripts/clean_room_certify.py,
  tests/architecture/test_v52_minimality_budget.py,
  tests/integration/test_g16h_release.py, tests/integration/test_g20b_clean_room.py,
  tests/integration/test_spatial_movement.py,
  reports/V5_1_DUPLICATE_FORENSICS.md, reports/V5_2_MINIMALITY_BUDGET.md,
  reports/v52_minimality_budget.json, reports/sdk_api_baseline.json,
  reports/SDK_API_BASELINE.md, PLAN.md, STATUS.md, DECISIONS.md,
  CHANGELOG.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md,
  reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g31h: M28 Lineage Hypervisor ????`
