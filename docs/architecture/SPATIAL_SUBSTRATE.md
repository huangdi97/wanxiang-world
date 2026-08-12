# Spatial Substrate (G02A)

Ownership: `packages/substrate` (`wanxiang_substrate.spatial`), above
domain/runtime; framework-free domain semantics.

## Model

- Spatial state rides on the existing **versioned entity component model**
  (`spatial.region`, `spatial.place`, `spatial.portal`, `spatial.position`,
  `spatial.access_key`, `spatial.place_grant`) ? **no new persisted table** is
  required, so M1 event replay is untouched.
- `SpatialQuery` is a read-only projection of the canonical state:
  - hierarchical containment (place -> region) plus graph topology (portals);
  - portal state (open/closed/locked) with key-based access;
  - deterministic BFS shortest path / reachability / path cost;
  - occupancy/capacity and privacy checks;
  - semantic `VisibilityZone` (open portals) and `AcousticZone`
    (open or closed, not locked) ? no rendering assumptions.

## Authority

Movement and portal changes are **resolvers** registered on the M1 resolver
registry: `spatial.move`, `spatial.set_portal_state`, `spatial.instantiate`.
They read current canonical state, validate, and produce
`ProposedWorldDelta`; only Commit Authority commits. Structured spatial errors
(`PortalLocked`, `PortalClosed`, `PlaceAtCapacity`, `LocationNotReachable`,
`SpatialAccessDenied`) map to no-mutation rejections.

## Fixture

`build_house_fixture_commands` instantiates a source-neutral house
(hall/kitchen/garden, open door, locked door with key, actors with/without
key) via `spatial.instantiate` ? a deterministic world-definition seam that
still flows through Validate/Resolve/Commit.

## Compatibility

- No schema migration required for G02A; the pre-G02 DB (M1 head `0002`)
  upgrades cleanly and the M1 golden fixture replays on the same database.
- Spatial components are schema-versioned (`spatial schema v1`).
