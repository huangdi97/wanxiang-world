# 90-day Worldness & Population-LOD Qualification (G15G)

## Declared profile (small CI)
- World: Synthetic Full Reference World; seed per chunk (1000..1005); runtime versions SchemaVersion(1)/RuntimeVersion(1).
- Horizon: 90 simulated days (9000 ticks) in 6 x 15-day chunks; accelerated simulation (NOT real-time hosting).
- Scale claim states hardware/profile/seed/runtime versions as recorded here.

## Results
| Criterion | Result |
|---|---|
| 90-day run completes (9000 ticks) | PASS (~39s CI) |
| No unbounded growth (entities bounded <= 30; per-chunk events monotonic) | PASS |
| Dormant actors resume consistently (all 4 people valid at the end) | PASS |
| No scheduler starvation (duty events committed; multi-rate LOD) | PASS |
| Sampled replay spot checks match recorded hashes (each 15-day chunk) | PASS |
| Full replay + restore reproduce final hash | PASS |

## LOD mechanism
Multi-rate population scheduling (duty=25, focus=30, lightweight=50/60 tick rates) implements
active/background/dormant LOD; no ephemeral cognition artifacts are retained beyond world entities.

## Evidence
- `uv run pytest tests/integration/test_g15g_ninety_day.py -q` -> 1 passed (39s).
