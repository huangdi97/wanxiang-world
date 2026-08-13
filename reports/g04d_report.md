# Goal G04D Acceptance Report

## Status
PASS

## Pre-goal state
- branch: master
- commit: 62167c1 (G04C checkpoint)
- working-tree notes: clean before G04D work

## Objective
Separate canon/source-backed facts, reviewed completion, model inference and
user fiction through an auditable approval/completion ledger.

## Delivered
- `wanxiang_substrate.ledger`: truth-label taxonomy with deterministic
  promotion graph, CompletionLedger with immutable ReviewDecision history,
  canon lock + override rules, rights gate, package-version diff, audit
  snapshot, and fixtures (inference/reviewed/canon/rights-denied).

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run python scripts/quality.py` (full gate) | 302 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests (`tests/integration/test_completion_ledger.py`, 9 tests):
- unit: taxonomy and transition rules;
- negative: model inference cannot become canon without review/evidence;
- unit: promotion path to canon requires evidence;
- unit: canon lock requires override;
- history: reversal preserves the old decision (append-only);
- rights: review cannot approve disallowed redistribution;
- audit: every item exposes a truth label;
- unit: package-version diff (added/removed/label-changed);
- audit: reviewer and rationale exposed on the item.

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | guard + review |
| Goal + regression tests PASS | PASS | 302 tests incl. M1-M3/G04A-C |
| Lint/type/architecture PASS | PASS | full quality gate |
| Model inference cannot become canon unearned | PASS | negative tests |
| History immutable on reversal | PASS | history test |
| Rights gate enforced | PASS | rights test |
| Truth label exposed on every item | PASS | audit test |
| No new forbidden dependency | PASS | architecture guard |

## Key decisions
- Deterministic promotion graph; canon locks with override; evidence required
  for canon (ADR-0028).

## Known limitations
- In-memory ledger; durable persistence of review history is a later concern.

## External blockers
None.

## Final checkpoint
- commit: `goal g04d: completion ledger & review workflow`