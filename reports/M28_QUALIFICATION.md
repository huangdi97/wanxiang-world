# M28 ? Worldline / Lineage / Hypervisor Milestone Qualification

## Status: PASS

## Preconditions (all PASS)
| Goal | Status |
|---|---|
| G31A World Definition ? Worldline ???? | PASS (commit g31a) |
| G31B World Lineage Graph ???? | PASS (commit g31b) |
| G31C Lineage Repository ??? | PASS (commit g31c) |
| G31D World Hypervisor ????? | PASS (commit g31d) |
| G31E Interworld Identity ? Presence | PASS (commit g31e) |
| G31F Hybrid Genesis ?????????? | PASS (commit g31f) |
| G31G Lineage API SDK Studio ???? | PASS (commit g31g) |
| G31H M28 Lineage Hypervisor ???? | PASS (this gate) |

## Commit range
- From: `a3601d9` (M27 gate PASS)
- To: HEAD at M28 PASS (g31a..g31h commits)
- Working tree: clean

## Regression (full gate)
Command: `uv run python scripts/quality.py`

| Check | Result |
|---|---|
| ruff check . | PASS |
| ruff format --check . | PASS |
| pyright (strict) | 0 errors |
| pytest -q | 747 passed, 1 skipped (EXTERNAL_BLOCKED: live PostgreSQL) |
| architecture_check.py | Architecture conformance: PASS |

Additional:
- Mutation path: commit_paths = 1 (single authority unchanged).
- Replay: golden v5.1 hash unchanged; multi-instance replay independent (tested).
- Migration: head 0003 (lineage tables); old-DB upgrade keeps replay hash;
  downgrade 0003->0002 removes lineage tables (tested).
- Lineage: fixture + visualization generated; parent not modified by
  child/promotion (tested).

## Acceptance matrix (M28)
| Item | Status |
|---|---|
| World Definition read-only versioned; Instance refs | PASS |
| Branch == worldline fork (no second history object) | PASS |
| Lineage DAG (nodes/edges, cycle rejection, ancestor/descendant queries) | PASS |
| Lineage persistence (minimal tables, migration 0003, branch reuse) | PASS |
| Hypervisor multi-instance isolation + budgets/profiles | PASS |
| Interworld presence (explicit policies, no implicit write-back) | PASS |
| Hybrid Genesis compatibility analysis / safe rejection | PASS |
| Lineage API/SDK/Studio (GET-only, OpenAPI-regenerated) | PASS |
| No second kernel / branch / event system | PASS |
| Old replay + migration compatibility | PASS |

## Performance/complexity change
- LOC 22,962 (M27) -> 23,853 (M28) = +891 LOC across 8 lineage Goals
  (identity model, graph, repository+migration, hypervisor, presence,
  hybrid genesis, API/Studio, fixture tooling + tests).
- API routes 10 -> 13 (3 GET-only lineage endpoints).
- registries 10 -> 11 (PresenceRegistry); no new engine/god object.

## Blockers
- None internal. External unchanged: live PostgreSQL; real Red Chamber source
  (M32); real providers/renderers/sensors.

## Known limitations
- LineageRepository persists nodes/edges; branch lineage is derived on demand
  from the branches table (by design, no duplication).
- Hybrid Genesis produces candidate/rejection only; merge execution is a later
  Goal (M30 promotion).

## Next Milestone prerequisites
- M29 (G32A..G32H): Evolution Policy Stack / multi-scale co-evolution ? start
  G32A after M28 gate PASS, no user confirmation required.
