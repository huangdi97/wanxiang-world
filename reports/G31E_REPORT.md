# Goal G31E Acceptance Report ? Interworld Identity ? Presence

## Status
PASS

## Objective
Cross-world presence references with NO implicit two-way history sync: entering
another world requires an explicit presence/translation policy; return/sync is
explicit-policy only.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/lineage/presence.py`:
   - `OriginIdentity` ? home identity (entity_id, origin worldline/instance,
     canonical_ref).
   - `PresenceRef` ? a subject's presence in a host world with explicit
     translation_policy (mirror/isolated/mapped) + sync_policy
     (none/one_way_out/explicit_only) + mapped_local_id.
   - `PresenceRegistry` ? thin registry: `enter(...)` (rejects identity
     conflicts unless mapped), `leave(...)`, `get(...)`,
     `can_sync_back(presence)` (explicit policy required).
   - Exported via `wanxiang_substrate.lineage` (SDK baseline +5 non-breaking).
2. `tests/unit/substrate/test_presence.py` (4 tests):
   - entering generates explicit policy (no implicit write-back);
   - B-world experiences do NOT write back to A (can_sync_back False by
     default; explicit_only enables an explicit step);
   - identity conflict rejected unless mapped (mapped_local_id distinct);
   - presence round-trip + leave.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_presence.py -q` | 4 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=899 (+5 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| OriginIdentity / PresenceRef defined | PASS |
| Entering a world generates explicit presence/translation policy | PASS |
| Return/sync requires explicit policy | PASS (can_sync_back) |
| B-world experiences don't write back to A | PASS (tested) |
| Identity conflict explicitly rejected or mapped | PASS (tested) |
| No dual-write / history copy | PASS |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/lineage/presence.py,
  tests/unit/substrate/test_presence.py, reports/G31E_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/lineage/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g31e: Interworld Identity ? Presence`
