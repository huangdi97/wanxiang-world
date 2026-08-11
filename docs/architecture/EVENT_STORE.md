# Event Store, Ordering, Idempotency & Concurrency (GOAL_01C)

Ownership: `wanxiang_runtime.ports` (contract + in-memory adapter); durable
adapters implement the same contract (GOAL_01E).

## Contract (`EventStore`)

- `append(event)` ? append-only; enforces per-branch strict event-sequence
  ordering (must equal last+1), unique event ids, and command-id idempotency.
- `load(instance, branch, from_seq=, to_seq=)` ? ordered range load.
- `last_event_seq(instance, branch)` ? authoritative per-branch head.
- `command_result_event(command_id)` / `has_command(command_id)` ? idempotent
  retry support (return prior result).
- `integrity_check(instance, branch)` ? raises `CorruptEventStream` on gaps,
  duplicate seqs or duplicate event ids.

## Semantics

- **Ordering is by `event_seq`, never wall-clock.** Commit timestamps are audit
  fields and never determine canonical order.
- **Append-only**: no event rewrite; corrections are new events/branches.
- **Optimistic concurrency**: Commit Authority compares `expected_revision`
  against the event store head (`last_event_seq`); a stale writer raises
  `StaleRevision` and loses. The event store additionally rejects out-of-order
  appends as a second line of defense.
- **Idempotency**: a command_id is committed at most once. The store rejects a
  second append with `DuplicateCommandConflict`; application/API layers return
  the prior result via `command_result_event`.
- **Atomicity**: `fail_append` injection proves no partial append on failure.

## Adapters

- `InMemoryEventStore`: deterministic, contract-tested, used by unit tests.
- SQLite adapter registered against the same contract suite in GOAL_01E.
- PostgreSQL compatibility assumed; SQL remains PG-compatible.

## Contract test suite

`tests/contract/test_event_store_contract.py` runs the same suite against every
adapter so ordering/idempotency/integrity semantics cannot drift between
implementations.
