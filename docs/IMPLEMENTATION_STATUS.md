# Implementation Status

## M0 ? Reproducible Engineering Base (PASS, 2026-08-12)

- uv workspace, strict ruff/pyright/pytest, TypeScript baseline, quality gate,
  ledgers/ADR structure, architecture guards.

## M1 ? Authoritative World Exists (PASS, 2026-08-12)

- Domain core contracts (`packages/domain`): ids, versions, errors, hierarchy,
  entity/relation/component, command, delta, event, hashing, snapshot, run,
  evidence/rights foundations, versioned serialization.
- Runtime (`packages/runtime`): immutable canonical state + pure apply,
  Commit Authority (preconditions, invariants, audit), EventStore contract +
  in-memory adapter, replay engine, snapshot store, branch fork/repository,
  state diff, resolver registry.
- Application (`packages/application`): WorldRuntime orchestration, synthetic
  micro-world resolvers, WorldEnvironment facade.
- Persistence (`packages/persistence`): SQLAlchemy adapters + Alembic
  migrations (0001, 0002), durable replay.
- Transport (`apps/api`): thin FastAPI routes, OpenAPI, structured errors.
- Acceptance: A1-A10 PASS; 130 tests; golden replay fixture; no LLM key.

## Next dependency

- G02A Spatial Topology & Access (do not start until M1 evidence is reviewed).

- G02B Temporal System & Schedules ? PASS (2026-08-13): monotonic world clock
  (command-advanced, backward rejected), calendars, appointments/deadlines/
  recurring duties with deterministic bounded expansion, schedule conflict +
  window constraints; restart/replay stable; 168 tests green.

- G02C Material, Container, Custody & Information Payload ? PASS (2026-08-13):
  items/containers/custody/ownership/info payloads on versioned components;
  custody != ownership and custody != knowledge; containment cycle prevention,
  capacity, explicit consume/damage; 182 tests green.

- G02D Body & Condition Constraints ? PASS (2026-08-13): bounded condition
  facets with deterministic transitions; capability check blocks otherwise-valid
  spatial movement; facet privacy; 192 tests green.

- G02E Institution, Authority, Duty & Norm ? PASS (2026-08-13): roles,
  time-scoped memberships, delegated permissions with provenance, duties and
  sanctions; restricted places require permission; expired roles cannot grant
  authority; 202 tests green.

- G02F Population Resolution & Autonomous Scheduler ? PASS (2026-08-13):
  multi-rate autonomous scheduler (focus/lightweight/duty/aggregate), budgets,
  deterministic 72h micro-town run with no user input; validated StateReader
  cache; 211 tests green.
