# Goal G31A Acceptance Report ? World Definition ? Worldline ????

## Status
PASS

## Objective
Formalize the identity relationships between WorldPack/Definition, Instance,
Worldline/Branch, and Derived World without creating a second history object.

## Delivered
1. `packages/domain/src/wanxiang_domain/worldline.py`:
   - `WorldDefinitionId` (wd) + `WorldlineId` (wl) added to ids.py.
   - `WorldDefinition` ? read-only, versioned birth definition (definition_id,
     version, name, constitution_ref, genesis_ref, package_ref, content_hash);
     immutable (no mutation API).
   - `WorldlineIdentity` ? continuous-history view (worldline_id, instance_id,
     root_branch_id, definition_ref, constitution_ref); the root branch is the
     start node, so a Branch fork IS a worldline fork relationship (reusing
     BranchAncestry), never a second history object.
   - `InstanceIdentity` ? an instance records definition/genesis/constitution/
     runtime refs.
   - `WorldlineFork` ? a branch fork formalized as a worldline fork record
     (parent_worldline/parent_branch/child_branch/fork_revision/fork_event_seq).
   - Exported via `wanxiang_domain.__init__` (SDK baseline +6 non-breaking).
2. `tests/unit/domain/test_worldline.py` (4 tests):
   - world definition is read-only + versioned (frozen, hashed, no mutation);
   - WorldPack unchanged by running (replay + instance identity don't touch the
     definition hash);
   - branch fork is a worldline fork relationship (round-trip identity);
   - instance identity round-trip.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/domain/test_worldline.py -q` | 4 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=883 (+6 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Stable IDs + references | PASS |
| Branch modeled as worldline fork (no second history object) | PASS (WorldlineFork over BranchAncestry) |
| World Definition read-only versioned | PASS (tested) |
| Instance records definition/genesis/constitution/runtime refs | PASS (tested) |
| Parent/child identity round-trip | PASS (tested) |
| WorldPack unchanged by running | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/domain/src/wanxiang_domain/worldline.py,
  tests/unit/domain/test_worldline.py, reports/G31A_REPORT.md
- modified: packages/domain/src/wanxiang_domain/ids.py,
  packages/domain/src/wanxiang_domain/__init__.py, reports/sdk_api_baseline.json,
  reports/SDK_API_BASELINE.md, PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g31a: World Definition ? Worldline ????`
