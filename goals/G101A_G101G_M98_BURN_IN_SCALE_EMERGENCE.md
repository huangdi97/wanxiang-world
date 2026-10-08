# G101A–G101G — M98 Emergence / Multi-run / Scale Burn-in

## G101A — Versioned run matrix
Create a machine-readable run registry. Minimum recommended Stable matrix:
- 30d: 3 seeds × 2 policy profiles × 2 pressure profiles = 12 worldlines;
- 90d: 3 seeds × baseline/stress = 6 worldlines;
- deterministic/reference providers by default for cost-bounded reproducibility; any real external provider run is additional evidence, clearly labeled.
Commit: `g101a: define v5.5 burn in run matrix`

## G101B — 30d multi-run
Run the 30d matrix with per-run WorldRunArtifact, checkpoint, replay hash, event counts, actor/relationship/org metrics, provider/runtime-control refs and failures.
Gate 73 must not accept partial-row aggregation as full matrix success.
Commit: `g101b: execute thirty day multi run burn in`

## G101C — 90d multi-run
Run the defined 90d subset. Verify crash/restart, checkpoint resume, branch isolation and replay equality on selected runs.
Gate 74 acceptance requires no unreconciled replay/branch/state corruption.
Commit: `g101c: execute ninety day burn in`

## G101D — Bounded emergence & false-positive controls
Measure Pattern/Norm/Organization/Institution candidates across runs. Add null/control evidence (e.g. shuffled temporal relation or synthetic no-pattern control) only as a detector calibration aid, not as a replacement for real runs.
Required safety property: no emergence candidate may auto-commit Ontology/Law/Institution reality without its existing validation/promotion boundary.
Report recurrence/support and false positives. No universal-emergence claim.
Commit: `g101d: qualify bounded emergence repeatability`

## G101E — Scale ladder
Using one frozen standard world/profile, test 10 → 50 → 100 → 500 → 1000 actors with Simulation LOD. Prefer at least 3 repetitions per tier where runtime cost permits.
Record actual active/full-policy actor counts separately from population size.
Commit: `g101e: execute actor scale ladder`

## G101F — Capacity/degradation curve
Record, at minimum:
CPU, peak RSS/RAM, DB bytes, event count/rate, provider calls, tick/action p50/p95, checkpoint duration/size, replay duration, recovery duration, storage growth and any monetary provider cost.
Find the actual knee/degradation point; do not extrapolate 10k/100k.
Commit: `g101f: publish v5.5 capacity and cost curve`

## G101G — M98 qualification
Write:
- `reports/M98_EMERGENCE_MULTI_RUN_SCALE_BURN_IN.md`
- `artifacts/v55_stable/m98/burn_in_summary.json`
- `artifacts/v55_stable/m98/scale_curve.json`
- `artifacts/v55_stable/m98/emergence_controls.json`

Accept Gates 73–77 only with complete evidence or explicitly documented failed tier/matrix. A failed high tier may still produce a valid measured capacity limit, but any corruption, unrecoverable replay mismatch or silent data loss is release-blocking until fixed.
Commit: `g101g: qualify m98 burn in and scale evidence`
