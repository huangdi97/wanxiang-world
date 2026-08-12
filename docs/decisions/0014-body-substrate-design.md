# ADR-0014: Body & Condition Substrate Design (G02D)

- Status: accepted
- Date: 2026-08-13

## Context

G02D needs body/condition state as constraints on action, schedule and
perception, not decorative RPG stats.

## Decision

1. Body condition is a versioned component with bounded facets (0..100) and
   deterministic capability derivation (mobility, fatigue, sleep).
2. Condition changes are resolvers through the M1 authority; ranges validated.
3. A capability check (`BodyQuery.can_move`) is consulted by the spatial move
   resolver: fatigue/immobility blocks otherwise-valid movement.
4. Condition facets have observable/private visibility; public projection
   excludes private facets.

## Consequences

- Deterministic, replayable condition evolution; action constraints without
  direct coupling for actors lacking a body component.
- No medical advice/biological modeling (explicitly out of scope).
