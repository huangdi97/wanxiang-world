# M98 G101E/G101F Scale Ladder and Capacity Measurements

**Conclusion:** `PASS` — `15/15` rows completed.

The runner used the frozen `m98-standard-scale-template-v1` standard fixture template and
`book` profile through OneClickAuthoring, PlayableService, Commit Authority, and
real migrated SQLite runtimes. It measured 10, 50, 100, 500, and 1000 actor
tiers with three independent repetitions per tier. Population size, actual
full-policy actor count, and SimulationLOD L0/L1 active count are separate fields.

Each completed row records provider calls/cost basis, CPU, peak RSS, database
bytes and growth, event count/rate, tick/action p50/p95, checkpoint duration and
storage delta, replay/recovery durations, package/world/branch refs, and
replay/recovery/proposal-only/LOD checks. Build SHA: `09c161c79f14911c804b3d22c38896c3545c41cf`; template
hash: `e43135ca34d98d5cf6d619b13173eb6dcbc8baa8cabbe0e653141288613ea129`.

All results are bounded local engineering measurements. A passing 1000-actor
tier is not extrapolated to 10k/100k. The reported knee is the first measured
super-linear recovery-duration point, not a production capacity limit. The
local reference provider has no monetary charge; no production capacity or
universal-emergence claim is made.

Machine-readable evidence: `artifacts/v55_stable/m98/scale_curve.json`.
