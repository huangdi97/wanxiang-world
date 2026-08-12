# Wanxiang Engineering Standards

> Applies to all production code written under the Wanxiang Engineering Program Architecture.

---

## 1. Design priorities

In order:

1. correctness of world authority and invariants;
2. readability and explicit semantics;
3. testability and deterministic reproduction;
4. modifiability / upgradeability;
5. observability and diagnosability;
6. performance with measurements;
7. implementation convenience.

Do not trade higher priorities for lower ones without an ADR.

---

## 2. Layering rules

### Domain

Contains semantic identities, value objects, immutable command/event/delta contracts where appropriate, invariant definitions and domain-level error types.

Forbidden dependencies:
- FastAPI;
- SQLAlchemy ORM sessions/models;
- Alembic;
- React/Phaser concepts;
- network clients;
- LLM SDKs;
- global application container.

### Application

Contains use cases, command/query handlers and ports. It coordinates domain/runtime behavior but does not encode HTTP or DB details.

### Runtime

Contains validation, adjudication, commit orchestration, replay orchestration and later observe/schedule/remember hooks. It speaks through ports.

### Persistence

Implements repositories/event store/snapshot store. SQLAlchemy stays here. It must satisfy contract tests shared across adapters.

### Transport

FastAPI routes validate transport shape, authorize, call application use cases, map errors to responses, and return DTOs. No direct ORM mutations. No canonical rules in routers.

---

## 3. Naming

Use Wanxiang vocabulary consistently:

- `WorldInstance`, not generic `Game`;
- `BranchRevision`, not generic `version` when it means branch sequence;
- `ProposedWorldDelta` vs `CommittedEvent`;
- `CanonicalState` vs `Projection`;
- `Claim` vs `Fact`;
- `Observation` vs `Truth`;
- `RightsDecision`, not `is_allowed` scattered booleans when policy context matters.

Avoid:
- `Manager` without a narrow noun;
- `Utils` modules;
- `Common` dumping grounds;
- `DataService` covering unrelated contexts;
- `handle_everything` style functions.

---

## 4. File and module limits

Default production file target <= 300 lines.

If a file grows beyond 300 lines:
1. inspect for mixed responsibilities;
2. split by domain concern, protocol, adapter or use case;
3. if not split, record why in `DECISIONS.md`.

Generated files and schema snapshots are exempt but must be clearly generated.

No module may become a permanent catch-all for new Goals.

---

## 5. Function / class standards

- Keep functions focused and typed.
- Prefer pure functions for invariant checks and deterministic transforms.
- Separate command preparation, validation, resolution and commit.
- Constructors should establish valid objects, not perform hidden network/database I/O.
- Do not hide dependencies behind mutable singletons.
- Avoid inheritance-heavy frameworks for domain semantics; favor composition/protocols.
- A class should have one reason to change.

---

## 6. Domain type design

Represent important identifiers as dedicated types/value objects where practical instead of passing raw strings everywhere.

Examples:
- `WorldInstanceId`
- `BranchId`
- `EntityId`
- `EventId`
- `CommandId`
- `SnapshotId`
- `SchemaVersion`

Represent revisions and event sequence as explicit non-negative integers with validation.

Persisted contracts include schema version.

Avoid untyped nested dictionaries for canonical events/deltas. Flexible component payloads may exist, but identity, versioning, event ordering and relationship metadata remain typed.

---

## 7. Immutability and mutation ownership

Prefer immutable event records and command objects.

Do not expose internal mutable state collections to adapters/UI.

Only the Commit Authority pathway may transform canonical state.

Any convenience method named like `update_state`, `save_entity`, `set_location` must be reviewed for authority bypass. Persistence methods may persist already-authorized committed state; they do not decide legality.

---

## 8. Serialization

Serialization/deserialization is a compatibility boundary.

Rules:
- explicit schema version;
- deterministic/canonical ordering for hashes where relevant;
- no arbitrary Python object pickles for canonical durable storage;
- validation on deserialize;
- unknown/newer incompatible versions produce structured errors;
- migration/translation code is isolated and tested.

---

## 9. Persistence

Use ports to express required behavior.

SQLite is the default fast local implementation; SQL must remain PostgreSQL-compatible where the program specifies compatibility.

Transactions must respect commit atomicity.

Never make canonical correctness depend on ORM identity map side effects.

Derived current-state tables may improve query performance but must be rebuildable from snapshot + events according to the defined persistence strategy.

---

## 10. Event store requirements

A committed event should minimally be able to carry:

- event id;
- instance id;
- branch id;
- event sequence / resulting revision;
- world time when applicable;
- event type;
- schema version;
- payload/delta reference;
- causation id;
- correlation/trace id;
- command id when user/system command caused it;
- actor/controller where relevant;
- rule/resolver/runtime version metadata;
- committed timestamp (wall clock, separate from world time).

