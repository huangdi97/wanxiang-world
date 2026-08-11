# GOAL 01B — Commit Authority & Core Invariants

## Objective

Implement the only authoritative mutation pathway for the initial kernel: accept validated/resolved proposals, enforce commit preconditions/invariants, apply canonical deltas, produce committed events/audit metadata and expose deterministic results without depending on web/database/LLM frameworks.

## Scope

- Commit Authority service/use case;
- initial invariant framework;
- pure delta application;
- commit result contract;
- validation/resolution seam for deterministic micro-world;
- structured audit/trace metadata;
- in-memory adapters acceptable for unit-level execution, with persistence supplied later.

## Non-goals

- no full Action Validator from G03D;
- no domain-specific physics/social rules;
- no multiplayer queue;
- no SQL persistence requirement in this Goal;
- no LLM.

## Required reading

Master spec Canonical State Kernel, World Reality Bus, standard runtime loop, core invariants.

## Architecture constraints

- mutation cannot occur outside Commit Authority public path;
- commit inputs include expected branch revision where required;
- apply operation deterministic;
- rejected proposal cannot partially mutate state;
- audit/trace data is emitted separately from domain state where appropriate.

## Deliverables

- Commit Authority implementation;
- invariant registry/composition mechanism kept simple;
- deterministic minimal resolver/proposal test support;
- typed commit result/errors;
- tests for success/rejection/atomicity semantics.

## Implementation tasks

1. Implement read-only canonical state input and pure delta application semantics.
2. Add minimum invariants needed for P1: entity existence/reference integrity as applicable, revision monotonicity, duplicate identity prevention, branch identity matching, schema compatibility.
3. Implement expected-revision precondition.
4. Keep resolution separate from commit: Commit Authority does not invent outcomes.
5. Produce committed event candidate/record through an event append port; if event store final implementation is next Goal, define the port now.
6. Guarantee state/event atomicity at the abstraction contract; in-memory implementation must model all-or-nothing behavior.
7. Add structured audit trace fields.
8. Add tests that attempt direct illegal update through exposed APIs and confirm no such public mutation path exists.
9. Add tests for proposal validation rejection preserving state hash.
10. Add deterministic successful commit test.

## Tests

- valid commit;
- invalid proposal/no mutation;
- wrong instance/branch;
- stale revision;
- duplicate entity/reference violation where supported;
- transaction/port failure leaves canonical state unchanged in the tested adapter;
- deterministic result hash.

## Acceptance criteria

- exactly one logical production mutation path exists for canonical P1 state;
- stale revision is a typed conflict;
- failed commit does not advance revision or state;
- committed result has event/audit identity;
- no transport/ORM/model dependency leaks into domain/runtime core;
- full quality suite green.

## Failure / blocker handling

Any need to bypass Commit Authority is an architecture defect, not a shortcut. Refactor instead.

## Documentation updates

- `docs/architecture/COMMIT_AUTHORITY.md`;
- core runtime sequence diagram;
- goal report/acceptance matrix.

## Git / checkpoint requirements

`goal 01B: implement canonical commit authority`
