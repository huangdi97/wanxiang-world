# Goal G15G Acceptance Report — Extended 90-day Virtual Run & Population-LOD Qualification

## Status
PASS

## Objective
Extend worldness beyond a seven-day showcase and verify long-horizon stability, memory metabolism and population scheduling under controlled scale.

## Delivered
- `tests/integration/test_g15g_ninety_day.py` — 90-day run with sampled checkpoints + replay spot checks.
- `reports/NINETY_DAY_WORLDNESS_AND_LOD.md`, `reports/G15G_REPORT.md`.

## Findings
- 90 simulated days complete deterministically (~39s CI) with bounded growth and monotonic per-chunk events.
- Dormant actors resume consistently; no scheduler starvation (duty events present).
- Sampled replay spot checks and full restore reproduce recorded hashes.

## Evidence
- 1 test passed (39s); ruff/pyright clean.
- Scale claims are environment-measured and state profile/seed/versions.

## Remaining limitations
- Accelerated simulation, not real-time 90-day hosting; retention policy documented (no unbounded artifact growth).

## Final checkpoint
- commit: `g15g: extended 90-day virtual run & population-lod qualification`
