# Goal 01C Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: 6b21b9e (goal 01B checkpoint)
- working-tree notes: clean

## Objective
Implement the durable event-stream abstraction and a real local adapter with
explicit ordering, branch revisions, idempotent command semantics and
optimistic concurrency behavior required by replay/host/multiplayer features.

## Delivered
- `wanxiang_runtime.ports`: `EventStore` protocol (append/load/last_event_seq/
  command_result_event/has_command/integrity_check) + `InMemoryEventStore`
  adapter with strict ordering, idempotency, integrity checks and failure
  injection.
- Commit Authority now derives the current branch revision from the event store
  head (optimistic concurrency): stale writers raise `StaleRevision`.
- Reusable contract suite `tests/contract/test_event_store_contract.py`
  (in-memory adapter registered now; SQLite adapter added in GOAL_01E).
- `docs/architecture/EVENT_STORE.md`.

## Key architecture decisions
- Event store head is the concurrency authority; caller-supplied state must
  match `expected_revision`.
- event_seq (not wall clock) defines canonical ordering.
- Idempotency enforced at the store (duplicate append rejected) and retrievable
  via command_result_event for API/application retry semantics.

## Test evidence
| Check | Command | Result | Evidence path |
|---|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS | |
| Pyright strict | `uv run pyright` | PASS (0 errors) | |
| Pytest | `uv run pytest -q` | 75 passed | tests/contract, tests/unit/event_store |
| Architecture | `uv run python scripts/architecture_check.py` | PASS | |
| Full gate | `uv run python scripts/quality.py` | PASS | |

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Stream ordering independent of wall-clock | PASS | contract test |
| Duplicate command cannot duplicate effect | PASS | store rejects; prior result retrievable |
| Stale writer loses with explicit conflict | PASS | StaleRevision from store head |
| Contract tests reusable | PASS | parameterized suite |
| No event silently overwritten | PASS | append-only; integrity_check |
| Real persistence path planned; M1 dependency explicit | PASS | SQLite adapter in 01E; contract suite ready |

## Migrations / compatibility
- Serialization unchanged (schema v1); SQLite tables introduced in GOAL_01E.

## Security / rights impact
- No secrets; no rights changes.

## Known limitations
- Durable SQLite adapter and migrations are GOAL_01E (real persistence path
  exists by M1).

## External blockers
None.

## Final checkpoint
- commit: `goal 01C: implement ordered event store semantics`
