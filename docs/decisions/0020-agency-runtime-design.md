# ADR-0020: Actor & Organization Runtime Design (G03C)

- Status: accepted
- Date: 2026-08-13

## Context

G03C needs actors, organizations, controller policies, membership, command
flow and information flow without treating organizations as giant chat agents.

## Decision

1. Policies expose a propose-only `IntentCandidate`; they never mutate state
   and only receive knowledge-bounded context.
2. Orders are versioned components with an explicit lifecycle and typed
   transitions; invalid transitions raise `OrderStateConflict`.
3. Policy context is authorized information (observations/beliefs only).

## Consequences

- Deterministic, replayable orders; policies cannot access commit repositories
  through the interface; organizations are runtime aggregates, not chat agents.
