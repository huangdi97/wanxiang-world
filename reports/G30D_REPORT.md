# Goal G30D Acceptance Report ? World Semantic ISA ????

## Status
PASS

## Objective
Implement minimal typed semantic instructions (DECLARE/ASSERT/RETRACT/PROPOSE/
VALIDATE/COMMIT/FORK/PROMOTE) without a parallel command bus, and make the ISA
the reduction target for compiler/domain/actions while business actions stay at
the upper layer.

## Delivered
1. `packages/domain/src/wanxiang_domain/world_isa.py`:
   - `WorldIsaInstruction` (Literal union of the 8 instructions) +
     `ISA_INSTRUCTIONS` tuple + `ISA_VERSION`/`ISA_SUPPORTED_VERSIONS`.
   - `WorldIsaOp` ? frozen discriminated payload (op/version/payload); unknown
     instruction or unsupported version fails explicitly at construction and
     at parse.
   - `isa_op_from_primitive` / `to_primitive` ? schema round-trip.
   - `reduce_isa_to_delta` ? data instructions reduce to existing deltas
     (DECLARE -> EntityCreate, ASSERT -> RelationCreate, RETRACT -> EntityDelete/
     RelationDelete, PROPOSE -> ProposedWorldDelta via delta_from_primitive);
     control instructions (VALIDATE/COMMIT/FORK/PROMOTE) map to existing use
     cases and return None here.
   - Documented reduction mapping (single commit boundary, fork reuses branch
     semantics, PROMOTE -> promotion pipeline in later Goals).
   - Exported via `wanxiang_domain.__init__` (SDK baseline +8 non-breaking).
2. `tests/unit/domain/test_world_isa.py` (10 tests):
   - exactly 8 instructions + version; schema round-trip;
   - unknown version fails; unknown instruction fails;
   - DECLARE/ASSERT/RETRACT/PROPOSE reduce to expected deltas;
   - control instructions reduce to None;
   - no direct DB write (no sqlalchemy/persistence/fastapi/httpx imports);
   - business actions stay at the upper layer (PROPOSE carries an existing
     delta payload).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/domain/test_world_isa.py -q` | 10 passed |
| `uv run pytest tests/unit/domain/ -q` | 49 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=860 (+8 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| ISA enum / discriminated payload | PASS |
| Instruction schema + version recorded | PASS (ISA_VERSION, round-trip, unknown-version fail) |
| ISA as reduction target for compiler/domain/action | PASS (reduce_isa_to_delta) |
| Business actions stay at upper layer | PASS (tested; no application action in ISA) |
| No parallel command bus / giant interpreter | PASS (data ops -> deltas; control ops -> use cases) |
| Unknown ISA version fails explicitly | PASS |
| No direct DB write | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/domain/src/wanxiang_domain/world_isa.py,
  tests/unit/domain/test_world_isa.py, reports/G30D_REPORT.md
- modified: packages/domain/src/wanxiang_domain/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g30d: World Semantic ISA ????`
