# Changelog ? Wanxiang Engineering Program

## 2026-08-11 ? Batch initialization

- Repository initialized (`git init`, branch `main`).
- Pre-implementation audit written (`reports/PRE_IMPLEMENTATION_AUDIT.md`).
- Ledgers created: PLAN, STATUS, DECISIONS, BLOCKERS, KNOWN_FAILURES, CHANGELOG, AGENTS.
- Batch scope: GOAL_00A .. GOAL_01F + M1 qualification. Stop after M1 PASS.

## 2026-08-11 ? GOAL_00A PASS

- uv workspace + 7 Python packages (src layout, py.typed), strict ruff/pyright/pytest config.
- `packages/observability`: settings loading, secret redaction, structured logging.
- TypeScript baseline (`packages/sdk_ts`) with strict tsconfig, ESLint, Vitest; all gates green.
- `scripts/quality.py` stable quality gate; CI workflow; docker-compose baseline.
- Ledgers/ADR structure/runbook created; ADR-0001 accepted.
- Checkpoint: `goal 00A: establish reproducible engineering foundation`.

## 2026-08-12 ? GOAL_00B PASS (M0 PASS)

- `scripts/architecture_check.py`: forbidden imports, import cycles, file-size,
  secret and placeholder guards; integrated into `scripts/quality.py`.
- `docs/architecture/MODULE_BOUNDARIES.md`, `reports/ACCEPTANCE_MATRIX.md` created.
- Architecture guard negative tests (17 tests total green).
- Reports: `reports/goal_00B_report.md`, `reports/M0_ENGINEERING_BASE_ACCEPTANCE.md`.
- Milestone tag `m0-engineering-base` created at M0 PASS.

## 2026-08-12 ? GOAL_01A PASS

- `packages/domain` core contracts: ids, versions, time, errors, hierarchy,
  entity, command, delta, event, hashing, state, snapshot, run, evidence, rights.
- Versioned serialization (command/delta + history contracts) with schema-version
  rejection; semantic hashing excluding wall-clock/audit fields.
- `docs/architecture/CORE_CONTRACTS.md`; ADR-0003.
- 48 tests green (unit + property).

## 2026-08-12 ? GOAL_01B PASS

- Commit Authority with preconditions, immutable canonical state, pure
  apply_delta, invariant registry, append-port atomicity, audit records.
- EventAppendPort + in-memory adapter (failure injection); ResolverRegistry seam.
- ComponentData gains component_id; ADRs 0004-0005.
- 63 tests green; docs/architecture/COMMIT_AUTHORITY.md.

## 2026-08-12 ? GOAL_01C PASS

- EventStore contract (append/load/idempotency/integrity) + InMemoryEventStore.
- Optimistic concurrency via store head; stale writers raise StaleRevision.
- Reusable contract suite (in-memory now; SQLite adapter in 01E).
- 75 tests green; docs/architecture/EVENT_STORE.md; ADR-0006.

## 2026-08-12 ? GOAL_01D PASS

- ReplayEngine (fork-aware, contiguous seq, version checks), SnapshotStore +
  in-memory adapter, branch fork/repository, state diff.
- Commit Authority branch_base_revision; golden replay fixture v1 committed.
- 93 tests green; docs/architecture/REPLAY_BRANCHING.md; ADR-0007.

## 2026-08-12 ? GOAL_01E PASS

- SQLAlchemy adapters (event store, snapshot store, branch/instance/audit repos).
- Alembic migrations 0001_initial + 0002_add_event_seq_index; migration tests.
- SqlAlchemyEventStore in shared contract suite; durable replay == golden hash.
- 111 tests green; docs/architecture/PERSISTENCE.md; ADR-0008.

## 2026-08-13 ? G02D PASS (M2 phase)

- `wanxiang_substrate.body`: bounded condition facets, mobility/fatigue
  capability, visibility/privacy, deterministic exert/rest transitions.
- Spatial move rejects fatigued/immobile actors (BodyConstraintViolation).
- 192 tests green; ADR-0014; docs/architecture/BODY_SUBSTRATE.md;
  reports/g02d_report.md; checkpoint `goal g02d: body & condition constraints`.

## 2026-08-13 ? G02C PASS (M2 phase)

- `wanxiang_substrate.material`: items/containers/custody/ownership/info
  payloads on versioned components; transfer/move/consume/damage/seal/read
  resolvers through M1 authority; sealed-letter epistemic separation.
- Containment cycle prevention, capacity, custody conservation; no new migration.
- 182 tests green; ADR-0013; docs/architecture/MATERIAL_SUBSTRATE.md;
  reports/g02c_report.md; checkpoint `goal g02c: material, container, custody
  & information payload`.

## 2026-08-13 ? G02B PASS (M2 phase)

- `wanxiang_substrate.temporal`: WorldClock (command-advanced, monotonic),
  Calendar, Appointment/Deadline/RecurringEvent with deterministic bounded
  recurrence, TemporalQuery, resolvers, calendar fixture.
- Backward advance -> BackwardTimeError; schedule conflicts -> ScheduleConflict;
  window violations -> TimeWindowViolation; restart keeps due events exactly once.
- 168 tests green; ADR-0012; docs/architecture/TEMPORAL_SUBSTRATE.md;
  reports/g02b_report.md; checkpoint `goal g02b: temporal system & schedules`.

## 2026-08-13 ? G02A PASS (M2 phase begins)

- `packages/substrate` spatial substrate: model, query (topology/path/capacity/
  access/zones), resolvers (move/set_portal_state/instantiate), house fixture.
- Spatial state on versioned components; no new migration; M1 replay untouched.
- 153 tests green; ADR-0011; docs/architecture/SPATIAL_SUBSTRATE.md;
  reports/g02a_report.md; checkpoint `goal g02a: spatial topology & access`.

## 2026-08-12 ? GOAL_01F PASS (M1 PASS)

- Application layer: WorldRuntime, synthetic micro-world resolvers,
  WorldEnvironment facade; FastAPI thin transport with structured errors/OpenAPI.
- M1 acceptance A1-A10 PASS on SQLite; API e2e + environment tests.
- 130 tests green; reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md; acceptance
  matrix updated; docs/IMPLEMENTATION_STATUS.md.
- Milestone tag `m1-authoritative-world` created at M1 PASS.
- Batch stop condition reached: do not begin G02A in this batch.
