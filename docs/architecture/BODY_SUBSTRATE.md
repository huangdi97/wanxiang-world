# Body & Condition Substrate (G02D)

Ownership: `wanxiang_substrate.body` (body/condition state as constraints).

## Model

- `BodyCondition`: bounded facets (health/energy/sleep/pain/mobility in 0..100),
  deterministic mobility capability and fatigue/sleep thresholds.
- `MobilityCapability`: unrestricted / reduced / immobile derived from mobility.
- `visible_facets`: public projection excluding private facets (privacy).

## Authority

- `body.exert` / `body.rest`: deterministic bounded energy/sleep transitions.
- `body.apply_condition`: validated facet updates (out-of-range rejected).
- `body.medicate`: attaches an active medication record.
- `body.set_visibility`: marks facets private for public projection.

## Capability integration

The spatial move resolver consults `BodyQuery.can_move(actor)`; a fatigued or
immobile actor cannot move even through a spatially valid path
(`BodyConstraintViolation`). Actors without a body condition are unaffected
(no coupling for the M1 micro-world).

## Compatibility

- Body state rides on versioned components (`body` schema v1); no new
  migration; M1 replay untouched.
- Condition evolution replays deterministically.
