# GOAL 01D — Snapshot, Replay, Branch & Determinism

## Objective

Make Wanxiang history operational: create/restore snapshots, replay committed event streams to canonical state, fork isolated branches, compare semantic state and verify deterministic reconstruction.

## Scope

- snapshot contract/store port;
- snapshot creation at revision;
- replay engine;
- branch ancestry and fork;
- branch isolation;
- canonical semantic hash;
- replay integrity/version checks;
- basic branch diff sufficient for M1 diagnostics.

## Non-goals

- rich Studio time-travel UI;
- distributed snapshots;
- long-world performance optimization;
- narrative canon comparison;
- full experiment runtime.

## Required reading

Master spec Event/Branch/Temporal Kernel, world Git, replay/determinism requirements.

## Architecture constraints

- snapshot is a checkpoint, not replacement for history;
- replay uses ordered committed events;
- parent history immutable from child;
- semantic hash excludes nondeterministic audit fields;
- incompatible/corrupt history fails explicitly.

## Deliverables

- ReplayEngine;
- snapshot store abstraction + local implementations as appropriate;
- branch repository/model;
- branch creation use case;
- semantic hash utility narrowly scoped to canonical state;
- deterministic golden fixture tests.

## Implementation tasks

1. Define snapshot content vs metadata and schema version.
2. Create snapshot at a known branch revision.
3. Restore state from snapshot.
4. Replay subsequent events through the same trusted delta/event application semantics; do not invent a second mutation model.
5. Support replay from initial baseline for small fixture.
6. Define and calculate canonical semantic hash deterministically.
7. Implement branch fork at valid revision/snapshot.
8. Verify child reads ancestry/baseline then receives independent child commits.
9. Implement minimal state/event diff useful for tests/reports.
10. Add corrupt/missing/incompatible event failure tests.
11. Add property tests with generated deterministic command/event sequences where feasible.
12. Create stable synthetic golden replay fixture.

## Tests

- snapshot round trip;
- replay from snapshot;
- full replay from baseline;
- final hash equality;
- child branch isolation;
- parent unchanged;
- invalid fork revision;
- corrupt event order;
- incompatible schema;
- deterministic same-seed scenario.

## Acceptance criteria

- derived current state can be discarded and rebuilt for fixture;
- replay final semantic hash equals original;
- child mutations do not affect parent;
- corrupt history is not silently accepted;
- golden fixture committed and documented;
- no alternate hidden state-update pathway used during replay.

## Failure / blocker handling

If existing persistence design prevents reconstructability, change persistence design now; do not defer to G12.

## Documentation updates

- `docs/architecture/REPLAY_BRANCHING.md`;
- golden fixture notes;
- goal report.

## Git / checkpoint requirements

`goal 01D: add replay snapshots and isolated branches`
