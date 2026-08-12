# ADR-0021: Action, Affordance & Validator Design (G03D)

- Status: accepted
- Date: 2026-08-13

## Context

G03D needs structured action definitions and current-state affordances, then
reject impossible, unauthorized or epistemically invalid actions before
resolution.

## Decision

1. Actions are versioned definitions with parameter schemas in a registry.
2. A side-effect-free validator checks existence/activation, authority,
   reachability, resources, time, visibility and parameter schemas, returning
   structured issues.
3. Affordances are computed per actor from the validator, never mutating state.

## Consequences

- Impossible/unauthorized/epistemic-invalid actions are rejected early with
  structured reasons; the resolver never sees invalid candidates.
