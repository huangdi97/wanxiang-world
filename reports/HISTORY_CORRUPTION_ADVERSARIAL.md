# History Corruption Adversarial Qualification (G14D)

## Corruption corpus
| Corruption type | Detection | Result |
|---|---|---|
| Sequence gap / reorder | ReplayEngine CorruptEventStream + diagnose_stream `sequence_gap_or_reorder` | PASS |
| Instance/branch mismatch | ReplayEngine CorruptEventStream + `instance_branch_mismatch` | PASS |
| Revision jump | ReplayEngine CorruptEventStream + `revision_jump` | PASS |
| Unsupported schema version | IncompatibleVersion + `unsupported_schema_version` | PASS |
| Unsupported rule version | IncompatibleVersion + `unsupported_rule_version` | PASS |
| Duplicate event id | store append rejects (Conflict); replay-level uniqueness is store-enforced | PASS |
| Corrupt snapshot baseline (decodable but wrong) | restore_and_replay rejects snapshot, falls back to events, `snapshot_rejected=True` | PASS (fixed in this Goal) |
| Unreadable snapshot (structural corruption) | restore_and_replay falls back to events; never blocks recovery | PASS (fixed in this Goal) |

## Finding fixed (P1)
`restore_and_replay` used a snapshot baseline without validation: a corrupted snapshot silently produced a
wrong semantic hash (silent semantic drift). Now:
- the snapshot is validated by replaying events up to its event_seq and comparing the semantic hash;
- schema/rule version mismatches reject the snapshot;
- decode/persistence failures during snapshot load fall back to events;
- the fallback is observable via `RestoreResult.snapshot_rejected` / `used_snapshot=False`.

## Tooling
- `scripts/history_diagnostics.py::diagnose_stream` — read-only scan reporting the affected event index and
  precise corruption kind for operators.

## Operator remediation flow
1. Run `diagnose_stream` over the affected stream to identify the corruption and the instance/branch/revision.
2. Restore from authoritative event history (no manual DB mutation; snapshot is discardable).
3. If a repair tool is added later, it must create auditable new artifacts/events, never silent mutation.

## Evidence
- `uv run pytest tests/integration/test_g14d_corruption.py -q` -> 7 passed.
- Valid history remains replayable to the same hash after a read-only diagnostic scan.
- Existing snapshot/replay/restore regression: 23 passed.
