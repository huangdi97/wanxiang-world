# G89D — Belief Revision

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Evidence

The existing `BeliefAssertion` now carries an explicit actor-local stance
(`supported`, `contested`, or `unknown`) in addition to confidence and status
lineage. `BeliefRevisionEngine` creates typed support, contradict, refine, and
unknown before/after projections with a new assertion id, evidence ref, reason,
and `supersedes` lineage. `BeliefRevisionChain` preserves the prior assertion
and rejects a revision that does not continue the current chain. No revision
method writes canonical state or declares a belief to be World Truth.

`BeliefEvidence` contains only an actor, time, strength, temporal scope, and an
opaque reference. Future-scoped evidence is rejected before revision, so a
runtime actor cannot receive future knowledge. Contradictory evidence lowers
confidence and marks the new assertion contested; it does not erase the prior
possibly-false belief. Unknown is explicit rather than silently treated as
truth or deletion.

## Gates

| Gate | Result |
|---|---|
| Support / contradict / refine / unknown outcomes | PASS |
| Confidence update and false-belief preservation | PASS |
| Before/after revision lineage | PASS |
| Rumor is not World Truth | PASS; existing G03B authority regression |
| Future-knowledge leak rejection | PASS; G35G character boundary regression |
| Ruff / format / Pyright | PASS; 0 errors |
| Architecture conformance | PASS |
| Belief, memory, propagation, character-boundary and replay regression | PASS; 24 passed, 1 expected Hypothesis warning |

Gate 9 (`Secret / rumor / future-knowledge isolation`) is **ACCEPTED** in
`reports/V55_ACCEPTANCE_MATRIX.md`. v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**;
G89E is next.
