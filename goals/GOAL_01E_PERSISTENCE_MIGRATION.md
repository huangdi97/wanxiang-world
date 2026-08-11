# GOAL 01E — Persistence, Schema Migration & Recovery Foundation

## Objective

Provide a real local durable persistence implementation for M1 with SQLAlchemy 2/Alembic, clean repository ports, transactional commit compatibility, migration tests and a foundation that remains PostgreSQL-compatible without coupling higher layers to ORM models.

## Scope

Persist the P1 concepts only:
- world instance metadata needed for M1;
- branch metadata/revision;
- events;
- snapshots;
- idempotency/command records if design requires;
- minimal canonical projection/current state if chosen, explicitly rebuildable;
- audit metadata needed for M1.

## Non-goals

- full tables for spatial/body/memory/family/heritage;
- pgvector;
- graph database;
- Redis/NATS/Kafka;
- S3/object storage unless required for snapshots and justified;
- production HA.

## Required reading

Master persistence layering, database boundary, Program Architecture version/migration policy.

## Architecture constraints

- ORM confined to persistence package;
- domain/runtime access through ports;
- SQLite local tests;
- schema designed to be PostgreSQL-compatible;
- migration revision mandatory;
- canonical commit transaction all-or-nothing;
- rebuildability documented.

## Deliverables

- SQLAlchemy mappings;
- repositories/event/snapshot store adapters;
- Alembic initial migrations;
- integration tests using fresh SQLite database;
- migration fixture test;
- recovery/rebuild test;
- persistence architecture documentation.

## Implementation tasks

1. Map P1 persistence objects without leaking ORM to domain.
2. Define unique/index constraints for instance/branch/event seq/event id/command id.
3. Implement transactional append/commit semantics.
4. Ensure foreign keys/integrity are enabled in SQLite tests.
5. Create Alembic migrations from explicit model decisions, not auto-generated noise without review.
6. Test fresh database upgrade to head.
7. Create at least one previous-schema fixture or migration simulation sufficient to prove migration harness works; if this is initial revision, create a controlled pre-head fixture rather than claiming migration strategy tested with only empty DB.
8. Test persistence adapter contracts.
9. Test destroy/recreate application process/store object and reload durable world.
10. Test rebuild derived/current projection from snapshot/events.
11. Document backup/restore boundary for later G06C without implementing full production backup tooling.
12. Run SQL against PostgreSQL compatibility assumptions where feasible; record SQLite-specific limitations.

## Tests

- fresh Alembic upgrade;
- constraints/index behavior;
- duplicate event/command rejection;
- transaction rollback;
- persistence across process/store recreation;
- snapshot/event replay from DB;
- migration harness;
- full adapter contract tests.

## Acceptance criteria

- M1 works with actual SQLite persistence, not only in-memory mocks;
- no ORM types escape into domain/runtime public API;
- migrations are reproducible;
- failed transaction does not create state/event mismatch;
- durable replay passes;
- schema/version documented.

## Failure / blocker handling

Do not bypass migrations by deleting the DB in tests that are specifically intended to test upgrade compatibility.

## Documentation updates

- `docs/architecture/PERSISTENCE.md`;
- development DB commands;
- migration policy docs;
- goal report.

## Git / checkpoint requirements

`goal 01E: add durable persistence and migration foundation`
