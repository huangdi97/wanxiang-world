# Observation & Perspective Isolation (G03A)

Ownership: `wanxiang_substrate.observation` (explicit observations, perspective
boundaries; no canonical truth copied into actor context).

## Model

- `Observation`: observer, source event (provenance), world time, place,
  channel (visual/acoustic/textual), typed `ObservationFact`, confidence, and
  the rules that allowed it (`rule_refs`).
- `ObservationFact`: a derived fact about what happened (movement, transfer,
  announcement) ? never the canonical payload itself.
- `EntityVisibility`: public / group / private marking on an entity's actions.

## Perspective service

`PerspectiveService.context_for(observer, events)` assembles the observations
an observer could perceive, derived from committed events plus spatial
(visibility/acoustic zones) and rights (visibility level, group membership)
conditions:

- visual: same place or line-of-sight through open portals;
- acoustic: through open/closed (not locked) portals;
- textual: direct announcements in the same place;
- private events visible only to the actor; group events only to members.

Each observation records the rule that allowed it (audit). A sealed payload's
content never appears in observations (custody != knowledge).

## Compatibility

- Observations are a derived read-model (not persisted separately); they replay
  deterministically from events + state. Visibility markings are versioned
  components; no new migration.
