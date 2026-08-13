# ADR-0039: Observation Fusion & Validation Design (G07B)
- Status: accepted
- Date: 2026-08-13

## Context
G07B needs deterministic fusion that preserves conflicts and emits only
claims/proposals.

## Decision
1. FusionPolicy is versioned with thresholds; fusion dedups consistent
   duplicates and retains conflicts as conflict sets with provenance.
2. Outputs are proposals or claim candidates (deferred), never direct state.

## Consequences
- Conflicting inputs are never overwritten or blindly averaged; high-confidence
  validated changes are proposals only.