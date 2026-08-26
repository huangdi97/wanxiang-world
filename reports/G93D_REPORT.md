# G93D — Relationship Evolution

Date: 2026-08-27  
Status: PASS

## Implemented contract

`RelationshipEvolutionEvent` is an event-bound signal and
`RelationshipDeltaRule` maps exactly one signal to one existing relationship
dimension. `propose_relationship_evolution` produces an immutable proposal
with the existing `RelationshipState` before/after values and the typed G93A
`RelationshipDelta`; it does not mutate a graph or canonical world.

Rule coefficients and per-event steps are bounded. The resulting dimensions
are clamped to the existing `[-1, 1]` invariant, actor direction and relation
identity must match, ambiguous rules are rejected, and stale proposals cannot
be applied. Provider output is wrapped as a proposal and explicitly rejects
Commit Authority as a producer.

Reviewed proposals append through the existing `RelationshipGraph.revise`
projection history. `RelationshipGraph.replay` reconstructs the same graph,
including the initial state and before/after revision lineage. A separate
read-only `RelationshipBehaviorFeedback` derives cooperation and avoidance
biases for future behavior from relationship dimensions without committing
anything.

## Reproducible evidence

- `tests/unit/substrate/test_g93d_relationship_evolution.py`: 4 passed,
  covering typed event/rule deltas, clamps, provider-only proposals, review
  gating, stale/ambiguous rules, behavior feedback, and replay equality.
- `tests/integration/test_g93d_relationship_evolution_product_chain.py`: 1
  passed. A private rights-approved source traversed OneClickAuthoring,
  PlayableService, Preview, and SQLite WorldRuntime; a committed event became
  relationship evidence, the approved projection history replayed equally,
  and canonical state hash/event count remained unchanged.

## Quality and boundary gates

- G93A-G93C regressions plus G93D focused tests: 26 passed; one existing
  Hypothesis collection warning.
- Ruff check: PASS.
- Pyright on the changed evolution package and G93A-G93D tests: 0 errors,
  0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.
- `git diff --check`: PASS.

G93D is PASS and committed. Gate 30 remains pending until G93H's complete
30-day Actor/Relationship/Organization qualification. G93E-G97J and Gate 24
remain pending; v5.5 remains `IN_PROGRESS / NOT_ACCEPTED`. No private source
was uploaded, no model was trained, and no v5.6 work was started.
