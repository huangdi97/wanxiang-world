# ADR-0022: Resolver, Adjudication & Deterministic Policies Design (G03E)

- Status: accepted
- Date: 2026-08-13

## Context

G03E needs to resolve valid actions into auditable outcomes and deltas using
deterministic rules/probability where configured, with provenance and version
pinning.

## Decision

1. Adjudicators are registered by (action, version) and return an
   `Adjudication` (outcome + delta + explanation + provenance + uncertainty);
   they never commit.
2. `SeededRng` provides deterministic probability with explicit RNG ownership.
3. The adjudication service dry-runs the delta on a copy before Commit
   Authority; resolver versions are pinned per action.

## Consequences

- Deterministic, replayable adjudication; missing/incompatible versions fail
  explicitly; narrative text never decides canonical outcomes.
