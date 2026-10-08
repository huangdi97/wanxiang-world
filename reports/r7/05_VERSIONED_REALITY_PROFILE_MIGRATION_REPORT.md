# R7 05 — Versioned RealityProfile and Shadow-Replay Migration

Status: `IMPLEMENTED` / `VALIDATED` (unit + property level; no live PostgreSQL profile).

## 1. What was built

| Module | Responsibility |
|---|---|
| `packages/reality/src/wanxiang_reality/registry.py` | `ProfilePin`, `RealityProfileRegistry`: one pinned `RealityProfile`/`WorldProfile` version per worldline, coexistence of versions across worldlines, no silent hot swap |
| `packages/reality/src/wanxiang_reality/migration.py` | `LockedSnapshot`, `ReplayOutcome`, `ReplaySource`, `DriftReport`, `compare_replay`, `plan_migration` -> typed `migrate` / `fork` / `reject` |
| `packages/reality/src/wanxiang_reality/migration_apply.py` | `Approval`, `MigrationSink`, `MigrationArtifact`, `MigrationOutcome`, `migrate_worldline`, `dry_run_artifact` |

## 2. Invariants that the code enforces

- A worldline is never re-pinned in place: an incompatible profile change produces
  a plan, and applying it requires an explicit `Approval` plus a `MigrationSink`.
- A major `RealityProfile` upgrade follows checkpoint -> shadow replay -> compare
  -> migrate/fork. Divergence that the plan cannot explain rejects instead of
  guessing.
- Snapshot is not truth: the migration artifact records the replay outcome and the
  drift report, and a shadow replay never writes canonical state.
- No implicit canonical write exists in this path: the only mutation goes through
  the caller-supplied sink.

## 3. Evidence

```text
uv run pytest tests/unit/reality -q            -> 64 passed
uv run pytest tests/unit -q                    -> 855 passed (at the time of the R7 slice)
uv run python scripts/quality.py               -> 1605 passed, 1 skipped (PostgreSQL), architecture PASS
```

## 4. Not claimed

- No real long-history migration was run against a production-scale store; the
  replay comparison is exercised on generated fixtures.
- The API/CLI do not yet expose a migration approval surface.
