# Goal 01B Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: e34c74e (goal 01A checkpoint)
- working-tree notes: clean

## Objective
Implement the only authoritative mutation pathway: accept validated/resolved
proposals, enforce commit preconditions/invariants, apply canonical deltas,
produce committed events/audit metadata and expose deterministic results
without web/database/LLM framework dependencies.

## Delivered
- `wanxiang_runtime.state`: immutable InMemoryCanonicalState + pure
  `apply`/`apply_delta` (no public mutator).
- `wanxiang_runtime.invariants`: initial invariant registry
  (duplicate entity/relation, reference integrity, delete existence).
- `wanxiang_runtime.authority`: CommitAuthority with preconditions (branch/
  instance match, expected revision -> StaleRevision, rule version ->
  IncompatibleVersion), empty-delta rejection, event append, revision advance,
  CommitResult.
- `wanxiang_runtime.ports`: EventAppendPort protocol + InMemoryEventAppendLog
  (with failure injection).
- `wanxiang_runtime.audit`: AuditRecord (trace/event identity).
- `wanxiang_runtime.resolver`: ResolverRegistry (deterministic resolution seam).
- Domain refinement: ComponentData gains explicit component_id (identity typed).
- `docs/architecture/COMMIT_AUTHORITY.md`.

## Key architecture decisions
- apply_delta is a pure method on the state; authority advances revision and
  appends the event (append port = commit point).
- Event seq is derived from the append port's last_event_seq (authoritative).
- Invariant violations: duplicates -> Conflict; missing references -> ValidationRejected.

## Test evidence
| Check | Command | Result | Evidence path |
|---|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS | |
| Pyright strict | `uv run pyright` | PASS (0 errors) | |
| Pytest | `uv run pytest -q` | 63 passed | tests/unit/runtime, tests/unit/domain |
| Architecture | `uv run python scripts/architecture_check.py` | PASS | |
| Full gate | `uv run python scripts/quality.py` | PASS | |

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Exactly one logical production mutation path | PASS | only CommitAuthority.commit; no state mutator |
| Stale revision is typed conflict | PASS | StaleRevision raised; test |
| Failed commit does not advance revision/state | PASS | stale/conflict/failure tests |
| Committed result has event/audit identity | PASS | result.event/result.audit assertions |
| No transport/ORM/model dependency leaks into domain/runtime core | PASS | architecture guard |
| Full quality suite green | PASS | quality.py |

## Migrations / compatibility
- ComponentData serialization now includes component_id (schema v1 still; field
  added, decode validates presence). No persisted DB yet.

## Security / rights impact
- Audit/trace emitted separately; no secrets involved.

## Known limitations
- In-memory adapters only (durable persistence is GOAL_01C/01E).
- Command-level idempotency (duplicate command) delegated to event store (01C).

## External blockers
None.

## Final checkpoint
- commit: `goal 01B: implement canonical commit authority`
