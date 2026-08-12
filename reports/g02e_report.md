# Goal G02E Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: 84568a4 (G02D checkpoint)
- working-tree notes: clean

## Objective
Implement social/institutional constraints that determine authority, duties,
permissions, obligations and sanctions.

## Delivered
- `wanxiang_substrate.institution`: model (Role, Membership, DelegatedPermission,
  Duty, PermissionDecision), errors, versioned components, InstitutionQuery,
  resolvers (define_role/grant_role/grant_permission/assign_duty/complete_duty/
  apply_sanction/instantiate), club fixture (restricted study, member role,
  delegated duty).
- Spatial move now requires `enter.<place>` permission for restricted places
  (`PermissionDeniedByInstitution` with rule references).

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run pytest -q` | 202 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests:
- unit: role grants, membership/delegation time scope, duty validation;
- integration: authorized actor enters restricted room; unauthorized rejected
  with rule reference; permission decision provenance; duty lifecycle (due,
  complete, already-complete); role/permission history replays; delegated
  permission grants access;
- property: expired roles cannot grant current authority.

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | placeholder guard |
| Goal + regression tests PASS | PASS | 202 tests incl. M1 + G02A-D |
| Lint/type/architecture PASS | PASS | quality gate |
| Schema change has migration test | NOT_APPLICABLE | no schema change; M1 replay green |
| Mutations flow through Validate/Resolve/Commit | PASS | resolvers -> CommitAuthority |
| No domain/core dependency on FastAPI/SQLAlchemy/UI/LLM | PASS | guard |
| Permissions affect allowed actions | PASS | restricted-place entry test |

## Key decisions
- Role/membership/permission/duty as versioned components; permission decisions
  carry provenance (ADR-0015).

## Known limitations
- Full organization decision-making deferred (later phases).

## External blockers
None.

## Final checkpoint
- commit: `goal g02e: institution, authority, duty & norm`
