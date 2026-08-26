# G89G — Actor Continuity Projection

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Evidence

`ActorContinuityProjection` builds a frontend-safe, deterministic timeline DTO
from the existing ActorGoalStack, Epistemic Memory/Belief records,
RelationshipGraph, and action explanation refs. Actor views contain Goal,
Memory, Belief, Relationship, and Action items; action items expose only
reference IDs in `why_refs`, not hidden reasoning content. The snapshot has a
stable `to_dict` contract for a client surface.

The viewer is enforced server-side in the projection builder. The target actor
or an explicit admin can inspect private cognition. An observer receives
redacted categories for Goal/Memory/Belief, receives only relations permitted
by RelationshipGraph visibility, and gets no private why refs. The projection
has no write method and owns no canonical state.

## Gates

| Gate | Result |
|---|---|
| Goal / Memory / Belief / Relationship timeline DTO | PASS |
| Why-action explanation refs | PASS |
| Actor-only vs observer permission boundary | PASS |
| Private cognition redaction | PASS |
| Ruff / format / Pyright | PASS; 0 errors |
| Architecture conformance | PASS |
| Actor-continuity projection regression | PASS; 6 passed, 1 expected Hypothesis warning |

M86 Gate 11 remains pending until G89H completes the multi-day continuity
qualification. v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**; G89H is next.
