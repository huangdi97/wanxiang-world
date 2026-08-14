# Disaster Recovery Runbook (G16G)

## Profile
- Storage: SQLite (local deterministic/dev); PostgreSQL is the production target (live instance EXTERNAL_BLOCKED).
- RPO target: last committed event (backup at a defined cadence; recovery point = the backup manifest hash).
- RTO target: restore from backup copy into an isolated path and replay; measured per deployment after baseline.

## Backup
`uv run python scripts/backup_restore.py backup <live.db> <backup_dir>` copies the DB and writes
`backup_manifest.json` (schema version, event counts per branch, db sha256).

## Restore
`uv run python scripts/backup_restore.py restore <backup_dir> <restored.db>` verifies the integrity hash
and restores into the destination; then `uv run alembic upgrade head` (if needed) and run the replay corpus
to confirm semantic hashes.

## Game day (accidental deletion / corrupt current state)
1. Detect the failure (world cannot read / hash mismatch).
2. Restore the latest verified backup into an isolated path.
3. Replay all branches; compare semantic hashes to the recovery point.
4. Promote the restored DB to the live path only after hash verification.
No manual DB repair is required.

## Advanced PITR
True point-in-time recovery (PostgreSQL WAL / log shipping) is NOT implemented in the SQLite profile and is
named accurately as such (requires a Postgres instance + log shipping; EXTERNAL_BLOCKED).
