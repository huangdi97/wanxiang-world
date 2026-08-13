# Observation Fusion & Validation (G07B)
Ownership: `wanxiang_substrate.reality.fusion`.

## Policy
`FusionPolicy` is versioned (confidence threshold, conflict window, dedup
window); invalid thresholds are rejected.

## Fusion
`ObservationFusion.fuse` deduplicates identical readings within the window,
fuses consistent duplicates (highest confidence), and retains conflicting
observations as a conflict set with provenance. Outputs are always claims or
proposals — never direct world state. Low-confidence observations defer to
review as `claim_candidate`.