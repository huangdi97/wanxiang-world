# Clean-room Build, Install, Upgrade, Restore & Replay Certification (G20B)

Environment: Windows/PowerShell; repository `E:\AI\wanxiang`; scratch `tests/_arch_tmp/cleanroom`.
No hidden local path dependency: every step runs from repository artifacts and
documented scripts (`release_build`, `backup_restore`, `wxpack`,`reference_world_conformance`, alembic).

## Results

| Step | Result | Evidence |
|---|---|---|
| clean_tree | PASS | tracked modifications=0; caches=[]; documented out-of-scope docs=92 |
| release_manifest | PASS | version=0.1.0; sha==HEAD=True; reproducible=True; head=0002_add_event_seq_index |
| migration_upgrade | PASS | 0001->head: 0001_initial -> 0002_add_event_seq_index |
| golden_replay | PASS | 5 events; hash match=True |
| backup_restore_replay | PASS | backup=5; restored=5; hash_match=True |
| external_sample_pack | PASS | errors=[] |
| reference_world | PASS | conformance=True; installed=True; instantiate_events=1 |

## Verdict

**PASS** - clean-room build/install/upgrade/restore/replay certified for commit 72a8c0f6085efbb2b008ad56b09017966e05836f.

## Evidence commands

```
uv run python scripts/clean_room_certify.py   # writes this report
uv run python scripts/release_build.py         # build_manifest (imported here)
uv run python scripts/traceability.py          # 44 reqs / 63 goals / 16 kernels, validation clean
uv run python scripts/quality.py               # full gate
```

## Limitations

- Live PostgreSQL (PITR/WAL) and real multi-node hosting remain EXTERNAL_BLOCKED; the
  SQLite profile backup/restore + replay are the certified deterministic path.
- Untracked V5.1 program pack documents in the working tree are out of scope for this
  certification (not developer caches; not part of the M10-M17 baseline).
