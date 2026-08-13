# Completion Ledger & Review Workflow (G04D)

Ownership: `wanxiang_substrate.ledger` (canon vs reviewed vs inferred content).

## Truth taxonomy

Labels: `canon`, `source_backed`, `completion`, `model_inference`,
`reconstruction`, `user_fiction`. Promotion is deterministic:
user_fiction/model_inference -> completion/reconstruction -> source_backed ->
canon. Model inference and user fiction can never jump straight to canon.

## Review

`CompletionLedger.review` applies an immutable `ReviewDecision` (reviewer +
rationale + review version + evidence refs + override flag). History is
append-only: a reversal adds a new decision; the old decision is never erased.
Canon items are locked; changing them requires an explicit override (branch
rule). Rights-gated: a review cannot promote an item whose rights do not allow
redistribution (`RightsBlocked`).

## Canon rules

- Canon promotion always requires evidence refs (`ReviewRequired` otherwise).
- Once canon, an item is locked; only an override decision changes it.

## Diff

`CompletionLedger.diff(before, after)` reports added/removed items and label
changes between package versions, so review diffs are explicit.

## Integration

Compiled package items (G04C) enter the ledger with their truth label; the
ledger snapshot exposes the label on every item for audit, and can be diffed
across package versions before install (G04E).