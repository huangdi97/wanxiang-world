# Release Process (G16H)

## CI quality gates (blocking)
- `uv run python scripts/quality.py` (ruff, pyright, pytest, architecture) — must PASS.
- `packages/sdk_ts`: `tsc --noEmit`, `eslint`, `vitest` — must PASS.
- Migration head must equal the declared release head; schema/client drift tests must PASS.

## Release artifact
`uv run python scripts/release_build.py` -> manifest (version, git SHA, build-input hashes, migration head,
release_hash) reproducible from a clean checkout; artifact checksums in the manifest.

## Migration preflight
`scripts.release_build.preflight_migration(database_url)` blocks deployment when the DB head is not reachable
by the deployed migration chain (IncompatibleDeployment).

## Rollback / fallback policy
- Fallback = restore the previous verified backup (scripts/backup_restore.py) and replay to confirm hashes.
- Downgrade round-trip is covered by the migration suite.
- Deployment execution to external infrastructure remains user-controlled (never automatic).

## Staging promotion
A release candidate promotes to staging only after all gates PASS and the manifest is recorded; a deployment
smoke (health + replay corpus) runs before promotion to production.
