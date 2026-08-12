# Goal G02B Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: 8c0c7cf (G02A checkpoint)
- working-tree notes: clean

## Objective
Implement monotonic world time, calendars, schedules and recurring temporal
constraints independent of wall-clock time.

## Delivered
- `wanxiang_substrate.temporal`: model (WorldClock, Calendar, Appointment,
  Deadline, RecurringEvent, TimeWindowConstraint), errors, versioned components,
  TemporalQuery (read-only), resolvers (advance/advance_to/schedule/deadline/
  recurring/mark_done/instantiate), calendar fixture (day boundaries, recurring
  duty, deadline, appointment).
- No new persisted schema (temporal rides on versioned components).

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run pytest -q` | 168 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests:
- unit: monotonic clock, calendar day cycle, appointment/window validation,
  recurrence bounded expansion;
- integration: monotonic advance; backward advance structured failure;
  schedule + conflict + window violation; deadline becomes due; replay
  deterministic; due events remain due exactly once after persistence restart;
- property: committed world time never decreases.

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | placeholder guard |
| Goal + regression tests PASS | PASS | 168 tests incl. M1 + G02A |
| Lint/type/architecture PASS | PASS | quality gate |
| Schema change has migration test | NOT_APPLICABLE | no schema change; M1 replay + restart tests |
| Mutations flow through Validate/Resolve/Commit | PASS | resolvers -> CommitAuthority |
| No domain/core dependency on FastAPI/SQLAlchemy/UI/LLM | PASS | guard |

## Key decisions
- World clock advanced only by commands; backward = BackwardTimeError (ADR-0012).

## Known limitations
- Autonomous population scheduler is G02F; this Goal provides the primitives.

## External blockers
None.

## Final checkpoint
- commit: `goal g02b: temporal system & schedules`
