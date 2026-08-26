# G89E — RelationshipState v1

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Evidence

`RelationshipState` is an actor-continuity projection over the existing world
relation boundary. It carries bounded trust, affection, hostility, debt,
loyalty, dependency, authority, and reputation dimensions, a valid-from/to
interval, event references, relation type, and an explicit visibility policy.
It does not replace `RelationState` or write canonical relations.

`RelationshipGraph` stores immutable revision lineage and replays the same
before/after sequence. Historical state can be queried at a tick; later
revisions do not erase the earlier interval. `visible_to` returns only public
relations or relations permitted by the participant/source policy. A private
source relation is invisible to the target and an unrelated observer, while an
explicit admin projection can inspect it.

## Gates

| Gate | Result |
|---|---|
| Eight relationship dimensions and bounds | PASS |
| Valid-from/to time projection | PASS |
| Event refs and before/after replay | PASS |
| Relation evolution replay | PASS |
| No global omniscience | PASS |
| Ruff / format / Pyright | PASS; 0 errors |
| Architecture conformance | PASS |
| Actor-continuity regression | PASS; 10 passed, 1 expected Hypothesis warning |

Gate 10 (`RelationshipState time/event provenance`) is **ACCEPTED** in
`reports/V55_ACCEPTANCE_MATRIX.md`. v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**;
G89F is next.
