# ADR-0018: Observation & Perspective Isolation Design (G03A)

- Status: accepted
- Date: 2026-08-13

## Context

G03A needs actors to receive only information they could perceive or be told,
with observed fact separated from interpretation/belief.

## Decision

1. Observations are derived on demand from committed events plus spatial
   (visibility/acoustic) and rights (visibility level, membership) conditions;
   they are not persisted separately.
2. Each observation carries source event id, channel, confidence and the rules
   that allowed it (auditable).
3. `ObservationFact` never contains sealed payload content; custody does not
   imply knowledge.
4. Visibility (public/group/private) is a versioned component on actors.

## Consequences

- Deterministic, replayable perspectives; branch perspectives differ only when
  branch events justify it; projection/cognition consume the read-model only.
