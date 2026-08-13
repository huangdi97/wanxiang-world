# Goal G04A Acceptance Report

## Status
PASS

## Pre-goal state
- branch: master
- commit: caa04a3 (G03G + M3 checkpoint)
- working-tree notes: clean before G04A work

## Objective
Implement portable Domain/World/Scenario package manifests, schema versions and
deterministic dependency resolution.

## Delivered
- `wanxiang_substrate.packages`: PackageManifest/SemanticVersion/
  VersionConstraint/PackageLock, deterministic DependencyResolver (cycles,
  conflicts, missing), InMemoryPackageRegistry with content-hash verification,
  ExecutableExtensionPolicy (default-deny for untrusted), manifest schema
  migration (v1->v2) + compatibility matrix, synthetic town package graph.

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run python scripts/quality.py` (full gate) | 275 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests (`tests/integration/test_package_registry.py`, 10 tests):
- unit: version ordering + constraints (`== >= <= > < ^ *`);
- unit: town graph resolves deterministically (stable lock hash);
- unit: content hash verified on register (tamper rejected);
- negative: missing dependency fails;
- negative: cycle detected;
- negative: conflicting re-pin detected;
- negative: incompatible constraint has no satisfying version;
- security: untrusted package cannot register executable resolver;
- migration: old manifest upgrades through declared path;
- negative: newer-than-target schema rejected.

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | guard + review |
| Goal + regression tests PASS | PASS | 275 tests incl. M1/M2/M3 |
| Lint/type/architecture PASS | PASS | full quality gate |
| Schema change has migration/compat test | PASS | manifest migration test |
| Determinism of lock resolution | PASS | stable lock hash test |
| No new forbidden dependency | PASS | architecture guard |

## Key decisions
- Manifest schema migration v1->v2; default-deny executable trust; deterministic
  sorted resolution (ADR-0025).

## Known limitations
- Only in-memory registry adapter; durable registry storage arrives with G04E.

## External blockers
None.

## Final checkpoint
- commit: `goal g04a: package, schema & dependency registry`