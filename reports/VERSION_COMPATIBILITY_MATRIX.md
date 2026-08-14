# Version Compatibility Matrix (G13E)

- Current schema version: 1
- Current runtime/rule version: 1

## Event schema versions

| Version | Replay behavior |
|---|---|
| 1 | supported |
| 0 | rejected with IncompatibleVersion (explicit) |
| 2 | rejected with IncompatibleVersion (explicit) |
| 99 | rejected with IncompatibleVersion (explicit) |

## Runtime/rule versions

| Version | Behavior |
|---|---|
| 1 | supported |
| 0 | rejected with IncompatibleVersion (explicit) |
| 2 | rejected with IncompatibleVersion (explicit) |
| 99 | rejected with IncompatibleVersion (explicit) |

## Database migrations

| Revision | Down revision |
|---|---|
| 0001_initial | base |
| 0002_add_event_seq_index | 0001_initial |

- Head: `0002_add_event_seq_index`

## Policy

- Package versioning: SemanticVersion pins; publishing never mutates a pinned install; incompatible package upgrades fork.
- Snapshot policy: Snapshot is an optimization/baseline; replay from events remains authoritative.
- Correction policy: Historical truth is corrected with new events/branches or explicit migration; never silent mutation.
