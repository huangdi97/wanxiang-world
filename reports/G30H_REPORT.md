# Goal G30H Acceptance Report ? Event Snapshot ???????

## Status
PASS

## Objective
Keep history interpretable and replayable after Constitution / Sigma / Gamma
evolution, with minimized storage, frozen snapshot version refs, and a legacy
adapter for old events.

## Delivered
1. `packages/domain/src/wanxiang_domain/version_context.py`:
   - `VersionContext` ? frozen, versioned record of constitution_version /
     semantic_space_version / law_set_version + optional domain_ref /
     runtime_ref (minimized: one record, not per-event duplication), with
     canonical hash.
   - `legacy_version_context(rule_version, schema_version)` ? adapter for old
     v5.0/v5.1 events (constitution 1 / semantic 1 / law 0).
   - `VersionContextEntry` + `extend(log, entry)` ? immutable append-only log
     (monotonic by revision).
   - `resolve_context(revision, log)` ? nearest preceding context, else legacy.
   - `SnapshotVersionContext` ? freezes the context a snapshot was created
     under (instance/branch/revision/event_seq + context hash).
   - Exported via `wanxiang_domain.__init__` (SDK baseline +7 non-breaking).
2. `tests/unit/domain/test_version_context.py` (6 tests):
   - legacy adapter handles old events;
   - v5.1 golden fixture replay UNCHANGED (semantic hash
     7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00);
   - context log resolves nearest preceding entry (incl. legacy fallback);
   - context log is append-only/monotonic;
   - replay deterministic before/after Law/Ontology evolution (context is
     metadata, never part of the semantic hash);
   - snapshot version context freeze round-trip.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/domain/test_version_context.py -q` | 6 passed |
| `uv run pytest tests/unit/domain/ -q` | 55 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=877 (+7 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Events reference constitution/semantic/law/domain/runtime version (minimized) | PASS (VersionContext + immutable log) |
| Snapshot freezes version refs | PASS (SnapshotVersionContext) |
| Legacy adapter for old events | PASS (legacy_version_context + golden replay) |
| v5.0/v5.1 fixture replay | PASS (golden hash unchanged) |
| Replay deterministic before/after Law/Ontology | PASS (tested) |
| No event-schema change / no second stream | PASS (context is metadata) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/domain/src/wanxiang_domain/version_context.py,
  tests/unit/domain/test_version_context.py, reports/G30H_REPORT.md
- modified: packages/domain/src/wanxiang_domain/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g30h: Event Snapshot ???????`
