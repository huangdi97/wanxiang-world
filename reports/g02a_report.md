# Goal G02A Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: d042fc7 (continuation pack baseline)
- working-tree notes: clean

## Objective
Build the authoritative spatial substrate (regions/places/rooms/portals/edges/
occupancy/visibility/acoustic zones/access) used by world logic, with movement
routed through the M1 Commit Authority path.

## Delivered
- `packages/substrate` (`wanxiang_substrate.spatial`):
  - model: PlaceTopology, PortalLink, PortalState, PrivacyLevel, SpatialSnapshot,
    Occupancy, VisibilityZone, AcousticZone, AccessPolicy, SpatialPath;
  - errors: SpatialError taxonomy (PortalLocked/PortalClosed/PlaceAtCapacity/
    LocationNotReachable/SpatialAccessDenied);
  - components: versioned spatial components (schema v1);
  - query: read-only SpatialQuery (containment, neighbors, BFS path/cost,
    reachability, capacity/occupancy, portal access, visibility/acoustic zones);
  - resolver: spatial.move / spatial.set_portal_state / spatial.instantiate;
  - fixture: synthetic house (hall/kitchen/garden, open door, locked door + key,
    actors with/without key).
- Architecture guard rule for `packages/substrate` + negative test.
- `docs/architecture/SPATIAL_SUBSTRATE.md`, ADR-0011.

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run pytest -q` | 153 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests:
- unit: model invariants; query (containment, neighbors, path cost, reachability,
  capacity, key access, zones, disconnected place);
- integration: move through open door; locked portal rejects without key
  (no mutation); key holder passes; closed portal rejects; capacity overflow
  rejects; spatial replay deterministic; M1 golden replay unaffected;
  pre-G02 DB upgrades cleanly (head stays `0002`) + M1 fixture + spatial replay;
- property: entity has a single valid location after valid commits; rejected
  moves leave state unchanged.

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Implementation tasks complete; no TODO/placeholder in production path | PASS | placeholder guard |
| Goal-specific + milestone-regression tests PASS | PASS | 153 tests incl. M1 suite |
| Lint/type/architecture PASS | PASS | quality gate |
| Schema change (if any) has migration/compat test | PASS | none required; pre-G02 upgrade + M1 fixture replay test |
| Canonical mutations flow through Validate/Resolve/Commit with audit | PASS | resolvers -> CommitAuthority |
| No new domain/core dependency on FastAPI/SQLAlchemy/UI/LLM | PASS | guard rule + negative test |

## Key decisions
- Spatial state on versioned components (no migration); ADR-0011.
- ActorId -> EntityId adapter at resolver boundary.

## Known limitations
- Access model is minimal (key entities + place grants); institution roles are G02E.
- Zones are single-hop semantic models; propagation rules can deepen later.

## External blockers
None.

## Final checkpoint
- commit: `goal g02a: spatial topology & access`
