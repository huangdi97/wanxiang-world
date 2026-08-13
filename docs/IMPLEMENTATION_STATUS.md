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

## M3 ? Bounded Agents Can Live Inside the World (PASS, 2026-08-13)

## M4 ? Worlds Can Be Authored, Reviewed, Installed and Instantiated (in progress)

- G04A Package, Schema & Dependency Registry ? PASS (2026-08-13): portable manifests, semantic constraints, deterministic resolver, content hashes, default-deny executable trust, manifest migration; 275 tests green.

- G03A Observation & Perspective Isolation ? PASS (2026-08-13): observations
  derived from events + spatial/acoustic/rights; sealed payload content never
  leaks; private/group visibility; 220 tests green.

- G03B Belief, Memory & Temporal Epistemic Graph ? PASS (2026-08-13): actor-local
  beliefs/memories with corrections (lineage), contradictions, forgetting and
  bounded compaction; actor-scoped access; 228 tests green.

- G03C Actor & Organization Runtime ? PASS (2026-08-13): propose-only policies,
  order lifecycle with typed transitions, actor states, organization views;
  236 tests green.

- G03D Action, Affordance & Validator ? PASS (2026-08-13): versioned action
  registry + side-effect-free validator (schema/actor/permission/reachability/
  epistemic/resources); affordances; 244 tests green.

- G03F Skill Runtime ? PASS (2026-08-13): versioned skills (definition/step/instance), registry with reference skills, SkillRuntime executing every step through the authoritative path, permission gate at start, failure marks instance failed; 255 tests green.

- G03G Capability & Learning ? PASS (2026-08-13): bounded capability (level 0..10, mastery/confidence 0..1), practice/assessment evidence records, deterministic clamped LearningPolicy, capability resolvers through Commit Authority, skill step capability gates; 265 tests green.

## M3 ? Bounded Agents Can Live Inside the World (PASS, 2026-08-13)

## M4 ? Worlds Can Be Authored, Reviewed, Installed and Instantiated (in progress)

- G04A Package, Schema & Dependency Registry ? PASS (2026-08-13): portable manifests, semantic constraints, deterministic resolver, content hashes, default-deny executable trust, manifest migration; 275 tests green.

- G03E Resolver, Adjudication & Deterministic Policies ? PASS (2026-08-13):
  adjudicator registry by (action, version), seeded RNG, provenance +
  uncertainty, version pinning; delta dry-run before commit; 250 tests green.
