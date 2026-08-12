# Wanxiang Acceptance, Testing and Evidence Standard

---

## 1. Principle

A Goal is not complete because code exists. It is complete when behavior is reproducibly demonstrated by tests and evidence.

Acceptance evidence must let a future Codex session or human reviewer answer:
- what was required;
- what changed;
- which command proved it;
- what output/result was obtained;
- what remains external;
- which commit contains the accepted state.

---

## 2. Required test classes

Each Goal declares applicability for:

- Unit
- Property
- Contract
- Integration
- Migration
- Replay/Determinism
- Architecture
- Security/Rights
- API/E2E
- Performance/Soak

`N/A` requires a short reason.

---

## 3. Mandatory quality commands

Exact commands may be adapted to repository tooling, but equivalent checks are mandatory.

Python baseline:

```text
ruff check .
ruff format --check .
pyright
pytest -q
```

Frontend when present:

```text
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

E2E when present:

```text
pnpm e2e
```

Migration checks when DB schema exists:

```text
alembic upgrade head
# fresh database + upgrade
# supported migration-from-previous-fixture test
```

No quality check may be disabled merely to finish a Goal.

---

## 4. M1 canonical acceptance scenarios

### A1 — Valid commit

Given a new synthetic world instance at branch revision 0,
when a deterministic valid command is submitted,
then it is validated/resolved,
a ProposedWorldDelta is produced,
Commit Authority commits exactly once,
branch revision advances,
a committed event is persisted,
and canonical state reflects the effect.

### A2 — Invalid command does not mutate

Given the same world,
when validation rejects a command,
then no event representing a successful state change exists,
revision does not advance for a canonical change,
and state hash is unchanged.

### A3 — Duplicate command idempotency

Submit command ID X twice.
The second attempt must not duplicate world effects or create a second equivalent committed mutation.

### A4 — Stale revision

Prepare command against revision N.
Advance branch to N+1 through another valid commit.
Attempt stale command.
It must return structured conflict/rejection and not overwrite N+1 state.

### A5 — Snapshot and replay

Commit a deterministic sequence of N actions.
Create snapshot at an intermediate revision.
Delete/rebuild derived current state.
Replay snapshot + remaining events.
Final canonical hash and semantically relevant state must equal the original final state.

### A6 — Full replay from initial baseline

For a small stream, rebuild from initial baseline + all events and compare final hash.

### A7 — Branch isolation

Fork child branch at revision K.
Commit events to child.
Parent branch event stream/state hash remains unchanged.
Child reports correct ancestry.

### A8 — Deterministic seed/version

Run the same deterministic scenario twice with same inputs/seed/runtime rule version.
Committed event semantic results and final canonical hash must match, excluding explicitly non-semantic wall-clock/audit fields.

### A9 — Corrupt stream detection

Alter/introduce invalid ordering or incompatible event fixture in a test context.
Replay must fail explicitly rather than silently produce state.

### A10 — Migration compatibility

Create data/events under a prior supported schema fixture.
Apply migrations/translators.
Replay/queries still produce the expected semantic result.

---

## 5. Architecture acceptance

At M0/M1, tests must prove forbidden imports are detected.

At least one test fixture or analyzer rule should demonstrate each critical boundary.

Example forbidden relationships:

```text
domain -> fastapi
domain -> sqlalchemy
runtime -> apps.api
projection -> sqlalchemy ORM internals
plugin/domain pack -> ORM session
model provider -> canonical repository mutation
```

---

## 6. Evidence report format

Every Goal writes `reports/goal_<id>_report.md`:

```markdown
# Goal <id> Acceptance Report

## Status
PASS | EXTERNAL_BLOCKED | FAIL

## Pre-goal state
- branch:
- commit:
- working-tree notes:

## Objective
...

## Delivered
...

## Key architecture decisions
- ADR links

## Test evidence
| Check | Command | Result | Evidence path |
|---|---|---|---|

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|

## Migrations / compatibility
...

## Security / rights impact
...

## Known limitations
...

## External blockers
...

## Final checkpoint
- commit:
- files changed summary:
```

No Goal report may say merely “all tests pass” without naming the relevant commands/suites.

---

## 7. Acceptance matrix

Maintain `reports/ACCEPTANCE_MATRIX.md` throughout the program, not only at G12.

Columns:

```text
Requirement ID
Source section
Owning Goal
Test/evidence
Current status
Last verified commit
Notes
```

This prevents requirements from disappearing between Goals.

---

## 8. Test fixture policy

Synthetic fixtures:
- must be explicitly named synthetic;
- must not use invented real historical/museum/family claims while implying authenticity;
- may use generic people/places/items to test runtime behavior;
- should be small enough to understand manually;
- should be stable/versioned for replay regression.

Golden fixtures are changed only when semantics intentionally change and the report explains why.

---

## 9. No mock-only acceptance

Mocks/fakes are legitimate for unit/contract tests, but a Goal that promises real internal behavior must include at least one integration path using the real implementation of that behavior.

Examples:
- persistence Goal must run against real SQLite adapter, not only mock repository;
- event store Goal must actually append/load/sequence events;
- migration Goal must actually upgrade a database fixture;
- API Goal must call application runtime, not return static JSON.

External integrations may remain fake only when the Goal explicitly scopes the real connector out or is externally blocked.

---

## 10. Failure injection

Where practical, tests should inject:
- persistence transaction failure;
- corrupted serialized payload;
- duplicate command;
- stale branch revision;
- incompatible schema;
- unavailable optional adapter.

System must fail explicitly and preserve canonical integrity.

---

## 11. Performance evidence

Early phases establish baselines rather than hard optimization targets.

Report:
- event append/replay duration for synthetic fixture;
- snapshot size/count;
- test runtime;
- later: tick latency, queue lag, model calls/cost.

A performance change must not weaken correctness/replay guarantees without an ADR.

---

## 12. Milestone M1 final evidence bundle

Before starting G02A, produce:

- `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`
- `reports/ACCEPTANCE_MATRIX.md`
- deterministic scenario fixture
- replay golden hash/summary
- branch isolation evidence
- duplicate/stale command evidence
- fresh DB migration evidence
- architecture conformance evidence
- full lint/typecheck/test output paths or captured summaries
- current commit hash

Status must be PASS. External LLM/data absence is irrelevant to M1 and cannot justify skipping M1 tests.
