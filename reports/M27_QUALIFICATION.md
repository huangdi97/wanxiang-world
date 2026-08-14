# M27 ? Reality Root / Constitution / Semantic ISA Milestone Qualification

## Status: PASS

## Preconditions (all PASS)
| Goal | Status |
|---|---|
| G30A Reality Root ???? | PASS (commit g30a) |
| G30B World Constitution ????? | PASS (commit g30b) |
| G30C Constitution ??????? | PASS (commit g30c) |
| G30D World Semantic ISA ???? | PASS (commit g30d) |
| G30E ISA ?????? Commit ???? | PASS (commit g30e) |
| G30F ?? World Commit ?? | PASS (commit g30f) |
| G30G Fact Scope ? Authority Partition | PASS (commit g30g) |
| G30H Event Snapshot ??????? | PASS (commit g30h) |
| G30I M27 Root Constitution ISA ???? | PASS (this gate) |

## Commit range
- From: `272fe0a` (M26 gate PASS)
- To: HEAD at M27 PASS (g30a..g30i commits)
- Working tree: clean

## Regression (full gate)
Command: `uv run python scripts/quality.py`

| Check | Result |
|---|---|
| ruff check . | PASS |
| ruff format --check . | PASS |
| pyright (strict) | 0 errors |
| pytest -q | 714 passed, 1 skipped (EXTERNAL_BLOCKED: live PostgreSQL) |
| architecture_check.py | Architecture conformance: PASS |

Additional:
- Mutation-path search: commit_paths = 1; the only event append path is
  CommitAuthority.commit -> EventAppendPort; resolution dry-run is pure.
- Old replay: golden v5.1 fixture hash `7d17aba7...` unchanged; baseline
  fixtures (combined hash f27b7724...) still reproducible.
- Migration compatibility: migration head 0002 unchanged; migration tests green.
- Code minimality: v52_minimality_budget hard_ok=True.

## Acceptance matrix (M27)
| Item | Status |
|---|---|
| Reality Root = semantic bedrock, no second kernel | PASS |
| Constitution versioned + immutable roots vs mutable law layers | PASS |
| Constitution enforcement in pre-commit invariants (kernel priority) | PASS |
| World Semantic ISA: 8 typed instructions, no parallel bus | PASS |
| ISA executes through the existing pipeline (PROMOTE = use case only) | PASS |
| Three World Commit kinds on one authority; no CapabilityCommit | PASS |
| Fact scope + authority partition; projection filtered | PASS |
| Event/Snapshot version context; legacy adapter | PASS |
| No new Commit Boundary bypass | PASS (1 commit path) |
| Old replay still PASS | PASS |

## Performance/complexity change
- LOC 21,901 (M26) -> 22,962 (M27) = +1,061 LOC across 9 semantic Goals
  (Reality Root contract, Constitution, ISA + pipeline, commit kinds,
  runtime control ledger, fact scope policy, version context + tests).
- No hot-path change: CommitAuthority gained kind validation (constant-time);
  replay/commit semantics unchanged; ports 23 -> 24 (RealityRootContract).

## Blockers
- None internal. External unchanged: live PostgreSQL; real Red Chamber source
  (M32); real providers/renderers/sensors.

## Known limitations
- RuntimeControlLedger is in-memory (persistence arrives with ledger/DB
  migrations in M31).
- VersionContext is history metadata resolved at read time; no DB column yet
  (M31 compatibility migration).

## Next Milestone prerequisites
- M28 (G31A..G31H): World Definition / Worldline / Lineage / Hypervisor ? start
  G31A after M27 gate PASS, no user confirmation required.
