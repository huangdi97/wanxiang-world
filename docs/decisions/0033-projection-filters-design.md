# ADR-0033: Projection API, Perspective & Rights Filters Design (G05D)

- Status: accepted
- Date: 2026-08-13

## Context

G05D needs server-composed projections that enforce knowledge/rights filters,
never return raw canonical state by default, and require privilege for debug.

## Decision

1. Projection contracts are DTOs separate from canonical types.
2. ProjectionService composes perception/knowledge + rights/privacy + mode
   filters server-side; debug requires explicit admin privilege.
3. Sealed payloads are redacted, private beliefs/memories never leak, and
   restricted places are redacted without permission; truth labels are
   included.

## Consequences

- Client-side state can never protect secrets; projections carry provenance
  labels and redaction metadata.