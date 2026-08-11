# Persistence, Migration & Recovery Foundation (GOAL_01E)

Ownership: `packages/persistence` (SQLAlchemy confined here). Domain/runtime
layers access state through ports; ORM types never escape.

## Layout

| Layer | Responsibility |
|---|---|
| `models.py` | ORM records: world_instances, branches, events, snapshots, audit_traces |
| `database.py` | engine/session factory; SQLite foreign-key pragma |
| `event_store.py` | `SqlAlchemyEventStore` implementing the runtime `EventStore` contract |
| `snapshot_store.py` | `SqlAlchemySnapshotStore` (state serialized via `state_codec`) |
| `branch_repository.py` | `SqlAlchemyBranchRepository` |
| `instance_repository.py` | world instance metadata |
| `audit_repository.py` | durable audit traces |
| `state_codec.py` | canonical state <-> primitive JSON |

## Schema notes (PostgreSQL-compatible)

- Text primary keys for ids; integer counters for event_seq/revision/world_time.
- Unique constraints: events.command_id; events (instance_id, branch_id, event_seq).
- `delta_json`/`state_json` are JSON-as-text (JSONB later); no SQLite-only types.
- Foreign keys enforced in SQLite via `PRAGMA foreign_keys=ON`.

## Migrations (Alembic)

- `0001_initial` ? core P1 tables.
- `0002_add_event_seq_index` ? ordered stream index (migration harness proven by
  upgrading a 0001 fixture with data to head).
- `alembic upgrade head` from fresh DB; downgrade round-trip tested.
- Runtime URL from `WANXIANG_DATABASE_URL` (default `sqlite:///./data/wanxiang.db`).

## Recovery / rebuild

- Canonical current state is rebuildable: snapshot (state_json) + remaining
  events (delta_json) replay to the same semantic hash.
- Durable replay across store recreation is integration-tested.
- Transaction atomicity: append is all-or-nothing; duplicate/out-of-order
  appends fail explicitly without partial rows.

## Backup/restore boundary

Full production backup tooling is G06C. This Goal establishes that every
durable artifact is reconstructable from committed events + snapshots, so a
restore = copy of the DB + replay verification.
