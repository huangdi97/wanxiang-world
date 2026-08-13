# ADR-0038: Reality Bridge Design (G07A)
- Status: accepted
- Date: 2026-08-13

## Context
G07A needs physical observations ingested from deterministic adapters,
normalized, and delivered on a bus, without becoming canonical truth.

## Decision
1. PhysicalObservation is a normalized, provenance-bearing value object; the
   RealityBridge validates and normalizes then publishes readings.
2. Source adapters are a replaceable port; fake sensors and manual reports are
   deterministic.
3. The bridge never mutates canonical world state.

## Consequences
- Observations remain data with provenance; no adapter owns commit authority.