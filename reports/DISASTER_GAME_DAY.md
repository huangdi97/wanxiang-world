# Disaster Game Day (G16G)

## Scenario: accidental deletion of the live DB
| Step | Result |
|---|---|
| Backup taken before the incident | PASS (manifest + DB copy) |
| Live DB deleted | simulated |
| Restore into an isolated path | PASS (integrity hash verified) |
| Replay worlds; compare semantic hashes to recovery point | PASS (hash matches) |
| No manual DB repair | PASS |

## Scenario: restore into clean environment
| Check | Result |
|---|---|
| Restored canonical worlds match expected semantic hashes | PASS |
| Backup includes DB + event counts + schema version + integrity hash | PASS |
| Runbook executable by a fresh operator | PASS (documented in docs/DISASTER_RECOVERY_RUNBOOK.md) |

## Evidence
- `uv run pytest tests/integration/test_g16g_backup_restore.py -q` -> 3 passed.
- RPO/RTO engineering targets defined; advanced PITR named accurately (not implemented in this profile).
