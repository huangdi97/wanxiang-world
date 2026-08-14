# Goal G31B Acceptance Report ? World Lineage Graph ????

## Status
PASS

## Objective
First-class DAG storage and query of world definition / worldline derivation
relationships (fork/promotion origins, inherited history refs, constitution/
domain/runtime/evolution versions, rights/provenance), with cycle rejection.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/lineage/graph.py`:
   - `LineageNode` ? kind (definition/worldline/derived_world), definition_ref,
     inherited_history_ref, constitution/domain/runtime versions,
     evolution_policy, rights_ref, provenance (references only, never history).
   - `LineageEdge` ? parent->child with edge_kind (fork|promotion) + origin_ref.
   - `LineageGraph` ? in-memory DAG: add_node/add_edge with duplicate + cycle
     rejection; ancestors/descendants/common_ancestors queries; nodes/edges
     listing.
   - `wanxiang_substrate.lineage` package (SDK baseline +5 non-breaking).
2. `tests/unit/substrate/test_lineage_graph.py` (5 tests):
   - tree fixture queries (ancestors/descendants/common ancestors);
   - DAG (diamond) fixture queries;
   - cycle insertion rejected (incl. self-edge);
   - duplicate node/edge rejected;
   - node carries versions/rights/provenance.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_lineage_graph.py -q` | 5 passed |
| `uv run pytest tests/unit/substrate/ -q` | 68 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=888 (+5 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Lineage node/edge defined | PASS |
| fork/promotion origin + inherited history ref + versions + rights/provenance | PASS |
| Cycle rejection | PASS (tested) |
| Tree + DAG fixtures | PASS |
| Ancestor/descendant/common-ancestor queries | PASS |
| No history copied in graph | PASS (references only) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/lineage/graph.py,
  packages/substrate/src/wanxiang_substrate/lineage/__init__.py,
  tests/unit/substrate/test_lineage_graph.py, reports/G31B_REPORT.md
- modified: reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g31b: World Lineage Graph ????`
