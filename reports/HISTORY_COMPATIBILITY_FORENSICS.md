# History Compatibility Forensics (G13E)

## Event schema

- Carrier: `CommittedEvent`
- Version field: `schema_version`
- Rule version field: `rule_version`
- Replay check: ReplayEngine._check_event raises IncompatibleVersion on schema/rule mismatch
- Commit check: CommitAuthority._enforce_preconditions raises IncompatibleVersion on rule mismatch
- Serialization: wanxiang_domain.serialization_history (versioned; expect_version)

## Snapshot schema

- Carrier: `SnapshotMetadata`
- Version field: `schema_version`
- Content: opaque reference; state rebuilt via replay

## Database

- Migrations: 0001_initial, 0002_add_event_seq_index
- Head: `0002_add_event_seq_index`
- Tables: world_instances, branches, events, snapshots, audit_traces

## Package versioning

- Exact pins + schema_pins; incompatible upgrade forks; vN never mutates vN-1 installs.

## Correction policy

- New events/branches or explicit migration semantics only; no silent overwrite of canonical history.

## Silent-defaulting audit

- No unknown-field defaulting that changes semantic meaning (serialization is explicit; unknown keys rejected by expect_version).
