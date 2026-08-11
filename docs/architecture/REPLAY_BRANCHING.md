# Snapshot, Replay, Branch & Determinism (GOAL_01D)

Ownership: `wanxiang_runtime` (replay, snapshot, branch, diff).

## Replay engine

`ReplayEngine.replay(events, baseline=None)` rebuilds canonical state by
applying each committed event's delta through the same pure
`InMemoryCanonicalState.apply` path used by Commit Authority. It never invents a
second mutation model.

Integrity/version checks (explicit failure, never silent):
- event_seq must be contiguous (1..N per own stream);
- event revision must equal `baseline.revision + event_seq` (fork-aware);
- event instance/branch must match the stream;
- event schema_version and rule_version must equal the replay engine's.

## Snapshot

- Snapshot is a checkpoint/baseline, never a replacement for event history.
- `create_snapshot_metadata` + `SnapshotStore` (save/load/latest).
- Rebuild = snapshot state (revision K) + remaining events (seq K+1..N).

## Branch

- `BranchMetadata` carries explicit `BranchAncestry` (parent, fork revision,
  fork event seq, snapshot ref).
- Child branches commit to their own event stream; parent history is immutable.
- Child canonical revision = fork_revision + own event count. Commit Authority
  is constructed with `branch_base_revision` so optimistic concurrency and
  event revisions stay fork-aware.

## Determinism

- Canonical semantic hash is SHA-256 over sorted canonical fields
  (entities/relations/revision), excluding wall-clock/audit fields.
- Golden fixture `tests/fixtures/golden_replay_v1.json` pins the expected final
  hash for a 5-event synthetic scenario; regeneration via
  `scripts/generate_golden_fixture.py` (changes require documented rationale).
- Property tests: replay-from-snapshot equals full replay for generated
  command sequences.

## Diff

`diff_states` reports added/removed/updated entities and relations for M1
branch diagnostics.
