# Goal G13C Acceptance Report — Architecture, Dependency & Canonical-Mutation Forensics

## Status
PASS

## Objective
Independently prove the implemented repository still obeys architecture boundaries after M0-M9 growth, especially the single Commit Authority and dependency direction.

## Delivered
- `scripts/architecture_forensics.py` — AST-based audit tool: package import graph, forbidden-import scan, persistence-leakage scan, CommitAuthority call-site enumeration, direct persistence-write scan (receiver-name aware), cycle detection.
- `reports/ARCHITECTURE_FORENSICS.md` — full findings report.
- `reports/DEPENDENCY_GRAPH.md` — package-level wanxiang_* import edges.
- `reports/CANONICAL_MUTATION_PATHS.md` — the single authoritative mutation path and its enforcement.
- `reports/architecture_forensics.json` — machine-readable findings.
- `tests/architecture/test_architecture_forensics.py` — 11 tests.

## Findings (current repository)
| Check | Result |
|---|---|
| Forbidden imports | 0 |
| Persistence leakage (sqlalchemy/alembic/wanxiang_persistence outside persistence/api) | 0 |
| Direct persistence writes outside approved layers | 0 |
| Import cycles | 0 |
| CommitAuthority constructors | 1 — `packages/application/.../world_runtime.py` only |

Note: `packages/persistence/database.py:32` `session.commit()` is a SQLAlchemy transaction commit inside the approved persistence owner, not a canonical CommitAuthority call.

## Canonical mutation path (verified)
```
CommandEnvelope -> resolver/adjudication -> ProposedWorldDelta -> CommitRequest
  -> CommitAuthority.commit (preconditions -> apply_delta -> atomic append -> revision advance)
  -> CommittedEvent -> canonical state projection -> audit record
```
- Only `WorldRuntime.submit_command` constructs CommitAuthority and calls `.commit`.
- Projection service exposes only `compose` (no write API); StateReader exposes only `state_at/update/invalidate` (discardable read cache).
- The event store rejects duplicate-command retries (`DuplicateCommandConflict`), preserving idempotency.

## Tests
- `uv run pytest tests/architecture/test_architecture_forensics.py -q` -> 11 passed.
- Detector anti-tests prove the scanners catch forbidden imports, persistence writes outside owners, and import cycles (workspace-local fixtures, since the sandbox cannot write the OS temp dir).

## Evidence
- `uv run python scripts/architecture_forensics.py` -> forbidden=0 leakage=0 callsites=1 appends=0 cycles=0.

## Remaining limitations
- AST static analysis cannot prove type-level behavior; complemented by behavioral mutation-bypass/idempotency test and the existing 385-test suite.

## Final checkpoint
- commit: `g13c: architecture, dependency & canonical-mutation forensics`