Avoid conflating wall-clock time and world time.

---

## 11. Concurrency and idempotency

Every mutation use case must answer:

- What branch revision was read?
- What revision is expected at commit?
- What happens on stale revision?
- Can request be retried safely?
- How is duplicate command detected?
- Is event append + state change atomic?

Do not add concurrency “later” after multiplayer; basic revision semantics are part of P1.

---

## 12. Errors

Create explicit error taxonomy. Suggested families:

```text
WanxiangError
  ContractError
  ValidationRejected
  PermissionDenied
  RightsDenied
  NotFound
  Conflict
    StaleRevision
    DuplicateCommandConflict
  IncompatibleVersion
  ReplayError
  CorruptEventStream
  PersistenceError
  ExternalDependencyError
  ExternalDataBlocked
```

Names may be refined, but callers must not need to parse error strings.

---

## 13. Logging and audit

Use structured logs.

Do not log:
- secrets;
- raw private memories by default;
- full untrusted source documents by default;
- biometric/private family content in generic debug logs.

Audit records for canonical commit are more durable/structured than ordinary debug logs.

---

## 14. Tests near code

When adding a public contract or invariant, add tests in the same Goal.

For every happy path, consider at least one failure path.

For state mutation, normally test:
- valid request;
- invalid request;
- duplicate request;
- stale revision;
- persistence failure behavior where practical;
- replay compatibility.

---

## 15. Property-based testing

Hypothesis is especially valuable for:
- event sequence monotonicity;
- branch isolation;
- state hash stability;
- identifier uniqueness;
- idempotency;
- random valid command sequences;
- serialization round trips.

Property tests are not a substitute for explicit scenario tests.

---

## 16. Architecture conformance

Implement import/dependency checks early. At minimum fail when:

- `packages/domain` imports FastAPI/SQLAlchemy/Alembic or an app module;
- core/runtime imports `apps/api`;
- plugin/domain packages import persistence internals/ORM session;
- projection code accesses persistence models directly;
- model provider accesses canonical persistence directly.

Architecture tests must be part of the normal quality command.

---

## 17. Code generation and API contracts

Once FastAPI/OpenAPI exists:
- API contract is explicit;
- TypeScript SDK/types should be generated or systematically synchronized;
- do not manually maintain parallel copies of large DTO schemas.

Breaking API changes require version/compatibility decision.

---

## 18. Upgrade / migration discipline

Any change to persisted shape must include:
- migration;
- migration test;
- rollback/restore consideration;
- old fixture compatibility;
- update to schema/version docs.

Any change to event semantics must include replay tests against pre-change event fixtures or an explicit migration/translator.

Do not “fix” an old event by rewriting fixture history silently.

---

## 19. External adapters

Every genuine external dependency has:
- port/interface;
- production adapter when in scope;
- deterministic fake/test adapter;
- error mapping;
- timeout/retry policy where relevant;
- explicit provenance/identity in traces.

Do not create fake adapters and then claim real integration acceptance passed.

---

## 20. LLM/model providers

Core CI must not require an LLM API.

Model output is a proposal/input to typed runtime contracts, never an authority mutation.

Prompts are versioned/configured in dedicated provider/prompt modules, not scattered through business logic.

Record provider/model/prompt version and token/cost/latency when model calls are introduced.

---

## 21. Security coding rules

- no secrets in repository;
- no secrets in test snapshots;
- validate untrusted paths/URIs/files;
- parameterized SQL through ORM/query builder;
- do not `eval` untrusted package/source content;
- sanitize/segregate untrusted text supplied to models;
- least-privilege tool access;
- explicit authorization before privileged debug/global-state endpoints.

---

## 22. Documentation standards

Every non-trivial subsystem should explain:
- ownership;
- public contracts;
- invariants;
- lifecycle;
- persistence/versioning;
- failure modes;
- test strategy;
- extension points.

Avoid documentation that merely copies function signatures.

Keep `PLAN`, `STATUS`, `DECISIONS`, `BLOCKERS`, `KNOWN_FAILURES`, `CHANGELOG` current.

---

## 23. Refactoring rule

Refactoring is part of normal Goal completion when new work exposes poor cohesion.

Do not defer obvious structural problems with “TODO refactor later”.

Before creating a new abstraction, search for existing responsibility and avoid duplicate concepts.

After refactoring, replay/contract tests must remain green.

---

## 24. Review checklist

Before marking a Goal complete ask:

- Is there one authoritative mutation path?
- Did any new module bypass intended dependency direction?
- Can old persisted data still be migrated/replayed?
- Are failure modes explicit?
- Are tests asserting semantics rather than implementation details?
- Did any file become a dumping ground?
- Is a world-specific name leaking into Core?
- Can the new capability be replaced/upgraded behind a stable contract?
- Is observability sufficient to explain a failure?
- Is the code understandable without reading a large prompt/history?
