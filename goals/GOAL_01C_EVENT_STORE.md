# GOAL 01C — Event Store, Ordering, Idempotency & Concurrency Semantics

## Objective

Implement the durable event-stream abstraction and a real local adapter with explicit ordering, branch revisions, idempotent command semantics and optimistic concurrency behavior required by later replay/host/multiplayer features.

## Scope

- EventStore port;
- append/load stream operations;
- ordered sequence/revision;
- command-id idempotency tracking as appropriate;
- optimistic concurrency / expected revision;
- in-memory implementation for fast tests;
- SQLite implementation may begin here or be completed in 01E, but at least one real persistence integration path must exist by M1;
- transaction semantics compatible with Commit Authority.

## Non-goals

- Kafka/event broker;
- distributed consensus;
- multi-region replication;
- event streaming UI;
- multiplayer transport.

## Required reading

Program Architecture Event/Commit consistency contract and master event-sourcing principles.

## Architecture constraints

- append-only committed history;
- event sequence strictly ordered per branch;
- duplicate command retry cannot create duplicate effect;
- stale expected revision is rejected;
- no silent event rewrite;
- wall-clock commit timestamp does not determine canonical ordering.

## Deliverables

- EventStore port and adapters;
- contract test suite reusable by adapters;
- idempotency/concurrency tests;
- stream integrity checks;
- documentation.

## Implementation tasks

1. Finalize event stream key: instance + branch.
2. Define revision/event sequence initial/empty semantics.
3. Implement atomic append with expected revision.
4. Implement load from sequence/revision.
5. Implement command idempotency semantics and retrieval of prior result/event references where appropriate.
6. Ensure event IDs unique.
7. Detect out-of-order/corrupt event stream in tests.
8. Build reusable EventStore contract tests.
9. Run contract tests against in-memory adapter.
10. Run against real SQLite adapter now if available; otherwise ensure 01E completes it before M1.
11. Add failure-injection path for append/transaction error.
12. Document future PostgreSQL compatibility assumptions without adding distributed infrastructure.

## Tests

- sequential appends;
- expected revision success/failure;
- concurrent simulated writers against same revision;
- duplicate command ID;
- load ranges/order;
- corrupt sequence detection;
- adapter contract parity;
- transaction failure no partial append.

## Acceptance criteria

- stream ordering independent of wall-clock;
- duplicate command cannot duplicate committed semantic effect;
- stale writer loses with explicit conflict;
- contract tests reusable;
- no event is silently overwritten;
- real persistence path is planned/partially present and M1 dependency explicit.

## Failure / blocker handling

SQLite locking nuances are engineering issues; keep semantics deterministic and document adapter limitations. Do not replace required optimistic concurrency with last-write-wins.

## Documentation updates

- `docs/architecture/EVENT_STORE.md`;
- DECISIONS for revision semantics;
- goal report.

## Git / checkpoint requirements

`goal 01C: implement ordered event store semantics`
