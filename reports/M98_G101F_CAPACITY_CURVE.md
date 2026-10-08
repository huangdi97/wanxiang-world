# M98 G101F Capacity and Degradation Curve

Conclusion: PASS — 15/15 rows completed.

This report is derived from the same frozen standard fixture and the complete
15-row G101E ladder. Every row records CPU, peak RSS/RAM, database bytes,
event count/rate, provider calls and cost basis, tick/action p50/p95,
checkpoint duration/size, replay/recovery duration, and storage growth.

Measured degradation result: 500_actor_tier_by_superlinear_recovery; population ratio 5.0; recovery ratio 9.003203. The rule is the first adjacent
tier where maximum recovery duration grows faster than population. This is a
local SQLite/reference-provider observation, not a hard production capacity
limit.

The local reference provider has no monetary charge. No live-provider cost,
live-PostgreSQL, scientific-validity, or universal-emergence claim is made;
10k/100k extrapolation is explicitly forbidden. SimulationLOD active counts
remain separate from full-policy population counts.

Machine-readable evidence: artifacts/v55_stable/m98/capacity_curve.json
Source scale evidence: artifacts/v55_stable/m98/scale_curve.json
