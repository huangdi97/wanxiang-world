# GOAL 01F — Minimal Authoritative World Vertical Slice & M1 Qualification

## Objective

Integrate P0/P1 components into a small but real deterministic synthetic world execution path and prove Milestone M1 end-to-end. This is the first proof that Wanxiang has an authoritative replayable world kernel rather than only contracts and repositories.

## Scope

Build a tiny generic synthetic micro-world with no real literary/historical content. It only needs enough entities/components/actions to test canonical mutation semantics.

Implement minimal application/API/environment boundaries needed to exercise:
- create/instantiate synthetic World Instance;
- get canonical state/snapshot;
- submit deterministic structured command/action;
- validate minimal preconditions;
- deterministic resolve;
- ProposedWorldDelta;
- Commit Authority;
- event query;
- checkpoint;
- replay;
- branch;
- minimal branch diff;
- deterministic environment API functions needed for M1 tests.

A small FastAPI transport is allowed/expected if the repository stack is ready, but M1 must also be testable directly through application/runtime APIs. HTTP is not the authority.

## Non-goals

- no React UI;
- no Phaser;
- no LLM;
- no Living World spatial substrate beyond a trivial generic component/action used to test mutation;
- no cognition/memory;
- no Source Compiler;
- no Red Chamber/family/museum/campaign names or facts;
- no multiplayer websocket.

## Required reading

All prior Goals, M1 scenarios in Acceptance Standard, master API/world environment concepts.

## Architecture constraints

- API routes thin;
- application use cases own orchestration entry points;
- runtime owns validate/resolve/commit semantics;
- persistence behind ports;
- synthetic domain behavior clearly marked fixture/demo and not encoded as core-world-specific branching logic;
- same authoritative path used by direct application tests and HTTP tests.

## Deliverables

- deterministic synthetic micro-world fixture/package-like test data clearly marked synthetic;
- application use cases;
- minimal API endpoints or equivalent environment facade;
- M1 integration tests;
- final M1 acceptance report and matrix;
- implementation status docs.

## Implementation tasks

1. Define a generic synthetic scenario small enough to understand manually, e.g. two entities and a deterministic transferable token/resource or status update. Do not prematurely implement full item/spatial substrate.
2. Instantiate world with explicit instance/branch/revision/schema/runtime metadata.
3. Implement minimal command validator using typed contracts.
4. Implement deterministic resolver that produces ProposedWorldDelta; keep it fixture/domain-side enough not to hard-code future product domains into Core.
5. Execute through Commit Authority and durable EventStore.
6. Provide query for canonical state/event stream/snapshot metadata.
7. Provide checkpoint and replay use case.
8. Provide branch creation and child command.
9. Add duplicate command handling at the application boundary.
10. Add stale revision handling.
11. Add a minimal `WorldEnvironment` facade consistent with future `create/reset/observe/legal_actions/step/checkpoint/restore/branch/metrics/close`, implementing only the subset honestly supported now and clearly marking unsupported methods by interface scope rather than fake success. Prefer not exposing methods until implemented if the language/API design allows.
12. If FastAPI endpoints are added, generate explicit schemas and map domain errors to structured HTTP errors.
13. Add OpenAPI smoke/contract tests if API exists.
14. Run M1 A1–A10 acceptance scenarios.
15. Run full repository quality suite.
16. Inspect for files >300 lines, import cycles, duplicate schemas, broad `Any`, dead code and route business logic; refactor before final PASS.
17. Generate `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`.
18. Update `reports/ACCEPTANCE_MATRIX.md`, `docs/IMPLEMENTATION_STATUS.md`, PLAN/STATUS/etc.

## Tests

Mandatory M1 tests:
- valid commit;
- invalid command no mutation;
- duplicate command idempotency;
- stale revision conflict;
- durable event ordering;
- snapshot + remaining replay;
- full replay;
- branch isolation;
- deterministic semantic hash;
- corrupt/incompatible replay failure;
- fresh DB migration;
- persistence reload;
- architecture conformance;
- API contract/E2E if API exists.

## Acceptance criteria

M1 PASS requires all of the following:

1. No LLM/API key.
2. World instance can be created with real application/runtime/persistence code.
3. A valid deterministic command changes canonical state exactly once through Commit Authority.
4. An invalid command does not mutate state.
5. Duplicate command cannot duplicate effect.
6. Stale revision is explicitly rejected.
7. Event order is durable.
8. Snapshot + replay reconstructs same semantic hash.
9. Full baseline replay works for fixture.
10. Child branch mutation leaves parent unchanged.
11. Corrupt/incompatible stream fails explicitly.
12. SQLite durable persistence and migrations pass.
13. No required production path contains TODO/placeholder/NotImplemented/mock-only completion.
14. Architecture guards pass.
15. Ruff/format/typecheck/pytest and applicable TS/build checks pass.
16. Final acceptance evidence names commands, tests and commit.
17. Working tree is clean or only contains explicitly documented generated acceptance artifacts before final checkpoint.

## Failure / blocker handling

There should be no real external data blocker. Fix all internal failures. If an optional environment tool (Docker/PostgreSQL) is unavailable, M1 still must pass with the defined local deterministic path; document optional validation separately.

## Documentation updates

- `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`;
- `reports/ACCEPTANCE_MATRIX.md`;
- `docs/IMPLEMENTATION_STATUS.md`;
- world runtime foundation guide;
- PLAN/STATUS/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG.

## Git / checkpoint requirements

Create Goal checkpoint:

`goal 01F: qualify authoritative world milestone`

After all M1 evidence is complete, optionally create local annotated tag:

`m1-authoritative-world`

Do not push.
