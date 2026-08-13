# ADR-0049: Liaoshen Source-gated Reference Pack Design (G11F)
- Status: accepted
- Date: 2026-08-13

## Context
G11F needs a Liaoshen reference pack; real historical data is not available
with rights.

## Decision
1. Real pack is EXTERNAL_BLOCKED; only the manifest template and synthetic
   campaign are committed.
2. Historical vs counterfactual labels are preserved; missing history is never
   fabricated; generic M8 is not blocked.

## Consequences
- The platform is proven without inventing campaign history.