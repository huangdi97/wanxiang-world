# P0 Gap Backlog (G13H)

Every internally actionable P0 gap discovered by G13A-G13G, its root cause, the
fix commit, the regression test, and closure status. P0 open count target = 0.

| ID | Goal found | Title | Root cause | Fix | Regression test | Status |
|---|---|---|---|---|---|---|
| P0-1 | G13E | Child-branch cold replay / restore_and_replay fails | ReplayEngine conflated branch-local `event_seq` with global `revision`; forked worlds could not be rebuilt from events after restart/cache invalidation (`CorruptEventStream expected event seq 3, got 1`) | replay.py checks `event_seq` and `revision` as independent counters with explicit `start_seq` (child branches pass 1; snapshot continuation defaults to baseline.revision+1); StateReader + WorldRuntime wired | tests/integration/test_g13e_history.py::test_branch_ancestry_isolation_via_runtime (cold cache + restore_and_replay hash equality) | CLOSED (G13E, commit 45b0c91) |
| P0-2 | G13D | Architecture placeholder guard only checked the first pattern | `scan_placeholders` used `next((pattern.search(line) for pattern in PLACEHOLDER_PATTERNS), None)` which returns the FIRST pattern's result (None for TODO) and never advanced; FIXME/XXX/NotImplemented/placeholder/stub/mock-only were silently unchecked in production | guard now scans all patterns (first non-None match) with a documented `return NotImplemented` rich-comparison exception | tests/architecture/test_false_completion.py::test_placeholder_guard_catches_every_marker + test_placeholder_guard_allows_return_notimplemented | CLOSED (G13D, commit 0aad76e) |
| P0-3 | G13D | OpenAPI/SDK schema drift: documented vocabulary did not exist on the server | TS SDK stable document listed `/worlds/{id}/projection` + `/commands`; server exposes `/worlds`, `/state`, `/events`, `/actions`, `/checkpoint`, `/replay`, `/branches`, `/branches/compare`, `/healthz` | FastAPI app is the single source of truth: `scripts/export_openapi.py` exports `packages/sdk_ts/src/openapi-contract.json` (10 ops); TS test consumes it; Python drift test regenerates + compares | tests/architecture/test_false_completion.py::test_openapi_contract_matches_server + test_openapi_contract_detects_manual_edit | CLOSED (G13D, commit 0aad76e) |

## Open P0
- P0 open count: **0**
- Remaining items in this backlog are EXTERNAL_BLOCKED (real corpora/providers/hardware) and are not internal P0 defects.
