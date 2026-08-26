# G89A — ActorGoalStack v1

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Evidence

`ActorGoalStack` is an immutable actor-local projection in
`wanxiang_substrate.actor_continuity`. It defines the five product tiers
`life_motive`, `long_term`, `medium_term`, `short_term`, and `intent`, with
priority, dependency, deadline, status, timestamps, and explicit
`GoalProvenance`. Named tier aliases keep the product vocabulary available
without introducing five divergent schemas.

`GoalRevisionEvent` records a sequence, reason, evidence references, before /
after values, and an external event reference. `ActorGoalStack.apply` is a
deterministic projection operation; it does not call a Commit Authority or
mutate canonical state. Replay rejects actor, sequence, or before-value
mismatches.

Serialization is schema-versioned (`schema_version=1`) and includes both the
goal snapshot and revision lineage. Deserialization replays the revisions and
verifies that the serialized snapshot matches the replayed result. The goal
record contains no canonical entity type, world-truth value, or world-state
mutation operation; provenance is actor-facing evidence only.

## Gates

| Gate | Result |
|---|---|
| Goal stack serialization round-trip | PASS |
| Revision event replay and stale re-application rejection | PASS |
| Dependency / priority / five-tier contract validation | PASS |
| Goal is not world fact | PASS |
| Ruff / format / Pyright | PASS; 0 errors |
| Architecture conformance | PASS |
| v5.4 agency + epistemic regression | PASS; 18 passed, 1 expected Hypothesis warning |

No database schema was changed in G89A, so no migration was required. Durable
cross-session storage remains a later bounded goal and must use the existing
persistence/event boundaries.

M86 Gate 7 (`ActorGoalStack persistence/replay`) is accepted in
`reports/V55_ACCEPTANCE_MATRIX.md`. v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**;
G89B is next.
