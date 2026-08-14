# Goal G30F Acceptance Report ? ?? World Commit ??

## Status
PASS

## Objective
One CommitAuthority supporting State/Ontology/Law payload kinds, with
CapabilityCommit ambiguity eliminated (runtime control changes use
RuntimeControlTransaction, never a World Commit).

## Delivered
1. `packages/domain/src/wanxiang_domain/world_commit.py`:
   - `WorldCommitKind = Literal["state", "ontology", "law"]` +
     `WORLD_COMMIT_KINDS` + `DELTA_SCHEMA_VERSION = 1` +
     `validate_world_commit_kind` (rejects anything else, e.g. "capability").
2. `CommitRequest` extended with `kind: WorldCommitKind = "state"` and
   `delta_schema_version: int = DELTA_SCHEMA_VERSION` (defaults = backward
   compatible; existing callers unchanged).
3. `CommitAuthority.commit` validates the kind BEFORE preconditions/apply; the
   kind + delta_schema_version are recorded on the `AuditRecord` (reference
   view, not part of the event stream). Failure = rejection with no state
   mutation (atomic).
4. `packages/substrate/src/wanxiang_substrate/capability/runtime_control.py`:
   - `RuntimeControlTransaction` (frozen record: transaction_id, operation
     activate/deactivate/install/uninstall, provider_id, capability_name,
     version, rationale, created_at) + `RuntimeControlLedger` (append-only).
   - Explicitly NEVER a World Commit: no event_id/revision; never enters the
     canonical event stream.
5. Exported via `wanxiang_domain.__init__` (SDK baseline +6 non-breaking).

## Tests (`tests/unit/runtime/test_world_commit_kinds.py`, 5 passed)
- exactly three kinds; validation rejects "capability";
- state/ontology/law commits all pass through the single pipeline with the
  kind recorded on the audit and one event stream;
- capability kind rejected with no event appended and unchanged revision;
- RuntimeControlTransaction is NOT a World Commit (runtime control ledger only);
- RuntimeControlLedger is append-only.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/runtime/test_world_commit_kinds.py -q` | 5 passed |
| `uv run pytest tests/unit/runtime tests/integration/test_persistence_sqlite.py tests/integration/test_g14b_crash_atomicity.py tests/architecture/test_v52_baseline_fixtures.py -q` | 67 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=868 (+6 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Unified CommitRequest kind | PASS |
| Ontology/Law deltas versioned | PASS (delta_schema_version + rule/schema version) |
| Runtime control uses RuntimeControlTransaction | PASS |
| CapabilityCommit ambiguity eliminated | PASS (kind validation rejects "capability"; runtime control not a World Commit) |
| Failure atomicity | PASS (rejection with no mutation, tested) |
| No second event stream / no new Commit Authority | PASS |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/domain/src/wanxiang_domain/world_commit.py,
  packages/substrate/src/wanxiang_substrate/capability/runtime_control.py,
  tests/unit/runtime/test_world_commit_kinds.py, reports/G30F_REPORT.md
- modified: packages/runtime/src/wanxiang_runtime/authority.py,
  packages/runtime/src/wanxiang_runtime/audit.py,
  packages/domain/src/wanxiang_domain/__init__.py, reports/sdk_api_baseline.json,
  reports/SDK_API_BASELINE.md, PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g30f: ?? World Commit ??`
