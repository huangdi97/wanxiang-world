# Goal G29D Acceptance Report ? ?? State Event Audit ????

## Status
PASS

## Objective
Ensure only Committed History is authoritative and CurrentState / Projection /
Audit views are rebuildable from or reference the history/ledger.

## Delivered (verification + tests)
The repository already implements the target derivation model; G29D added
crisp regression evidence for each invariant:
1. `tests/integration/test_g29d_state_event_audit.py` (2 tests):
   - `test_current_state_is_rebuildable_materialized_projection`: creates a
     world, commits 3 events, materializes a checkpoint (derived state), then
     DELETES all snapshot rows and invalidates the in-memory read cache; the
     state is rebuilt from events with the identical semantic hash, and
     `restore_and_replay` falls back to event replay (`used_snapshot=False`)
     with the same hash; direct `ReplayEngine` replay also matches.
   - `test_audit_rows_reference_events_and_are_not_authoritative`: after a
     commit, the `audit_traces` row references the committed event
     (`event_id`/`trace_id`/`command_id`/`actor_id`) and carries no duplicate
     delta payload (`no delta_json` column); deleting audit rows never changes
     the canonical replay hash.

## Findings (evidence)
- Persistence schema (`migrations/0001_initial.py`) has exactly one
  authoritative stream: `events` (committed history). `world_instances` /
  `branches` are metadata; `snapshots` is a cache (state_json + content_ref);
  `audit_traces` is a reference view (no delta_json column). There is NO
  second authoritative state table.
- `StateReader.state_at` derives state from events (optional snapshot baseline
  + replay), validates cache freshness against the event-store head, and
  exposes `invalidate()` ? the read cache is a discardable projection.
- `CommitAuthority.commit` is the only write path (1 commit_paths);
  `apps/api` forbidden-imports include `sqlalchemy`/`alembic`/`wanxiang_persistence`,
  so routes/providers cannot write canonical tables directly (architecture
  guard, verified by `tests/architecture/test_architecture_guards.py`).
- Audit records are written by `AuditTraceRepository` (persistence) with
  reference fields only; `CommitAuthority` emits the audit after append.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/integration/test_g29d_state_event_audit.py -q` | 2 passed |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |
| `uv run python scripts/architecture_check.py` | PASS (in quality gate) |
| `uv run python scripts/v51_forensics.py` | commit_paths 1 (unchanged) |
| Golden replay regression | unchanged (replay hash invariant already pinned) |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| CurrentState confirmed as materialized projection | PASS |
| Second authoritative state path | PASS (none exists) |
| Duplicate audit writes -> Ledger references | PASS (audit references events; no delta duplication) |
| Projection cache drop-and-rebuild | PASS (tested) |
| No route/provider direct canonical write | PASS (architecture guard + tests) |
| Replay hash invariant | PASS |
| Report + ledgers updated | PASS |

## Changed files
- added: tests/integration/test_g29d_state_event_audit.py, reports/G29D_REPORT.md
- updated: PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g29d: ?? State Event Audit ????`
