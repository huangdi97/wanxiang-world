# ADR-0028: Completion Ledger & Review Workflow Design (G04D)

- Status: accepted
- Date: 2026-08-13

## Context

G04D needs to keep canon, source-backed facts, completion, model inference,
reconstruction and user fiction strictly separate through an auditable
approval/completion ledger, without auto-labeling completion as fact.

## Decision

1. Truth labels follow a deterministic promotion graph; model inference and
   user fiction can never jump straight to canon.
2. Every promotion is an immutable ReviewDecision (reviewer + rationale +
   review version + evidence); history is append-only and reversals preserve
   the old decision.
3. Canon promotion requires evidence; canon items are locked and changes need
   an explicit override (branch rule).
4. Rights gate: review cannot promote items whose rights disallow
   redistribution.
5. Package-version diffs are explicit (added/removed/label-changed).

## Consequences

- No label is treated as fact without review/evidence; review history is
  immutable; canon is stable until an audited override.