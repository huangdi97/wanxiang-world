# Backup, Restore & Migration Qualification (G12B)

`tests/integration/test_g12b_backup.py` copies a SQLite world file, restores it
into a clean runtime, replays to the identical canonical hash, and migrates the
backup through the declared Alembic path with forward/rollback policy intact.