# ADR-0011: Spatial Substrate Design (G02A)

- Status: accepted
- Date: 2026-08-13

## Context

G02A needs authoritative spatial semantics (regions/places/portals, access,
capacity, occupancy, reachability) without rendering coordinates and without
breaking M1 event replay.

## Decision

1. Spatial state is expressed as **versioned entity components** on the existing
   M1 component model, not new tables: `spatial.region/place/portal/position/
   access_key/place_grant`. No Alembic migration is required for G02A.
2. `SpatialQuery` is a read-only projection; topology/path/occupancy logic is
   deterministic (BFS by portal count).
3. Movement/portal changes are deterministic resolvers producing
   `ProposedWorldDelta` through the M1 Commit Authority (no second mutation path).
4. Actor identity in commands is `ActorId`; the spatial resolver adapts it to the
   acting `EntityId` at the boundary (an actor is an entity with a position).
5. Keys are entities; actors "hold" keys via `spatial.access_key` components;
   locked portals require the held key entity id.

## Consequences

- M1 replay unchanged; spatial history is normal ordered events.
- Deterministic, no-LLM, no-rendering; Phaser/Godot later only project this.
- Access model is deliberately minimal (key entities + place grants); institution
  roles/permissions deepen in G02E.
