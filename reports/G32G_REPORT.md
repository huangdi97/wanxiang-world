# Goal G32G Acceptance Report ? Evolution Telemetry ?????

## Status
PASS

## Objective
Minimal authorized data plane for cross-world learning: metadata/hash/aggregate
by default; sensitive actor trajectories gated by retention + rights; opt-in
consent/rights policy; revocation.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/evolution/telemetry.py`:
   - `TelemetryEnvelope` (kind metadata/hash/aggregate/trajectory, consent,
     rights_ref, retention_days, aggregate/value_hash).
   - `TelemetryPolicy` ? opt-in consent required; trajectory envelopes need
     explicit rights + retention.
   - `CrossWorldDataset` ? only eligible envelopes enter; `revoke_world` applies
     the deletion/revocation policy.
   - Exported via `wanxiang_substrate.evolution` (SDK baseline +4 non-breaking).
2. `tests/unit/substrate/test_telemetry.py` (3 tests):
   - unauthorized (no consent / no rights) data never enters the dataset;
   - authorized aggregate/hash enters;
   - deletion/revocation removes a world's envelopes.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_telemetry.py -q` | 3 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=13 ts=5 py=930 (+4 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Telemetry envelope defined | PASS |
| Default metadata/hash/aggregate; trajectory gated by retention/rights | PASS |
| Opt-in / consent / rights policy | PASS |
| Unauthorized world data does not enter cross-world dataset | PASS (tested) |
| Deletion/revocation policy | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/evolution/telemetry.py,
  tests/unit/substrate/test_telemetry.py, reports/G32G_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/evolution/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g32g: Evolution Telemetry ?????`
